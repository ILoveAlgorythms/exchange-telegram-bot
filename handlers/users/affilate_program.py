from loader import bot, db, cache, me, config
from bot_locale.translate import _
from keyboards.inline.menu import MenuKeyboard
import json

callback_data_affilate_program = 'bot.user.affilate_program'

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data == callback_data_affilate_program)
def affilate_program(call):
    """ Партнёрская программа
    """
    # TASK: вынести в глобальный middleware все базовые надстройки пользователя и передавать в объекте закэшированный user
    bot_cfg = db.get_config()

    user = db.get_user(call.from_user.id)
    affilate_id = f"{config['affilate']['prefix']}{user['uid']}"

    refferal_lines = db.get_refferal_lines(user['id'])
    refferer = _(user['language_code'], 'no_refferer')

    if user['refferer_id'] > 0:
        refferer = db.get_user(user['refferer_id'], name_id="id")
        refferer = refferer['username'] # sorry

    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.from_user.id,
        text=_(
            user['language_code'],
            'affilate_user_text'
        ).format(**{
            'affiliate_invite_code':          affilate_id,
            'user_refferer':                  refferer,
            'username':                       me.username,
            'summary_amount':                 0,
            'summary_amount_current_mounth':  0,
            'summary_amount_previous_mounth': 0,
            'summary_user_count_first_line':  refferal_lines['first_line'],
            'summary_amount_first_line':      0,
            'summary_user_count_second_line': refferal_lines['second_line'],
            'summary_amount_seconds_line':    0,
            'base_asset':                     bot_cfg['affilate_base_asset']
        }),
        reply_markup=MenuKeyboard.smart({
            'Withdrawal': {
                'callback_data': 'bot.back_to_main_menu'
            },
            'Back to': {
                'callback_data': 'bot.back_to_main_menu'
            }
        })
    )
