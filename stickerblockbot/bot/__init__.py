import logging
from . import messagehandlers, conversationhandlers, stickers, admins
from telegram import Update
from telegram.error import InvalidToken
from telegram.ext import Application, MessageHandler, filters, CallbackQueryHandler, CallbackContext
assert CallbackQueryHandler  # silence pyflakes

logger = logging.getLogger(__name__)
logging.getLogger('httpx').setLevel(logging.WARNING)


def start_bot(token):
    try:
        application = Application.builder().token(token).build()
    except InvalidToken:
        logger.error("The Telegram bot token was not accepted")
        raise BotTokenException("Invalid token")

    application.add_error_handler(error)

    banned_sticker_handler = MessageHandler(filters.Sticker.ALL & filters.ChatType.GROUPS, messagehandlers.banned_stickers)

    stickers.init()
    admins.init()

    application.add_handler(conversationhandlers.get_handler())
    application.add_handler(banned_sticker_handler)

    logger.info("Bot started")
    application.run_polling()


def error(update: Update, context: CallbackContext):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


class BotTokenException(Exception):
    pass
