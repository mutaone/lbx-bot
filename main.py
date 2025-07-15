import os
import logging
import asyncio
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Command: /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot LBX đã hoạt động! Gõ /btc hoặc /status để tiếp tục.")

# Command: /status
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Bot hoạt động ổn định.")

# Command: /btc
async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        response.raise_for_status()
        price = float(response.json()["price"])
        await update.message.reply_text(f"💰 Giá BTC hiện tại: ${price:,.2f}")
    except Exception as e:
        logger.error(f"Lỗi lấy giá BTC: {e}")
        await update.message.reply_text("⚠️ Không lấy được giá BTC.")

# Async entry point
async def main():
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        raise RuntimeError("❌ Thiếu TELEGRAM_TOKEN trong biến môi trường!")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("btc", btc))

    logger.info("🚀 Bot đã sẵn sàng.")
    await app.run_polling()

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
