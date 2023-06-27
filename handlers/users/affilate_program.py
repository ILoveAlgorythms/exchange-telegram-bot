from loader import bot, db, cache, me
from bot_locale.translate import _
from keyboards.inline.menu import MenuKeyboard
import json

callback_data_affilate_program = 'bot.user.affilate_program'

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data == callback_data_affilate_program)
def affilate_program(call):
    """ Партнёрская программа
    """
    user = db.get_user(call.from_user.id)

    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.from_user.id,
        # text=_(user['language_code'], 'user_support_select_reason'),
        text="💎 *Партнёрская программа*\n\nВаш ID: {affiliate_invite_code}\nВас пригласил: {user_refferer}\nВаша партнерская ссылка: `https://t.me/{username}?start={affiliate_invite_code}`\nВсего заработано: {summary_amount} USDT\n\nОборот реферальной структуры (2 линии + свой)\nТекущий месяц: {summary_amount_current_mounth} USDT\n\nПрошедший месяц: {summary_amount_previous_mounth} USDT\n\n1 линия. Кол-во человек: {summary_user_count_first_line}\nОборот: {summary_amount_first_line} USD\n2 линия. Кол-во человек: {summary_user_count_second_line}\nОборот: {summary_amount_seconds_line} USD".format(**{
            "affiliate_invite_code": "GW-000000",
            "user_refferer": "-",
            "username": "GreenWalletExchange",
            "summary_amount": 10.2,
            "summary_amount_current_mounth": 10.2,
            "summary_amount_previous_mounth": 0,
            "summary_amount_first_line": 7,
            "summary_amount_seconds_line": 3.2,
            "summary_user_count_first_line": 2,
            "summary_user_count_second_line": 1,
        }),
        # reply_markup=,
        reply_markup=MenuKeyboard.smart({
            'Withdrawal': {
                'callback_data': 'bot.back_to_main_menu'
            },
            'Back to': {
                'callback_data': 'bot.back_to_main_menu'
            }
        })
    )
