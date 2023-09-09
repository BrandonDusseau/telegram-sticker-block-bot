import logging
from . import stickers
from datetime import datetime, timezone
from telegram import Update
from telegram.ext import CallbackContext
from telegram.error import BadRequest

logger = logging.getLogger(__name__)


async def banned_stickers(update: Update, context: CallbackContext):
    if is_expired(update.message.date, 300):
        return

    if update.message.sticker.set_name is None:
        return

    if stickers.is_banned(update.message.sticker.set_name):
        update.message.delete

        try:
            await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
            await context.bot.send_message(chat_id=update.message.chat_id, text='@' + update.message.from_user.username
                             + ': that sticker pack is not allowed in this group.')
        except BadRequest:
            logger.warning("Unable to delete banned sticker from group '" + update.message.chat.title
                           + "'. Is the bot an admin?")


def is_expired(time, expiry):
    if (int((datetime.now(timezone.utc) - time).total_seconds()) >= expiry):
        return True

    return False
