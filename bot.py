import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask
import threading

TOKEN = os.getenv("BOT_TOKEN")

PAYMENT_LINK = "SEU_LINK_MERCADO_PAGO"
CHANNEL_LINK = "SEU_LINK_CANAL_PRIVADO"

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot ativo"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💳 Pagar R$ 10,90", url=PAYMENT_LINK)],
        [InlineKeyboardButton("✅ Já paguei", callback_data="paid")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🔥 Bem-vindo ao Acesso VIP da Bia\n\n"
        "Para acessar o conteúdo exclusivo, clique abaixo:",
        reply_markup=reply_markup
    )

async def paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "✅ Pagamento confirmado!\n\n"
        f"Acesse o canal:\n{CHANNEL_LINK}"
    )

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(paid, pattern="paid"))

    threading.Thread(target=run_flask).start()
    application.run_polling()

if __name__ == "__main__":
    main()
