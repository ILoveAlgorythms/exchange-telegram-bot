from telebot.custom_filters import SimpleCustomFilter
from telebot.types import Message, CallbackQuery
from bot_locale.translate import translate
from keyboards.inline.menu import MenuKeyboard
from loader import bot, db

class IsAdmin(SimpleCustomFilter):
    """Проверяет является ли пользователь администратором"""
    key='is_admin'
    @staticmethod
    def check(message: Message):
        telegram_id = message.from_user.id
        user = db.get_user(message.from_user.id)

        if user and user['is_admin']:
            return True

        if type(message) == Message:
            bot.send_message(message.from_user.id, "Access denied")

        return False

class IsAmount(SimpleCustomFilter):
    """ Проверяет является ли введённый текст
        числом или числом с плавающей точкой
    """
    key='is_amount'
    @staticmethod
    def check(message: Message):
        try:
            amount = float(message.text)
            return True
        except Exception as e:
            return False

class IsChat(SimpleCustomFilter):
    """Проверяет находится ли бот в чате"""
    key='is_chat'
    @staticmethod
    def check(message: Message):
        if type(message) == CallbackQuery:
            message = message.message
        return message.chat.type in ['group', 'supergroup']

# TASK: переписать под AdvancedCustomFilter
#       добавить тип отображаемого сообщения
#       (callback или message)
class IsCancelAction(SimpleCustomFilter):
    """ Было ли отменено действие?
        Очищает любое состояние
        (для reply-кнопок ...Отмена...)
    """
    key='is_cancel_action'
    @staticmethod
    def check(message: Message):
        telegram_id = message.from_user.id
        user = db.get_user(message.from_user.id)
        reply_cancel = translate(user['language_code'], 'reply_exchange_cancel')

        if user and message.text in [reply_cancel]:
            # Если есть совпадение, удаляем состояние
            bot.delete_state(telegram_id)

            mid_cancel_action = bot.send_message(
                message.from_user.id,
                translate(user['language_code'], 'bot_reply_cancel_action'),
                reply_markup=MenuKeyboard.remove_reply()
            )

            bot.send_message(
                chat_id=telegram_id,
                text=translate(user['language_code'], 'start_text'),
                reply_markup=MenuKeyboard.home(user)
            )

            return True

        return False
