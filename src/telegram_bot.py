import logging

import requests
from telegram import ReplyKeyboardRemove
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)

EMAIL = range(1)


def invite(update, context):
    update.message.reply_text("Digite o e-mail de quem você quer convidar.")

    return EMAIL


def email(update, context):
    email = update.message.text
    user = update.message.from_user
    logger.info(f"User {user.first_name} invited {email}")

    requests.

    reply = "E-mail enviado!"
    update.message.reply_text(reply)

    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info(f"User {user.first_name} canceled the operation.")

    update.message.reply_text("Operação cancelada!", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning(f"Update {update} caused error {context.error}")


def main():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("convidar", invite)],
        states={EMAIL: [MessageHandler(Filters.text, email)]},
        fallbacks=[CommandHandler("cancelar", cancel)],
    )

    bot_token = input("Insert bot token: ")
    updater = Updater(bot_token, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(conv_handler)
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
