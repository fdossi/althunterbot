# 📖 Manual do Usuário - AltHunterBot

Este manual fornece orientações detalhadas sobre como configurar, operar e interpretar os dados gerados pelo **AltHunterBot**.

---

## 1. Configuração Inicial

### 1.1 Telegram
1.  Inicie uma conversa com o [@BotFather](https://t.me/botfather) e crie um bot para obter seu `API TOKEN`.
2.  Para obter o `CHAT_ID` do seu grupo:
    * Adicione o bot ao grupo e promova-o a administrador.
    * Acesse a versão Web do Telegram; o ID do grupo estará na URL (ex: `-100...`).
    * **Importante:** IDs de grupos devem conter o prefixo `-100`.

### 1.2 GitHub Secrets
No seu repositório GitHub, vá em `Settings > Secrets and variables > Actions` e adicione:
* `TELEGRAM_TOKEN`: O token do seu bot.
* `TELEGRAM_CHAT_ID`: O ID do chat ou grupo de destino.

---

## 2. Funcionamento do Sistema

### 2.1 Agendamento (Cron Job)
O bot está configurado no arquivo `main.yml` para rodar automaticamente nos seguintes horários:
* **07:00 BRT** (10:00 UTC)
* **12:00 BRT** (15:00 UTC)

### 2.2 Alça de Segurança (Bitcoin Safety)
O bot possui um mecanismo de proteção de capital. Se a variação do Bitcoin nas últimas 24 horas for inferior a **-5%**, a varredura de altcoins é abortada. Um aviso será enviado ao Telegram informando que o mercado está em "modo de segurança".

---

## 3. Interpretando o Relatório

Cada ativo listado no relatório apresenta as seguintes métricas:

* **Status Visual:**
    * 🔥 **Fogo:** Ativo em sobrevenda extrema (RSI < 35). Indica alta probabilidade de repique técnico.
    * 🟢 **Verde:** Momentum de compra saudável (RSI 35-45).
    * 🟡 **Amarelo:** Ativo em zona neutra ou de consolidação (RSI 45-65).
* **V/MCap (Volume / Market Cap):** Indica a liquidez proporcional ao tamanho do ativo. Valores acima de **0.07** sugerem forte interesse e volume institucional.
* **🏛️ Exchanges:** Lista as 3 principais corretoras para facilitar a execução da ordem.
* **🏆 Aposta do Dia:** O algoritmo seleciona o ativo da sua Watchlist prioritária (IA, RWA, DePIN) que apresenta o melhor setup de entrada no momento.

---

## 4. Resolução de Problemas

* **O Bot não enviou o relatório:**
    1. Verifique na aba **Actions** do GitHub se o workflow falhou.
    2. Se houver falha, você receberá um alerta automático no Telegram com o link direto para o log de erro.
    3. Verifique se o Bitcoin não caiu mais de 5% no dia, o que causaria o cancelamento automático.
* **Erro "403 Forbidden":** Verifique se você iniciou o bot no Telegram com o comando `/start`.
* **Erro de API (Rate Limit):** O bot utiliza a versão gratuita da CoinGecko. O script possui pausas automáticas (`time.sleep`) para evitar bloqueios.

---

## 5. Boas Práticas
* **Não use o Bot isoladamente:** Utilize os sinais do AltHunterBot como um filtro inicial e valide o gráfico manualmente antes de entrar em uma operação.
* **Monitore Narrativas:** A Watchlist foca em setores de alto crescimento (IA, RWA, DePIN). Se uma nova narrativa surgir, atualize o dicionário `WATCHLIST` no arquivo `altcoin_bot.py`.