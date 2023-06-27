from utils.misc.data import (
    binance_p2p_arithmetic_mean_data,
    binance_get_price_pair,
    cryptoexchange_parse_rate
)
from utils.message_templates import get_admin_deal_text, get_requisites_text
from utils.misc.exchange import add_spread, calculate_amount
from utils.misc.accounts import extract_last_use_account, get_payment_account
from utils.misc.restrictions import Restriction
from states.states import ExchageState, UserDeal
from keyboards.inline.menu import MenuKeyboard
from telebot.formatting import escape_markdown
from bot_locale.translate import translate
from loader import bot, db, config, cache
from datetime import datetime, timedelta
import json

callback_data_select_pair = 'bot.set.exchage_select_pair_'
callback_data_select_from_bank = 'bot.set.exchage_select_from_bank_'
callback_data_select_to_bank = 'bot.set.exchage_select_to_bank_'
callback_data_input_amount = 'bot.set.exchage_input_amount_'
callback_data_accept_agreement = 'bot.accept_agreement'

#======================================================#
#===================СОЗДАНИЕ ОРДЕРА====================#
#======================================================#

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data == callback_data_accept_agreement)
def bot_to_main_menu(call):
    """ Подтверждает выбор пользователя
        о соглашении и переводит пользователя
        к выбору валютных пар
    """
    user = db.get_user(call.from_user.id)

    if user['is_agreement'] == False:
        db.update_user(call.from_user.id, args={'is_agreement': 1})

    bot.answer_callback_query(
        call.id,
        text=translate(user['language_code'], 'bot_agreement_is_accepted'),
        show_alert=True
    )

    # Повторяет код из следующей функции
    #
    #
    # - Получаем пары
    pairs = db.get_pairs()
    # - Отображаем сообщение с валютными парами

    bot.delete_message(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
    )

    bot.send_message(
        chat_id=call.message.chat.id,
        text=translate(user['language_code'], 'exchange_select_pair'),
        reply_markup=MenuKeyboard.pairs(user, pairs, callback_data_select_pair)
    )
    # - Даёт возможность перейти к выбору банка
    bot.set_state(call.from_user.id, ExchageState.A2)
    #
    #
    # Повторяет код из следующей функции



#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_open_user_chat))
def callback_data_open_chat(call):
    """ Открытие чата
        по сделке
    """
    deal_id = call.data.replace(callback_data_open_user_chat, "")
    user = db.get_user(call.from_user.id)
    deal = db.get_deal(deal_id)

    bot.edit_message_reply_markup(
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        reply_markup=''
    )

    bot.send_message(
        chat_id=call.message.chat.id,
        text=translate(
            user['language_code'],
            'deal_chat_start'
        ).format(**{
            "id": deal_id
        }),
        reply_markup=MenuKeyboard.back_to(
            user,
            data='bot.back_to_main_menu',
            key_string='inline_back_to',
        )
    )

    bot.set_state(call.from_user.id, UserDeal.chat)
    #
    with bot.retrieve_data(call.from_user.id) as data:
        data['user'] = json.dumps(
            user,
            indent=4,
            sort_keys=True,
            default=str
        )
        data['deal'] = json.dumps(
            deal,
            indent=4,
            sort_keys=True,
            default=str
        )
        data['message_id'] = str(call.message.message_id)


@bot.message_handler(is_chat=False, state=UserDeal.chat, content_types=['audio', 'animation', 'sticker', 'video_note', 'voice', 'contact', 'location', 'venue', 'dice', 'invoice', 'successful_payment'])
def not_supported_message(message):
    """ Если пользователь отправил
        неподдерживаемый тип контента
        сообщаем ему об этом
    """
    user = db.get_user(message.from_user.id)
    with bot.retrieve_data(message.from_user.id) as data:
        deal = json.loads(data['deal'])
        bot.send_message(
            message.from_user.id,
            translate(user['language_code'], 'deal_file_not_supported')
        )

@bot.message_handler(is_chat=False, state=UserDeal.chat, content_types=['text', 'photo', 'video', 'document'])
def set_message(message):
    """ Сохраняем сообщение
    """
    with bot.retrieve_data(message.from_user.id) as data:
        user = json.loads(data['user'])
        deal = json.loads(data['deal'])

        data['attach'] = {}
        data['message'] = message.caption if message.caption is not None else 'Empty'
        data['content_type'] = message.content_type

        if message.content_type == 'photo':
            data['attach']["data"] = message.photo[-1].file_id

        if message.content_type == 'document':
            data['attach']["data"] = message.document.file_id

        if message.content_type == 'video':
            data['attach']["data"] = message.video.file_id

        if message.content_type == 'text':
            data['message'] = message.text[0:2048]

        try:
            new_message = bot.send_message(
                chat_id=message.chat.id,
                text=translate(user['language_code'], 'user_deal_add_data_success'),
                reply_markup=MenuKeyboard.accept_or_decline(
                    user,
                    cl_accept=callback_data_deal_send_message,
                    key_string_accept='inline_deal_send_message',
                    cl_decline='bot.back_to_main_menu',
                    key_string_decline='inline_back_to_main_menu',
                )
            )
            data['message_id'] = new_message.message_id
        except Exception as e:
            print(e)


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_deal_send_message), state=UserDeal.chat)
def accept_send_message(call):
    """ Подтверждаем отправку сообщения
    """
    config = db.get_config()

    with bot.retrieve_data(call.from_user.id) as data:
        user = json.loads(data['user'])
        deal = json.loads(data['deal'])
        manager_deal = db.get_user(deal['manager_id'], name_id="id")

        try:
            dialog = db.get_dialog(
                deal['id'],
                name_id="deal_id"
            )

            bot.edit_message_text(
                message_id=call.message.message_id,
                chat_id=call.message.chat.id,
                text=call.message.text,
                reply_markup=''
            )
            bot.send_message(
                chat_id=call.message.chat.id,
                text=translate(
                    user['language_code'],
                    'deal_chat_send_manager_message_success'
                ),
                reply_markup=MenuKeyboard.back_to(
                    user,
                    data='bot.back_to_main_menu',
                    key_string='inline_back_to',
                )
            )

            db.create_message(
                user_id=user['id'],
                dialog_id=dialog['id'],
                text=data['message'],
                attach=data['attach'],
                content_type=data['content_type'],
            )
        except Exception as e:
            print(e)

        try:
            kb = MenuKeyboard.back_to(
                manager_deal,
                key_string='inline_admin_notification_get_deal',
                data=callback_data_admin_work_open_deal+str(deal['id']),
            )

            user_deal_tid = manager_deal['telegram_id']
            key_string = 'msg_chat_deal_user'

            msg_attach = translate(
                user['language_code'],
                key_string
            ).format(**{
                "id": deal['id'],
                "text": escape_markdown(data['message'])
            })


            if data['content_type'] == 'text':
                bot.send_message(user_deal_tid, msg_attach, reply_markup=kb)

            if data['content_type'] == 'photo':
                bot.send_photo(user_deal_tid, data['attach']['data'], caption=msg_attach, reply_markup=kb)

            if data['content_type'] == 'video':
                bot.send_video(user_deal_tid, data['attach']['data'], caption=msg_attach, reply_markup=kb)

            if data['content_type'] == 'document':
                bot.send_document(user_deal_tid, data['attach']['data'], caption=msg_attach, reply_markup=kb)
        except Exception as e:
            print(e)

    bot.delete_state(call.from_user.id)
