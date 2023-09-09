import logging
import re
from . import admins, stickers
from .strings import messages
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler, filters, MessageHandler, CommandHandler

# States
MENU_SELECT = 0
STICKER_BAN = 1
STICKER_UNBAN = 2
STICKER_SELECT = 3
ADMIN_SELECT = 4
ADMIN_ADD = 5
ADMIN_REMOVE = 6

logger = logging.getLogger(__name__)


def get_handler():
    return ConversationHandler(
        entry_points=[
            CommandHandler('start', start, filters=filters.ChatType.PRIVATE),
            CommandHandler('ban_sticker_pack', sticker_ban_query, filters=filters.ChatType.PRIVATE),
            CommandHandler('unban_sticker_pack', sticker_unban_query, filters=filters.ChatType.PRIVATE),
            CommandHandler('list_banned_sticker_packs', sticker_unban_query, filters=filters.ChatType.PRIVATE),
            CommandHandler('add_admin', admin_add_query, filters=filters.ChatType.PRIVATE),
            CommandHandler('remove_admin', admin_remove_query, filters=filters.ChatType.PRIVATE),
            CommandHandler('list_admins', admin_list, filters=filters.ChatType.PRIVATE),
            CommandHandler('cancel', cancel, filters=filters.ChatType.PRIVATE),
            CommandHandler('help', menu, filters=filters.ChatType.PRIVATE),
        ],

        states={
            STICKER_BAN: [
                CommandHandler('cancel', cancel),
                MessageHandler(filters.Sticker.ALL, sticker_ban)
            ],
            STICKER_UNBAN: [
                CommandHandler('cancel', cancel),
                MessageHandler(filters.Sticker.ALL | filters.TEXT, sticker_unban)
            ],
            ADMIN_ADD: [
                CommandHandler('cancel', cancel),
                MessageHandler(filters.TEXT, admin_add)
            ],
            ADMIN_REMOVE: [
                CommandHandler('cancel', cancel),
                MessageHandler(filters.TEXT, admin_remove)
            ]
        },

        fallbacks=[
            CommandHandler('cancel', cancel, filters=filters.ChatType.PRIVATE),
            CommandHandler('help', menu, filters=filters.ChatType.PRIVATE)
        ]
    )


def get_help_string():
    command_list = {
        'ban_sticker_pack': messages['ban_sticker_pack_desc'],
        'unban_sticker_pack': messages['unban_sticker_pack_desc'],
        'list_banned_sticker_packs': messages['list_banned_sticker_packs_desc'],
        'add_admin': messages['add_admin_desc'],
        'remove_admin': messages['remove_admin_desc'],
        'list_admins': messages['list_admins_desc'],
        'cancel': messages['cancel_desc'],
        'help': messages['help_desc'],
    }

    return '\n'.join([f'/{key} - {value}' for key, value in command_list.items()])


async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    if not admins.is_admin(user.username):
        await update.message.reply_text(messages["error_unauth"])
        return ConversationHandler.END

    await update.message.reply_text(messages["start_convo"] + "\n\n" + get_help_string())
    return ConversationHandler.END


async def menu(update: Update, context: CallbackContext):
    user = update.message.from_user
    if not admins.is_admin(user.username):
        await update.message.reply_text(messages["error_unauth"])
        return ConversationHandler.END

    await update.message.reply_text(messages["help"] + "\n\n" + get_help_string())
    return ConversationHandler.END


async def admin_add_query(update: Update, context: CallbackContext):
    await update.message.reply_text(messages["admin_add_which"])
    return ADMIN_ADD


async def admin_remove_query(update: Update, context: CallbackContext):
    await update.message.reply_text(messages["admin_remove_which"])
    return ADMIN_REMOVE


async def admin_add(update: Update, context: CallbackContext):
    if (update.message.forward_from):
        user = update.message.forward_from.username
    else:
        user = re.sub(r'^@?([^\s]+).*$', r'\1', update.message.text).lower()

    success = admins.add(user)
    if success:
        await update.message.reply_text(messages["admin_add_success"])
    else:
        await update.message.reply_text(messages["admin_add_fail"])

    return ConversationHandler.END


async def admin_remove(update: Update, context: CallbackContext):
    if (update.message.forward_from):
        user = update.message.forward_from.username
    else:
        user = re.sub(r'^@?([^\s]+).*$', r'\1', update.message.text).lower()

    if (user == update.message.from_user.username):
        await update.message.reply_text(messages["admin_remove_self"])
        return ConversationHandler.END
    elif (admins.is_owner(user)):
        await update.message.reply_text(messages["admin_remove_owner"])
        return ConversationHandler.END

    success = admins.remove(user)
    if success:
        await update.message.reply_text(messages["admin_remove_success"])
    else:
        await update.message.reply_text(messages["admin_remove_fail"])
    return ConversationHandler.END


async def admin_list(update: Update, context: CallbackContext):
    await update.message.reply_text(get_admin_list())
    return ConversationHandler.END


def get_admin_list():
    output = []
    for admin in admins.list_admins():
        if (admins.is_owner(admin)):
            admin = admin + " (Owner)"
        output.append(admin)

    if len(output) == 0:
        return messages["admin_list_none"]
    else:
        return messages["admin_list"] + "\n\n" + "\n".join(output)


async def sticker_ban_list(update: Update, context: CallbackContext):
    await update.message.reply_text(get_sticker_list())
    return ConversationHandler.END


def get_sticker_list():
    output = []
    for pack in stickers.list_packs():
        output.append(pack + "\n" + "https://t.me/addstickers/" + pack)

    if len(output) == 0:
        return messages["sticker_list_none"]
    else:
        return messages["sticker_list"] + "\n\n" + "\n\n".join(output)


async def sticker_ban_query(update: Update, context: CallbackContext):
    await update.message.reply_text(messages["sticker_ban_which"])
    return STICKER_BAN


async def sticker_unban_query(update: Update, context: CallbackContext):
    await update.message.reply_text(get_sticker_list() + "\n\n" + messages["sticker_unban_which"])
    return STICKER_UNBAN


async def sticker_ban(update: Update, context: CallbackContext):
    if update.message.sticker.set_name is None:
        await update.message.reply_text(messages["sticker_invalid"])
        return ConversationHandler.END

    success = stickers.ban(update.message.sticker.set_name)
    if success:
        await update.message.reply_text(messages["sticker_ban_success"])
    else:
        await update.message.reply_text(messages["sticker_ban_fail"])
    return ConversationHandler.END


async def sticker_unban(update: Update, context: CallbackContext):
    if update.message.sticker:
        if update.message.sticker.set_name is None:
            await update.message.reply_text(messages["sticker_invalid"])
            return ConversationHandler.END
        pack_name = update.message.sticker.set_name
    else:
        pack_name = update.message.text

    success = stickers.unban(pack_name)
    if success:
        await update.message.reply_text(messages["sticker_unban_success"])
    else:
        await update.message.reply_text(messages["sticker_unban_fail"])
    return ConversationHandler.END


async def cancel(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("User {} canceled the conversation.".format(user.username))
    await update.message.reply_text(messages['cancel_convo'], reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END
