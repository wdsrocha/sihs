import logging

from email_sender import EmailSender

from telegram import ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

EMAIL = range(1)

EmailSender()


def invite(update, context):
    update.message.reply_text("Digite o e-mail de quem deve ter o acesso.")

    return EMAIL


def email(update, context):
    email = update.message.text
    user = update.message.from_user

    reply = "E-mail inválido"
    if email == "f":
        reply = "Show!"
    update.message.reply_text(reply)

    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info(f"User {user.first_name} canceled the operation.")

    update.message.reply_text("Operação cancelada!", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning(f"Update {update} caused error {context.error}.")


def main():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("convidar", invite)],
        states={EMAIL: [MessageHandler(Filters.text, email)]},
        fallbacks=[CommandHandler("cancelar", cancel)],
    )

    updater = Updater(input(), use_context=True)

    dp = updater.dispatcher
    dp.add_handler(conv_handler)
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
