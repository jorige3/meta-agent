# Meta-Agent (Daily Game Signal Engine)

This project runs a **daily prediction engine** using:
- Daily digit logic
- Seven-day weighted engine (v5)
- Backtested strategy
- Telegram notification support

Currently configured for **Sridevi market**.

---

## 📁 Project Structure

- `src/daily_predictor.py` → main daily engine
- `.env` → Telegram credentials (ignored by git)
- `reports/` → daily prediction outputs
- `logs/` → runtime logs

---

## ▶️ Run Manually

```bash
source venv/bin/activate
python src/daily_predictor.py

### Telegram Configuration

Create a `.env` file:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here


---

## ✅ STEP 3: Verify cleanup

Run these commands:

```bash
git grep -i telegram.json
