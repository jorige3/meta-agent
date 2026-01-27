import logging
import asyncio
from telegram import Bot

async def send_telegram_message(bot_token, chat_id, message):
    """
    Sends a message to the configured Telegram chat.
    """
    logging.info("Attempting to send Telegram notification...")

    try:
        if not bot_token or bot_token == "YOUR_TELEGRAM_BOT_TOKEN":
            logging.error("Telegram bot token is not configured.")
            return False

        if not chat_id or chat_id == "YOUR_TELEGRAM_CHAT_ID":
            logging.error("Telegram chat ID is not configured.")
            return False

        bot = Bot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
        logging.info("Telegram notification sent successfully.")
        return True

    except Exception as e:
        logging.error(f"Failed to send Telegram notification: {e}", exc_info=True)
        return False

def notify_meta_agent_results(bot_token, chat_id, message_text):
    """
    Sends a formatted message for Meta Agent results via Telegram.
    """
    return asyncio.run(send_telegram_message(bot_token, chat_id, message_text))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    # Example usage for testing
    test_bot_token = "YOUR_TELEGRAM_BOT_TOKEN"
    test_chat_id = "YOUR_TELEGRAM_CHAT_ID"
    test_message = "*Meta Agent Report*\n\nMeta-analysis completed successfully. Check the latest reports."
    notify_meta_agent_results(test_bot_token, test_chat_id, test_message)