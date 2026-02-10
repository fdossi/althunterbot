# 🚀 Crypto Altcoin Hunter Bot

Um sistema automatizado em Python que realiza varredura diária no mercado de criptomoedas em busca de **altcoins com alto potencial de valorização** no curto prazo. O bot analisa dados técnicos, volume e métricas de mercado, enviando um relatório detalhado diretamente para o seu **Telegram**.

## 📊 Como o Bot Funciona

O script roda via **GitHub Actions** todos os dias e executa as seguintes etapas:

1.  **Filtro de Ativos:** Ignora stablecoins e foca nas 250 principais altcoins por volume.
2.  **Análise Técnica:** Calcula o **RSI (Índice de Força Relativa)** para identificar ativos que não estão sobrecomprados.
3.  **Métrica de Momentum:** Analisa a relação **Volume/Market Cap** para detectar interesse real de "baleias" e institucionais.
4.  **Verificação de Liquidez:** Filtra moedas com volume saudável para evitar *low-caps* extremamente arriscadas.
5.  **Relatório:** Seleciona as 10 melhores oportunidades e envia via Bot API do Telegram.

## 🛠️ Tecnologias Utilizadas

* **Python 3.9+**
* **Pandas & Pandas-TA:** Para processamento de dados e indicadores técnicos.
* **CoinGecko API:** Fonte de dados de mercado em tempo real.
* **GitHub Actions:** Automação e agendamento (Cron Job).
* **Telegram Bot API:** Interface de saída para os relatórios.

## ⚙️ Configuração e Instalação

### 1. Requisitos
Crie um bot no Telegram através do `@BotFather` e obtenha seu `TOKEN` e seu `CHAT_ID`.

### 2. Configuração do Repositório
Para que o bot funcione automaticamente, adicione as seguintes chaves em **Settings > Secrets and variables > Actions > New repository secret**:

| Secret | Descrição |
| :--- | :--- |
| `TELEGRAM_TOKEN` | O token de API fornecido pelo BotFather. |
| `TELEGRAM_CHAT_ID` | O ID numérico da sua conversa com o bot. |

### 3. Execução Local
Se desejar rodar o script manualmente em sua máquina:
```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente (ou editar temporariamente no código)
export TELEGRAM_TOKEN='seu_token_aqui'
export TELEGRAM_CHAT_ID='seu_id_aqui'

# Rodar o bot
python altcoin_bot.py