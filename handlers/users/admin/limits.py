from loader import bot, db, ROOT_DIR
from states.states import EditLimit
from bot_locale.translate import translate
from keyboards.inline.menu import AdminKeyboard, MenuKeyboard
from telebot.formatting import escape_markdown
import json
import os
from pathlib import Path
from datetime import datetime
from utils.misc.texts import Pluralize

callback_data_admin_limits = 'admin.params_limits'
callback_data_admin_edit_limit = 'admin.params_limits.edit_'

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data == callback_data_admin_limits, role=['admin'])
def admin_limits_list(call):
    """ Отображает панель управления лимитами
    """

    bot.delete_state(call.from_user.id)

    user = db.get_user(call.from_user.id)
    lang = user['language_code']
    config = db.get_config()

    dispute_deal_limit_plural = Pluralize.ru(
        config['time_limit_dispute'],
        ["минута","минуты","минут"]
    )
    time_limit_deals_plural = Pluralize.ru(
        config['time_limit_deals'],
        ["минута","минуты","минут"]
    )
    limit_deals_per_plural = Pluralize.ru(
        config['limit_deals_per'],
        ["сделка","сделки","сделок"]
    )

    limits_info = translate(lang, 'admin_limits_info').format(**{
        'limit_deals_per': config['limit_deals_per'],
        'limit_deals_per_plural': limit_deals_per_plural,
        'time_limit_deals': config['time_limit_deals'],
        'time_limit_deals_plural': time_limit_deals_plural,
        'dispute_deal_limit': config['time_limit_dispute'],
        'dispute_deal_limit_plural': dispute_deal_limit_plural,
    })
    string_edit_limit_deals = translate(lang, 'inline_params_limits_edit_deals')
    string_edit_limit_dispute_deals = translate(lang, 'inline_params_limits_edit_dispute_deals')
    string_inline_back_to = translate(lang, 'inline_back_to')

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=limits_info,
        reply_markup=MenuKeyboard.smart({
            string_edit_limit_deals: {'callback_data': (callback_data_admin_edit_limit+'deals_limit')},
            string_edit_limit_dispute_deals: {'callback_data': callback_data_admin_edit_limit+'dispute_deal'},
            string_inline_back_to: {'callback_data': 'admin.params'},
        })
    )

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_edit_limit), role=['admin'])
def admin_edit_limit(call):
    """ Редактирование лимита
    """
    user = db.get_user(call.from_user.id)
    limit_param = call.data.replace(callback_data_admin_edit_limit, "")
    key_string = 'admin_edit_limits_deals'

    if limit_param == 'dispute_deal':
        key_string = 'admin_edit_limits_dispute_deals'

    bot.set_state(call.from_user.id, EditLimit.A1)

    with bot.retrieve_data(call.from_user.id) as data:
        data['message_id'] = call.message.message_id
        data['param'] = limit_param

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=translate(user['language_code'], key_string),
        reply_markup=MenuKeyboard.back_to(user, key_string='inline_back_to', data=callback_data_admin_limits)
    )


@bot.message_handler(is_chat=False, state=EditLimit.A1, role=['admin'])
def edit_limit(message):
    user = db.get_user(message.from_user.id)

    with bot.retrieve_data(message.from_user.id) as data:
        if data['param'] == 'deals_limit':
            first, second = 1, 1
            try:
                first, second = float(message.text.split("-")[0]), float(message.text.split("-")[1])
            except Exception as e:
                print(e)

            db.update_config({'limit_deals_per': first, 'time_limit_deals': second})

        if data['param'] == 'dispute_deal':
            first = 1
            try:
                first = float(message.text)
            except Exception as e:
                print(e)

            db.update_config({'time_limit_dispute': first})

        try:
            bot.delete_message(
                chat_id=message.chat.id,
                message_id=data['message_id']
            )
        except Exception as e:
            pass

        key_string_back_to = translate(user['language_code'], 'inline_back_to')
        bot.send_message(
            chat_id=message.chat.id,
            text=translate(user['language_code'], 'admin_limit_success_edit'),
            reply_markup=MenuKeyboard.smart({
                key_string_back_to: {'callback_data': callback_data_admin_limits}
            })
        )

        bot.delete_state(message.from_user.id)
