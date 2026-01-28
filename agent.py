#!/usr/bin/env python3
import subprocess
import sys
import os
import csv
from datetime import datetime
from fpdf import FPDF, XPos, YPos
import json # Import json for loading telegram config
from telegram_notifier import notify_meta_agent_results # Import telegram notifier
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ----------------------------
# TELEGRAM CONFIGURATION
# ----------------------------
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

# ----------------------------
# CONFIGURATION
# ----------------------------
TODAY = datetime.now().strftime("%Y-%m-%d")

# Paths to projects
GAME_AI_PATH = "/home/kishore/sridevi/game_ai"
JODI_PATH = "/home/kishore/sridevi/jodi-analyzer-pro-v2"

# Commands
GAME_AI_CMD = "/home/kishore/sridevi/game_ai/venv/bin/python run_automation.py"
JODI_CMD = "/home/kishore/sridevi/jodi-analyzer-pro-v2/venv/bin/python pro_agent.py"

# Output files
PDF_REPORT = "meta_report.pdf"
CSV_REPORT = "meta_report.csv"

# ----------------------------
# HELPER FUNCTIONS
# ----------------------------
def run_command(cmd, cwd):
    """Run a subprocess command and return stdout."""
    try:
        result = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running {cmd}: {e}")
        print(e.stdout)
        print(e.stderr)
        return ""

def parse_game_ai(output):
    """Extract digits and jodis from game-ai output."""
    digits, jodis = [], []
    for line in output.splitlines():
        if "Final Digits :" in line:
            digits = line.split(":")[1].strip().strip("[]").replace("'", "").split(", ")
        elif "Safe Jodis   :" in line:
            jodis = line.split(":")[1].strip().strip("[]").replace("'", "").split(", ")
    return digits, jodis

def parse_jodi(output):
    """Extract predictions from jodi-analyzer-pro-v2 output."""
    digits, jodis = [], []
    for line in output.splitlines():
        if "Hot Digit (Jodi)" in line:
            digits.append(line.split(":")[1].strip())
        elif "Support Jodis" in line:
            jodis_line = line.split(":")[1].strip()
            jodis.extend([x.strip() for x in jodis_line.split(",")])
    return digits, jodis

def generate_pdf(report):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=14)
    pdf.cell(0, 10, f"Meta-Agent Consensus Report - {TODAY}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.set_font("Helvetica", size=12)
    pdf.ln(5)
    pdf.cell(0, 10, f"Agreement Level: {report['agreement']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Common Digits: {', '.join(report['common_digits']) or 'None'}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Common Jodis: {', '.join(report['common_jodis']) or 'None'}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Final Note: {'High confidence!' if report['agreement']=='HIGH' else 'Use with caution!'}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.output(PDF_REPORT)
    print(f"✅ PDF saved: {PDF_REPORT}")

def generate_csv(report):
    with open(CSV_REPORT, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Agreement", "Common Digits", "Common Jodis", "Note"])
        writer.writerow([
            TODAY,
            report["agreement"],
            ";".join(report["common_digits"]),
            ";".join(report["common_jodis"]),
            "High confidence!" if report['agreement']=='HIGH' else "Use with caution!"
        ])
    print(f"✅ CSV saved: {CSV_REPORT}")

def compute_agreement(d1, j1, d2, j2):
    """Compute simple agreement level between two sets."""
    common_digits = list(set(d1) & set(d2))
    common_jodis = list(set(j1) & set(j2))
    level = "HIGH" if len(common_digits) >= 2 or len(common_jodis) >= 3 else "MEDIUM" if common_digits or common_jodis else "LOW"
    return level, common_digits, common_jodis

# ----------------------------
# MAIN EXECUTION
# ----------------------------
if __name__ == "__main__":
    print(f"Running meta-agent for {TODAY}")

    # ======================
    # Load Telegram Configuration
    # ======================
    telegram_bot_token = None
    telegram_chat_id = None
    try:
        with open("config/telegram.json", "r") as f:
            telegram_config = json.load(f)
            telegram_bot_token = telegram_config.get("bot_token")
            telegram_chat_id = telegram_config.get("chat_id")
    except FileNotFoundError:
        print("Telegram config file (config/telegram.json) not found. Skipping Telegram notifications.")
    except json.JSONDecodeError:
        print("Error decoding config/telegram.json. Skipping Telegram notifications.")
    except Exception as e:
        print(f"An unexpected error occurred while loading Telegram config: {e}. Skipping Telegram notifications.")

    # Run game-ai
    game_output = run_command(GAME_AI_CMD, GAME_AI_PATH)
    game_digits, game_jodis = parse_game_ai(game_output)

    # Run jodi-analyzer-pro-v2
    jodi_output = run_command(JODI_CMD, JODI_PATH)
    jodi_digits, jodi_jodis = parse_jodi(jodi_output)

    # Compute consensus
    agreement, common_digits, common_jodis = compute_agreement(game_digits, game_jodis, jodi_digits, jodi_jodis)
    report = {
        "agreement": agreement,
        "common_digits": common_digits,
        "common_jodis": common_jodis
    }

    # Generate reports
    generate_pdf(report)
    generate_csv(report)

    # Print summary
    print("=== CONSENSUS REPORT ===")
    print(f"Agreement Level: {agreement}")
    print(f"Common Digits: {common_digits}")
    print(f"Common Jodis: {common_jodis}")
    print(f"Final Note: {'High confidence!' if agreement=='HIGH' else 'Use with caution!'}")

    # ======================
    # SEND TELEGRAM NOTIFICATION
    # ======================
    if telegram_bot_token and telegram_chat_id:
        print("\nSending Telegram notification...")
        message_text = (
            f"*Meta-Agent Consensus Report - {TODAY}*\n\n"
            f"Agreement Level: *{agreement}*\n"
            f"Common Digits: `{', '.join(common_digits) or 'None'}`\n"
            f"Common Jodis: `{', '.join(common_jodis) or 'None'}`\n"
            f"Final Note: {'High confidence!' if agreement=='HIGH' else 'Use with caution!'}"
        )
        notify_meta_agent_results(telegram_bot_token, telegram_chat_id, message_text)
    else:
        print("\nSkipping Telegram notification: Bot token or chat ID not configured.")
