import requests
import pandas as pd
import pandas_ta as ta
import os
import sys
import time

# Configurações de API (GitHub Secrets)
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Watchlist de Narrativas Prioritárias para 2026
WATCHLIST = {
    'IA': ['TAO', 'FET', 'RENDER', 'TRAC', 'AIOZ', 'VIRTUAL'],
    'RWA': ['ONDO', 'PENDLE', 'AVAX', 'LINK', 'PROPC'],
    'DePIN': ['AKT', 'HNT', 'AR', 'THETA']
}

def check_bitcoin_safety():
    """Cancela o envio se o BTC cair > 5% em 24h."""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {'ids': 'bitcoin', 'vs_currencies': 'usd', 'include_24hr_change': 'true'}
    try:
        res = requests.get(url, params=params).json()
        change_24h = res['bitcoin']['usd_24h_change']
        if change_24h < -5.0:
            return False, change_24h
        return True, change_24h
    except:
        return True, 0 # Segurança em caso de falha da API

def send_telegram(message):
    if not TOKEN or not CHAT_ID: return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown", "disable_web_page_preview": True}
    requests.post(url, json=payload)

def get_coin_details(coin_id):
    """Busca corretoras e resumo do projeto."""
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    params = {'localization': 'false', 'tickers': 'true', 'market_data': 'false'}
    try:
        time.sleep(1.3) # Respeita limite da API Free
        res = requests.get(url, params=params).json()
        exchanges = sorted(list(set([t['market']['name'] for t in res.get('tickers', [])])), key=len)[:3]
        desc = res.get('description', {}).get('en', '').split('. ')[0]
        return ", ".join(exchanges), (desc[:120] + '...')
    except:
        return "DEX", "Resumo indisponível."

def analyze_market():
    # Validação de Segurança do Bitcoin
    is_safe, btc_change = check_bitcoin_safety()
    if not is_safe:
        return f"⚠️ *RELATÓRIO CANCELADO*\nO Bitcoin caiu {btc_change:.2f}% nas últimas 24h. Bot em modo de segurança para evitar falsos sinais."

    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {'vs_currency': 'usd', 'order': 'volume_desc', 'per_page': 150, 'sparkline': 'true'}
    coins = requests.get(url, params=params).json()
    
    opportunities = []
    extreme_alerts = []
    best_bet = None

    for coin in coins:
        symbol = coin['symbol'].upper()
        if symbol in ['USDT', 'USDC', 'BTC', 'ETH', 'FDUSD'] or coin['total_volume'] < 5000000: continue

        prices = coin['sparkline_in_7d']['price']
        if len(prices) < 14: continue
        
        df = pd.DataFrame(prices, columns=['close'])
        rsi = ta.rsi(df['close'], length=14).iloc[-1]
        vol_mcap = coin['total_volume'] / (coin['market_cap'] or 1)
        
        narrative = "Global"
        for cat, symbols in WATCHLIST.items():
            if symbol in symbols:
                narrative = cat
                break

        # Filtros Técnicos
        if 20 < rsi < 65 and vol_mcap > 0.05:
            exchanges, summary = get_coin_details(coin['id'])
            icon = "🟢" if rsi < 45 else "🟡"
            if rsi < 35:
                icon = "🔥"
                extreme_alerts.append(f"⚠️ *SOBREVENDA:* {coin['name']}!")

            msg = (f"{icon} *{coin['name']}* ({symbol})\n"
                   f"🏷️ *Setor:* {narrative} | RSI: {rsi:.2f}\n"
                   f"🏛️ *Exchanges:* {exchanges}\n"
                   f"📝 {summary}\n")
            
            opportunities.append(msg)
            if narrative != "Global" and (best_bet is None or rsi < best_bet['rsi']):
                best_bet = {'msg': msg, 'rsi': rsi, 'name': coin['name']}

            if len(opportunities) >= 10: break

    header = f"🚀 *ALTCOIN HUNTER REPORT*\n📅 {time.strftime('%d/%m/%Y %H:%M')}\n"
    if extreme_alerts: header += "\n" + "\n".join(extreme_alerts) + "\n"
    if best_bet: header += f"\n🏆 *APOSTA DO DIA: {best_bet['name']}*\n"
    
    return header + "\n----------------------------------\n" + "\n".join(opportunities)

if __name__ == "__main__":
    send_telegram(analyze_market())