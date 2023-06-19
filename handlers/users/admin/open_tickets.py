from loader import bot, db
from states.states import AdminDeal, AdminTicket
from bot_locale.translate import translate
from utils.message_templates import get_admin_deal_text
from keyboards.inline.menu import AdminKeyboard, MenuKeyboard
from telebot.formatting import escape_markdown, escape_html
import json

callback_data_admin_back_to_home = 'admin.back_to_home'
callback_data_admin_open_tickets = 'admin.support_tickets'
callback_data_admin_work_open_ticket = 'admin.open_work_ticket_'
callback_data_admin_change_ticket_status = 'admin.ticket_change_status_'
callback_data_admin_ticket_open_chat = 'admin.ticket_open_chat_'
callback_data_admin_ticket_open_chat_send = 'admin.ticket_chat_send'


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_work_open_ticket), role=['manager', 'admin'])
def admin_open_work_order(call):
    """ Открывает тикет с панелью управления
    """

    dialog_id = call.data.replace(callback_data_admin_work_open_ticket, "")
    user = db.get_user(call.from_user.id)
    ticket = db.get_dialog(dialog_id, name_id="id")
    ticket_user = db.get_user(ticket['user_id'], name_id="id")
    if ticket is None: return
    messages = db.get_messages({'dialog_id': dialog_id}, start_limit=0, end_limit=1, filter='ASC')
    msg_text = '-'

    bot.delete_state(call.from_user.id)

    if messages != []:
        msg_text = escape_html(escape_markdown(messages[0]['text']))

    ticket_status = translate(user['language_code'], 'dict_ticket_status')
    ticket_view = translate(
        user['language_code'],
        'admin_ticket_view'
    ).format(**{
        "id": ticket['id'],
        "telegram_id": ticket_user['telegram_id'],
        "username": escape_markdown(ticket_user['username']),
        "ticket_title": escape_markdown(ticket['title']),
        "ticket_text": msg_text,
        "status": ticket_status[ticket['status']],
        "created_at": ticket['created_at'],
    })

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=str(ticket_view),
        reply_markup=AdminKeyboard.ticket(user, ticket)
    )

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_change_ticket_status), role=['manager', 'admin'])
def admin_ticket_change_status(call):
    """ Изменяет статус тикета
    """

    prms = call.data.replace(callback_data_admin_change_ticket_status, "")
    params = prms.split("_")
    user = db.get_user(call.from_user.id)
    ticket = db.get_dialog(params[1], name_id="id")

    if ticket is None:
        return

    ticket['status'] = params[0]
    ticket_status = translate(
        user['language_code'],
        'dict_ticket_status'
    )
    ticket_view = translate(
        user['language_code'],
        'admin_ticket_update'
    ).format(**{
        "id": ticket['id'],
    })

    db.update_dialog(params[1], args={'status': params[0]})

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=ticket_view,
        reply_markup=MenuKeyboard.back_to(
            user,
            data=callback_data_admin_work_open_ticket+str(ticket['id']),
            key_string='inline_back_to',
        )
    )

####
####
####
####
####
####
####
####
####
####
####
####
####
####
####
####
####


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_ticket_open_chat))
def admin_ticket_open_chat(call):
    """ Открытие чата с пользователем
        по тикету
    """
    ticket_id = call.data.replace(callback_data_admin_ticket_open_chat, "")
    user = db.get_user(call.from_user.id)
    ticket = db.get_dialog(ticket_id, name_id="id")
    ticket_user = db.get_user(ticket['user_id'], name_id="id")
    if ticket is None: return

    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        text=translate(
            user['language_code'],
            'ticket_chat_start'
        ).format(**{
            "id": ticket_id
        }),
        reply_markup=MenuKeyboard.back_to(
            user,
            data=callback_data_admin_work_open_ticket+str(ticket['id']),
            key_string='inline_back_to',
        )
    )

    bot.set_state(call.from_user.id, AdminTicket.chat)
    #
    with bot.retrieve_data(call.from_user.id) as data:
        data['user'] = json.dumps(
            user,
            indent=4,
            sort_keys=True,
            default=str
        )
        data['ticket_user'] = json.dumps(
            ticket_user,
            indent=4,
            sort_keys=True,
            default=str
        )
        data['ticket'] = json.dumps(
            ticket,
            indent=4,
            sort_keys=True,
            default=str
        )
        data['message_id'] = str(call.message.message_id)


@bot.message_handler(is_chat=False, state=AdminTicket.chat, content_types=['audio', 'animation', 'sticker', 'video_note', 'voice', 'contact', 'location', 'venue', 'dice', 'invoice', 'successful_payment'])
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

@bot.message_handler(is_chat=False, state=AdminTicket.chat, content_types=['text', 'photo', 'video', 'document'])
def set_message(message):
    """ Сохраняем сообщение
    """
    with bot.retrieve_data(message.from_user.id) as data:
        user = json.loads(data['user'])
        ticket = json.loads(data['ticket'])

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
                    cl_accept=callback_data_admin_ticket_open_chat_send,
                    key_string_accept='inline_deal_send_message',
                    cl_decline=callback_data_admin_work_open_ticket+str(ticket['id']),
                    key_string_decline='inline_back_to',
                )
            )
            data['message_id'] = new_message.message_id
        except Exception as e:
            print(e)


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_ticket_open_chat_send), state=AdminTicket.chat)
def accept_send_message(call):
    """ Подтверждаем отправку сообщения
    """
    config = db.get_config()

    with bot.retrieve_data(call.from_user.id) as data:
        ticket_user = json.loads(data['ticket_user'])
        user = json.loads(data['user'])
        ticket = json.loads(data['ticket'])
        user_ticket = db.get_user(ticket['user_id'], name_id="id")

        try:
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
                    'ticket_chat_send_message_success'
                ),
                reply_markup=MenuKeyboard.back_to(
                    user,
                    data=callback_data_admin_work_open_ticket+str(ticket['id']),
                    key_string='inline_back_to',
                )
            )

            db.create_message(
                user_id=user['id'],
                dialog_id=ticket['id'],
                text=data['message'],
                attach=data['attach'],
                content_type=data['content_type'],
            )
        except Exception as e:
            print(e)

        try:
            kb = ''

            user_ticket_tid = user_ticket['telegram_id']
            key_string = 'msg_chat_ticket_manager'

            msg_attach = translate(
                user['language_code'],
                key_string
            ).format(**{
                "id": ticket['id'],
                "text": escape_markdown(data['message'])
            })


            if data['content_type'] == 'text':
                bot.send_message(user_ticket_tid, msg_attach, reply_markup=kb)

            if data['content_type'] == 'photo':
                bot.send_photo(user_ticket_tid, data['attach']['data'], caption=msg_attach, reply_markup=kb)

            if data['content_type'] == 'video':
                bot.send_video(user_ticket_tid, data['attach']['data'], caption=msg_attach, reply_markup=kb)

            if data['content_type'] == 'document':
                bot.send_document(user_ticket_tid, data['attach']['data'], caption=msg_attach, reply_markup=kb)
        except Exception as e:
            print(e)
