from utils.misc.data import (
    binance_p2p_arithmetic_mean_data,
    binance_get_price_pair
)
from utils.message_templates import get_admin_deal_text
from states.states import ExchageState, UserDeal
from keyboards.inline.menu import MenuKeyboard
from telebot.formatting import escape_markdown
from bot_locale.translate import translate
from loader import bot, db, config
import json

callback_data_deal_open_disput = 'bot.deal_open_dispute_'
callback_data_deal_create_disput = 'bot.deal_create_dispute'

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_deal_open_disput))
def open_dispute_deal(call):
    """ Пользователь открывает спор
        по сделке
    """
    deal_id = call.data.replace(callback_data_deal_open_disput, "")
    user = db.get_user(call.from_user.id)
    deal = db.get_deal(deal_id)

    if (
        deal['user_id'] != user['id'] or
        deal['status'] in ['dispute', 'declined']
    ):
        bot.answer_callback_query(
            call.id,
            translate(user['language_code'], 'deal_not_available'),
            show_alert=True
        )
        return

    bot.send_message(
        chat_id=call.message.chat.id,
        text=translate(
            user['language_code'],
            'deal_create_disput_start'
        ).format(**{
            "id": deal_id
        }),
    )

    bot.set_state(call.from_user.id, UserDeal.dispute)
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

@bot.message_handler(is_chat=False, state=UserDeal.dispute, content_types=['audio', 'animation', 'sticker', 'video_note', 'voice', 'contact', 'location', 'venue', 'dice', 'invoice', 'successful_payment'])
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

@bot.message_handler(is_chat=False, state=UserDeal.dispute, content_types=['text', 'photo', 'video', 'document'])
def set_message(message):
    """ Получаем доп информацию от пользователя по сделке
        (перед открытием спора)

        В текущей версии возможно прикреплять только по единице
        контента (1 фото или 1 видео или 1 документ) с описанием
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
                    cl_accept=callback_data_deal_create_disput,
                    key_string_accept='inline_deal_open_dispute',
                    cl_decline='bot.back_to_main_menu',
                    key_string_decline='inline_back_to_main_menu',
                )
            )
            data['message_id'] = new_message.message_id
        except Exception as e:
            print(e)


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_deal_create_disput), state=UserDeal.dispute)
def bot_to_main_menu(call):
    """ Подтверждаем создание спора
    """
    config = db.get_config()

    with bot.retrieve_data(call.from_user.id) as data:
        user = json.loads(data['user'])
        deal = json.loads(data['deal'])
        deal = db.get_deal(deal['id'])

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
                    'deal_create_disput_data_created'
                ).format(**{
                    "id": deal['id']
                })
            )

            db.create_message(
                user_id=user['id'],
                dialog_id=dialog['id'],
                text=data['message'],
                attach=data['attach'],
                content_type=data['content_type'],
            )

            db.update_deal(deal['id'], {'status': 'dispute'})
        except Exception as e:
            print(e)

        if config['notifications_deal_chat_id'] is not False:
            try:
                kb = MenuKeyboard.notification_deal(user, deal['id'])
                m = bot.send_message(
                    chat_id=config['notifications_deal_chat_id'],
                    text=translate(
                        user['language_code'],
                        'deal_create_disput_data_created_notification'
                    ).format(**{
                        "id": deal['id']
                    }),
                    reply_markup=kb
                )

                if data.get('content_type') is None:
                    # Если ничего не заполнено, не отправляем аттачи
                    return

                msg_attach = translate(
                    user['language_code'],
                    'msg_deal_attachment'
                ).format(**{
                    "id": deal['id'],
                    "text": escape_markdown(data['message'])
                })

                if data['content_type'] == 'text':
                    bot.send_message(config['notifications_deal_chat_id'], msg_attach, reply_to_message_id=m.message_id, reply_markup=kb)

                if data['content_type'] == 'photo':
                    bot.send_photo(config['notifications_deal_chat_id'], data['attach']['data'], caption=msg_attach, reply_to_message_id=m.message_id, reply_markup=kb)

                if data['content_type'] == 'video':
                    bot.send_video(config['notifications_deal_chat_id'], data['attach']['data'], caption=msg_attach, reply_to_message_id=m.message_id, reply_markup=kb)

                if data['content_type'] == 'document':
                    bot.send_document(config['notifications_deal_chat_id'], data['attach']['data'], caption=msg_attach, reply_to_message_id=m.message_id, reply_markup=kb)
            except Exception as e:
                print(e)

    bot.delete_state(call.from_user.id)
