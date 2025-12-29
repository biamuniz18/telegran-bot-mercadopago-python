import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
PAYMENT_LINK = os.getenv("PAYMENT_LINK")
CHANNEL_LINK = os.getenv("CHANNEL_LINK")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💳 Pagar R$ 10,90", url=PAYMENT_LINK)],
        [InlineKeyboardButton("✅ Já paguei", callback_data="paid")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🔒 Conteúdo exclusivo\n\nClique abaixo para pagar:",
        reply_markup=reply_markup
    )


async def paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        f"✅ Pagamento confirmado!\n\nAcesse o canal:\n{CHANNEL_LINK}"
    )


def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(paid, pattern="paid"))

    application.run_polling()


if __name__ == "__main__":
    main()
