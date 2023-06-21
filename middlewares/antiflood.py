from telebot.handler_backends import BaseMiddleware
from telebot import TeleBot
from telebot.handler_backends import CancelUpdate
from loader import bot
from bot_locale.translate import translate

class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, limit) -> None:
        self.last_time = {}
        self.limit = limit
        self.update_types = ['message']

    def pre_process(self, message, data):
        if not message.from_user.id in self.last_time:
            # User is not in a dict, so lets add and cancel this function
            self.last_time[message.from_user.id] = message.date
            return
        if message.date - self.last_time[message.from_user.id] < self.limit:
            # User is flooding
            bot.reply_to(
                message,
                translate(message.from_user.language_code, 'input_spam_detection')
            )
            return CancelUpdate()
        self.last_time[message.from_user.id] = message.date


    def post_process(self, message, data, exception):
        pass
