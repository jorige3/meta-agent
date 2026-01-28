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
- `config/telegram.json` → real Telegram credentials (ignored by git)
- `config/telegram.example.json` → sample config
- `reports/` → daily prediction outputs
- `logs/` → runtime logs

---

## ▶️ Run Manually

```bash
source venv/bin/activate
python src/daily_predictor.py

