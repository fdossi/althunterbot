# 🚀 AltHunterBot - Crypto Scanner

O **AltHunterBot** é um sistema automatizado em Python que realiza varreduras diárias no mercado de criptomoedas em busca de ativos com alto potencial de valorização no curto prazo. Ele prioriza as narrativas dominantes de 2026: **IA (Inteligência Artificial), RWA (Real World Assets) e DePIN (Infraestrutura Física Descentralizada)**.

O bot analisa dados técnicos, volume e liquidez em corretoras Tier 1, enviando relatórios detalhados diretamente para um grupo ou chat no **Telegram**.

## 📊 Funcionalidades Principais

O script utiliza **GitHub Actions** para automação serverless e executa as seguintes etapas:

1.  **Alça de Segurança (Bitcoin Safety):** Antes de analisar qualquer altcoin, o bot verifica a variação do Bitcoin nas últimas 24h. Se a queda for superior a **5%**, o relatório é cancelado para proteger o usuário de sinais falsos em quedas sistêmicas.
2.  **Filtro de Narrativas:** Prioriza moedas de setores estratégicos como IA, RWA e DePIN.
3.  **Análise de Momentum:** Calcula o **RSI (14 períodos)** e a relação **Volume/Market Cap**. Valores de V/MCap acima de 0.07 sugerem forte interesse institucional.
4.  **Alerta de Sobrevenda (🔥):** Ativos com **RSI < 35** são destacados com um ícone de fogo, indicando oportunidades de exaustão de venda.
5.  **Aposta do Dia:** Identifica automaticamente o ativo da watchlist com o melhor setup técnico para reversão imediata.
6.  **Contexto do Ativo:** Para cada oportunidade, o bot busca um resumo do projeto e as principais corretoras onde está listado.
7.  **Notificação de Erros:** Caso ocorra uma falha técnica (API offline ou erro de script), um alerta é enviado automaticamente ao Telegram.

## 🛠️ Tecnologias Utilizadas

* **Python 3.11**
* **Pandas & Pandas-TA-Classic:** Processamento de dados e indicadores técnicos.
* **CoinGecko API:** Dados de mercado em tempo real.
* **GitHub Actions:** Automação e agendamento (Cron Job) 2x ao dia (07h e 12h BRT).
* **Telegram Bot API:** Notificações de relatórios e alertas de falha técnica.

## ⚙️ Configuração e Instalação

### 1. Requisitos
* Crie um bot no Telegram via `@BotFather` para obter seu `TELEGRAM_TOKEN`.
* Obtenha seu `TELEGRAM_CHAT_ID` (pessoal ou de grupo). IDs de grupo devem começar com `-100`.

### 2. Configuração do Repositório (GitHub Secrets)
Adicione as chaves em **Settings > Secrets and variables > Actions > New repository secret**:

| Secret | Descrição |
| :--- | :--- |
| `TELEGRAM_TOKEN` | Token de API fornecido pelo BotFather. |
| `TELEGRAM_CHAT_ID` | ID numérico da conversa ou grupo (ex: -100...). |

### 3. Execução Local
```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar o bot
python altcoin_bot.py