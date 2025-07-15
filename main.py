import os
import logging
import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Thiết lập logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot LBX đã hoạt động! Gõ /btc để xem giá BTC hiện tại hoặc /status để kiểm tra.")

# Lệnh /status
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Bot đang hoạt động bình thường.")

# Lệnh /btc để lấy giá BTC từ Binance
async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        r.raise_for_status()
        price = float(r.json()['price'])
        await update.message.reply_text(f"💰 Giá BTC hiện tại là: ${price:,.2f}")
    except Exception as e:
        logger.error(f"Lỗi lấy giá BTC: {e}")
        await update.message.reply_text("⚠️ Không lấy được giá BTC từ Binance.")

# Hàm khởi động bot
async def main():
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        raise ValueError("⚠️ Bạn cần thiết lập TELEGRAM_TOKEN trong biến môi trường!")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("btc", btc))

    logger.info("🚀 Bot đang chạy...")
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
