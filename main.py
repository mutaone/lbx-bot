import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot LBX đã khởi động!")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📈 Bot vẫn đang hoạt động.")

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        price = float(res.json()['price'])
        await update.message.reply_text(f"💰 BTC hiện tại: ${price:,.2f}")
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("⚠️ Không lấy được giá BTC.")

async def main():
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        raise RuntimeError("⚠️ Chưa có TELEGRAM_TOKEN trong biến môi trường.")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("btc", btc))

    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
