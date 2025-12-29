import os
import threading
from flask import Flask

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# =========================
# ENV VARS (Render)
# =========================
TOKEN = os.getenv("BOT_TOKEN", "").strip()
PAYMENT_LINK = os.getenv("PAYMENT_LINK", "").strip()
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "").strip()

# Render define PORT automaticamente em Web Service
PORT = int(os.getenv("PORT", "8080"))

# =========================
# FLASK (healthcheck)
# =========================
app = Flask(__name__)

@app.get("/")
def home():
    return "Bot ativo ✅", 200

def run_flask():
    app.run(host="0.0.0.0", port=PORT)

# =========================
# TELEGRAM BOT
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Se faltar variável, avisa no Telegram
    if not TOKEN:
        await update.message.reply_text("❌ BOT_TOKEN não está configurado no Render.")
        return
    if not PAYMENT_LINK:
        await update.message.reply_text("❌ PAYMENT_LINK não está configurado no Render.")
        return
    if not CHANNEL_LINK:
        await update.message.reply_text("❌ CHANNEL_LINK não está configurado no Render.")
        return

    keyboard = [
        [InlineKeyboardButton("💳 Pagar", url=PAYMENT_LINK)],
        [InlineKeyboardButton("✅ Já paguei", callback_data="paid")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Para acessar o conteúdo:\n\n"
        "1) Clique em 💳 Pagar\n"
        "2) Depois clique em ✅ Já paguei",
        reply_markup=reply_markup
    )

async def paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not CHANNEL_LINK:
        await query.message.reply_text("❌ CHANNEL_LINK não está configurado no Render.")
        return

    await query.message.reply_text(
        "✅ Pagamento confirmado!\n\n"
        f"Acesse o canal:\n{CHANNEL_LINK}"
    )

def main():
    # Se TOKEN estiver vazio, derruba o deploy com erro claro
    if not TOKEN:
        raise ValueError("BOT_TOKEN não definido. Configure em Render > Environment Variables.")

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(paid, pattern="^paid$"))

    # Sobe o Flask (pra Render ver que tá vivo)
    threading.Thread(target=run_flask, daemon=True).start()

    # Roda o bot
    application.run_polling()

if __name__ == "__main__":
    main()
