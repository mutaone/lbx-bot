import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Lấy token từ biến môi trường
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")  # Nếu cần gửi tín hiệu chủ động

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot LBX đã hoạt động ✅")

# Lệnh /status
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Đây là ví dụ đơn giản, mày có thể chèn logic lấy tín hiệu real ở đây
    await update.message.reply_text("⚡ LBX hiện đang theo dõi top 50 coin.")

# Hàm chạy bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.run_polling()

if __name__ == "__main__":
    main()
