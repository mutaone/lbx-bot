import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot LBX đã hoạt động! Gõ /btc để xem giá BTC hoặc /status.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot đang chạy bình thường.")

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        res.raise_for_status()
        price = float(res.json()["price"])
        await update.message.reply_text(f"💰 Giá BTC hiện tại: ${price:,.2f}")
    except Exception as e:
        logger.error(f"Lỗi lấy giá BTC: {e}")
        await update.message.reply_text("⚠️ Không lấy được giá BTC!")

async def main():
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        raise ValueError("❌ TELEGRAM_TOKEN chưa được set trong biến môi trường.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("btc", btc))

    logger.info("🚀 Bot đã khởi động...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
