import json
from loader import bot, db, cache
from utils.misc.data import binance_p2p_arithmetic_mean_data, binance_get_price_pair
from states.states import SupportState
from bot_locale.translate import translate
from keyboards.inline.menu import MenuKeyboard

callback_data_create_ticket = 'bot.support.create'
callback_data_accept = 'bot.support.create.accept'
cache_waiting_create_support = '{0}_support_locked_time'

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data == 'bot.support.create')
def state_a0(call):
    """ Выбор причины обращения
    """
    user = db.get_user(call.from_user.id)
    reasons = translate(user['language_code'], 'list_support_request_reasons')
    is_lock_string = cache_waiting_create_support.format(user['id'])
    is_lock = cache.get(is_lock_string)

    if is_lock:
        bot.answer_callback_query(
            call.id,
            translate(user['language_code'], 'exceed_limit_ticket'),
            show_alert=True
        )
        return

    if user['is_banned'] == 1:
        bot.send_message(
            chat_id=call.from_user.id,
            text=translate(user['language_code'], 'user_is_banned')
        )
        return

    bot.delete_message(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
    )

    bot.send_message(
        chat_id=call.from_user.id,
        text=translate(user['language_code'], 'user_support_select_reason'),
        reply_markup=MenuKeyboard.reply_keyboard_parse(reasons)
    )

    bot.set_state(call.from_user.id, SupportState.A1)

@bot.message_handler(is_chat=False, state=SupportState.A1, is_cancel_action=False)
def state_a1(message):
    user = db.get_user(message.from_user.id)

    reason = message.text[0:128]

    with bot.retrieve_data(message.from_user.id) as data:
        data['reason'] = reason

    bot.send_message(
        chat_id=message.from_user.id,
        text=translate(user['language_code'], 'user_support_input_message'),
        reply_markup=MenuKeyboard.remove_reply()
    )
    bot.set_state(message.from_user.id, SupportState.A2)

@bot.message_handler(is_chat=False, state=SupportState.A2, is_cancel_action=False)
def state_a2(message):
    user = db.get_user(message.from_user.id)
    text = message.text[0:1024]

    with bot.retrieve_data(message.from_user.id) as data:
        data['message'] = text

        bot.send_message(
            chat_id=message.from_user.id,
            text=translate(
                user['language_code'],
                'user_support_finally_ticket'
            ).format(
                data['reason'],
                data['message'],
            ),
            reply_markup=MenuKeyboard.ticket_create_or_decline(user)
        )

    bot.set_state(message.from_user.id, SupportState.A3)

@bot.callback_query_handler(is_chat=False, state=SupportState.A3, func=lambda call: call.data.startswith(callback_data_accept))
def state_a3(call):
    user = db.get_user(call.from_user.id)
    config = db.get_config()

    if user['is_banned'] == 1:
        bot.answer_callback_query(
            call.id,
            translate(user['language_code'], 'user_is_banned')
        )
        return

    with bot.retrieve_data(call.from_user.id) as data:
        new_ticket = db.create_dialog(user['id'], title=data['reason'])
        is_lock_string = cache_waiting_create_support.format(user['id'])

        # добавляем в кэш запись о блоке на 5 минут
        cache.set(is_lock_string, user['id'])
        cache.expire(is_lock_string, 300)

        new_message = db.create_message(user['id'], new_ticket, text=data['message'])

        bot.edit_message_text(
            message_id=call.message.message_id,
            chat_id=call.from_user.id,
            text=translate(
                user['language_code'],
                'user_support_ticket_created'
            ).format(
                new_ticket
            ),
            reply_markup=MenuKeyboard.back_to(user)
        )

        if config['notifications_support_chat_id'] is not None:
            try:
                bot.send_message(
                    chat_id=config['notifications_support_chat_id'],
                    text=translate(
                        user['language_code'],
                        'user_support_ticket_created_notification'
                    ).format(
                        new_ticket,
                        data['reason'],
                        data['message'],
                    ),
                    reply_markup=MenuKeyboard.notification_ticket(
                        user,
                        new_ticket
                    )
                )
            except Exceptin as e:
                print(e)

    bot.delete_state(call.from_user.id)
