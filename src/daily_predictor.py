import os
import sys
from dotenv import load_dotenv

# Add path to jodi-analyzer-pro-v2 backtest engine
sys.path.append("/home/kishore/sridevi/jodi-analyzer-pro-v2/src/backtest")
import engine_v5  # import your v5 engine

load_dotenv()

# Paths
DATA_FILE = "/home/kishore/sridevi/jodi-analyzer-pro-v2/data/input/sridevi_data.csv"
META_REPORT_PATH = "reports/daily_prediction_report.csv"
RAN_TODAY_FILE = "logs/ran_today.txt"

# Telegram Configuration
TELEGRAM_ENABLED = bool(
    os.getenv("TELEGRAM_BOT_TOKEN") and
    os.getenv("TELEGRAM_CHAT_ID")
)

# Optional: Telegram notifier import
try:
    from telegram_notifier import send_telegram_message
except ImportError:
    pass

def confidence_label(any_hit_rate):
    if any_hit_rate >= 60:
        return "🔥 STRONG DAY"
    elif any_hit_rate >= 45:
        return "✅ NORMAL DAY"
    else:
        return "⚠️ RISK DAY"

def get_today_digits(report_df):
    last_played = report_df[report_df["played"]].iloc[-1]
    digits = last_played["digits_to_play"]
    return digits

def format_daily_message(digits, any_hit_rate):
    label = confidence_label(any_hit_rate)

    msg = f"""
🎯 DAILY GAME SIGNAL

Digits to Play: {' '.join(map(str, digits))}
Confidence    : {label}

Rules:
• Open → Strong
• Close → Medium
• Single digit focus
• No chasing

🧠 Engine: Daily + Seven-Day v5
"""
    return msg.strip()

def already_ran_today():
    """Check if the script has already run today."""
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    if os.path.exists(RAN_TODAY_FILE):
        with open(RAN_TODAY_FILE, 'r') as f:
            last_ran = f.read().strip()
        return last_ran == today
    return False

def mark_ran_today():
    """Mark that the script ran today."""
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(os.path.dirname(RAN_TODAY_FILE), exist_ok=True)
    with open(RAN_TODAY_FILE, 'w') as f:
        f.write(today)

def run_daily_prediction():
    """
    Run daily prediction using v5 engine and save the report.
    """
    # Run v5 engine backtest
    report_df = engine_v5.backtest_v5(data_file=DATA_FILE)

    # Get the last day played
    last_played = report_df[report_df['played']].iloc[-1]

    digits_today = last_played['digits_to_play']

    # Save meta-agent report
    os.makedirs(os.path.dirname(META_REPORT_PATH), exist_ok=True)
    report_df.to_csv(META_REPORT_PATH, index=False)

    print(f"✅ Daily prediction report saved: {META_REPORT_PATH}")
    print(f"🎯 Today’s recommended digits: {digits_today}")


    return report_df, digits_today

if __name__ == "__main__":
    if already_ran_today():
        print("⚠️ Daily signal already sent. Skipping.")
        sys.exit(0)

    report_df, _ = run_daily_prediction()
    
    today_digits = get_today_digits(report_df)

    # engine v5 known performance
    any_hit_rate = 61.24  # frozen from backtest

    message = format_daily_message(today_digits, any_hit_rate)

    print(message)
    
    if TELEGRAM_ENABLED:
        send_telegram_message(message)
        print("✅ Telegram notification sent")
    
    mark_ran_today()
    print("✅ Daily signal completed")
