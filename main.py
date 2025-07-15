import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Thiết lập logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 LBX Bot hoạt động! Dùng /btc để xem giá BTC.")

# Lệnh /btc
async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        price = float(res.json()['price'])
        await update.message.reply_text(f"💰 Giá BTC hiện tại: ${price:,.2f}")
    except Exception as e:
        logger.error(f"Lỗi lấy giá: {e}")
        await update.message.reply_text("⚠️ Không lấy được giá BTC.")

# Lệnh /status
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot đang online.")

# Khởi chạy
if __name__ == '__main__':
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        raise RuntimeError("⚠️ Thiếu TELEGRAM_TOKEN trong biến môi trường!")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("btc", btc))
    app.add_handler(CommandHandler("status", status))

    app.run_polling()
