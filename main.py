import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8857879696:AAECfRGeDHRjbCE1lZYiSD8TuBK832MqfwA"
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(list(users), f)

users = load_users()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in users:
        users.add(uid)
        save_users(users)
    await update.message.reply_text("👋 你好！欢迎关注，发送 /help 查看所有指令。")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📊 当前累计用户数：{len(users)} 人")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = " ".join(context.args)
    if not msg:
        await update.message.reply_text("⚠️ 请输入群发内容，例如：/broadcast 最新剧集已上线！")
        return

    succ, fail = 0, 0
    await update.message.reply_text(f"🚀 开始向 {len(users)} 位用户群发...")
    for user_id in list(users):
        try:
            await context.bot.send_message(chat_id=user_id, text=msg)
            succ += 1
        except Exception:
            fail += 1
    await update.message.reply_text(f"✅ 群发完成！\n成功：{succ} 人\n失败/拉黑：{fail} 人")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📖 指令菜单：\n/start - 启动\n/stats - 用户统计\n/broadcast [内容] - 全员群发")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("help", help_command))
    print("Bot started...")
    app.run_polling()
