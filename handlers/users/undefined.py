from loader import bot, db
from bot_locale.translate import _

@bot.message_handler(is_chat=False)
def undefined(message):
    """ Возвращает сообщение о неизвестной команде
    """
    user = db.get_user(message.from_user.id)
    bot.send_message(
        message.from_user.id,
        _(user['language_code'], 'input_conext_not_found')
    )
