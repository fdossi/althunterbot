import requests
import pandas as pd
import pandas_ta as ta
import os
import sys

# Pega as chaves das variáveis de ambiente (Secrets do GitHub)
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_telegram(message):
    if not TOKEN or not CHAT_ID:
        print("Erro: Variáveis de ambiente TELEGRAM_TOKEN ou CHAT_ID não configuradas.")
        sys.exit(1)
        
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Relatório enviado com sucesso para o Telegram!")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar mensagem: {e}")

def analyze_market():
    # 1. Busca dados da CoinGecko (Top 250 moedas por Volume)
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'volume_desc',
        'per_page': 250,
        'page': 1,
        'sparkline': 'true'
    }
    
    try:
        response = requests.get(url, params=params)
        coins = response.json()
    except Exception as e:
        return f"Erro ao acessar API CoinGecko: {e}"
    
    opportunities = []
    
    for coin in coins:
        # Filtros básicos: Ignora stables e moedas sem market cap
        if coin['symbol'] in ['usdt', 'usdc', 'fdusd', 'busd', 'btc', 'eth']: continue
        if not coin['market_cap'] or not coin['total_volume']: continue

        # 2. Análise de RSI (Sparkline de 7 dias)
        prices = coin['sparkline_in_7d']['price']
        if len(prices) < 14: continue
        
        df = pd.DataFrame(prices, columns=['close'])
        rsi = ta.rsi(df['close'], length=14).iloc[-1]
        
        # 3. Métrica de Momentum (Volume / Market Cap)
        vol_mcap = coin['total_volume'] / coin['market_cap']
        
        # 4. Critério de Seleção (RSI saudável + Volume forte)
        if 30 < rsi < 60 and vol_mcap > 0.08:
            status = "🟢" if rsi < 45 else "🟡"
            opportunities.append(
                f"{status} *{coin['name']}* ({coin['symbol'].upper()})\n"
                f"💰 Preço: ${coin['current_price']}\n"
                f"📊 RSI: {rsi:.2f} | Vol/Mcap: {vol_mcap:.2f}\n"
                f"📈 24h: {coin['price_change_percentage_24h']:.2f}%\n"
            )

    # Montagem do Relatório
    header = "🚀 *ALTCOIN HUNTER REPORT* 🚀\n"
    header += "----------------------------------\n"
    
    if not opportunities:
        return header + "Nenhuma oportunidade clara detectada agora."
    
    body = "\n".join(opportunities[:10]) # Top 10
    footer = "\n\n⚠️ *Atenção:* Analise a listagem em exchanges antes de operar."
    
    return header + body + footer

if __name__ == "__main__":
    report_content = analyze_market()
    send_telegram(report_content)