# Meta-Agent (Consensus-based Daily Game Signal Engine)

This project acts as a **Meta-Agent**, orchestrating multiple underlying prediction engines to generate a consensus-based daily game signal. It combines insights from:
- **Game AI Engine:** Provides initial predictions.
- **Jodi Analyzer Pro v2:** Offers further analysis and predictions.

The Meta-Agent then processes these outputs to determine a consensus, generates comprehensive reports (PDF and CSV), and supports Telegram notifications for daily signals.

Currently configured for **Sridevi market**.

---

## 📁 Project Structure

- `agent.py` → The main Meta-Agent orchestrator script.
- `src/daily_predictor.py` → One of the underlying daily prediction engines.
- `tests/` → Contains unit tests for the project.
- `.env` → Stores sensitive credentials like Telegram API keys (ignored by git).
- `reports/` → Stores generated daily prediction reports (PDF and CSV).
- `logs/` → Stores runtime logs.
- `telegram_notifier.py` → Handles sending Telegram notifications.

---

## ▶️ Getting Started

### 1. Setup Virtual Environment and Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Telegram Notifications (Optional)

Create a `.env` file in the project root with your Telegram Bot Token and Chat ID:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

You can obtain your `TELEGRAM_BOT_TOKEN` from BotFather on Telegram. To get your `TELEGRAM_CHAT_ID`, you can send a message to your bot and then use a service like `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates` to find your chat ID.

### 3. Run the Meta-Agent

To run the Meta-Agent and generate daily signals, reports, and send Telegram notifications (if configured):

```bash
source venv/bin/activate
python agent.py
```

---

## ✅ Testing

To run the unit tests for the project:

```bash
source venv/bin/activate
pytest tests/
```