from loader import bot, db
from states.states import AdminDeal
from bot_locale.translate import translate
from utils.message_templates import get_admin_deal_text, get_requisites_text
from keyboards.inline.menu import AdminKeyboard, MenuKeyboard
from telebot.formatting import escape_markdown
import json

callback_data_admin_back_to_home = 'admin.back_to_home'
callback_data_admin_open_deals = 'admin.open_deals'
callback_data_admin_open_disput_deals = 'admin.open_disput_deals'
callback_data_admin_work_open_deal = 'admin.open_work_deal_'
callback_data_admin_change_status_deal = 'admin.deal_change_status_'
callback_data_send_requisites = 'admin.deal_send_requisites'
callback_data_deal_set_profit = 'admin.deal_set_profit_'
callback_data_deal_chat = 'admin.deal_open_chat_'
callback_data_deal_send_message = 'admin.deal_send_message_chat'
callback_data_open_user_chat = 'bot.deal_open_user_chat_'
cache_waiting_create_new_deal = '{0}_deal_locked_time'


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_work_open_deal), role=['manager', 'admin'])
def admin_open_work_order(call):
    """ Открывает сделку с панелью управления
    """

    deal_id = call.data.replace(callback_data_admin_work_open_deal, "")
    user = db.get_user(call.from_user.id)
    deal = db.get_deal(deal_id)
    if deal is None: return

    bot.delete_state(call.from_user.id)

    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=''
    )

    bot.send_message(
        chat_id=call.message.chat.id,
        text=get_admin_deal_text(user, deal),
        reply_markup=AdminKeyboard.deal(user, deal)
    )

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_change_status_deal), role=['manager', 'admin'])
def admin_open_work_order(call):
    """ Изменяет статус сделки
    """
    calldata = call.data.replace(callback_data_admin_change_status_deal, "")
    data = calldata.split("_")
    action_type = data[0]
    deal_id = data[1]
    user = db.get_user(call.from_user.id)
    deal = db.get_deal(deal_id)
    user_deal =  db.get_user(deal['user_id'], name_id="id")
    lang_user_deal = user_deal['language_code']

    if (
        deal['manager_id'] != 0 and
        deal['manager_id'] != user['id']
    ):
        bot.answer_callback_query(
            call.id,
            translate(user['language_code'], 'warning_deal_manager_is_exists')
        )
        return

    if action_type == 'accepted':
        # Подтверждаем сделку
        deal['status'] = 'accepted'
        deal['manager_id'] = user['id']
        try:
            deal_text = translate(
                user_deal['language_code'],
                'deal_accepted_manager'
            ).format(
                deal['id']
            )
            bot.send_message(
                user_deal['telegram_id'],
                text=deal_text
            )
        except Exception as e:
            print(e)

        db.create_dialog(
            user_deal['id'],
            deal_id=deal['id'],
            title=translate(
                user_deal['language_code'],
                'msg_deal'
            ).format(**{
                "id": deal['id']
            }),
            type='deal'
        )
        db.update_deal(
            deal_id,
            {
             'status': 'accepted',
             'manager_id': user['id']
            }
        )

    if action_type == 'declined':
        deal['status'] = 'declined'
        deal['manager_id'] = user['id']
        try:
            deal_text = translate(
                user_deal['language_code'],
                'deal_declined_manager'
            ).format(
                deal['id']
            )
            bot.send_message(
                user_deal['telegram_id'],
                text=deal_text
            )
        except Exception as e:
            pass

        db.update_deal(deal_id, {'status': 'declined'})

    if action_type == 'process':
        deal['manager_id'] = user['id']
        deal['status'] = 'process'
        # выдаём состояние и переводим на другой callback
        bot.set_state(call.from_user.id, AdminDeal.requisites)
        with bot.retrieve_data(call.from_user.id) as data:
            data['deal'] = json.dumps(
                deal,
                indent=4,
                sort_keys=True,
                default=str
            )
            data['user'] = json.dumps(
                user,
                indent=4,
                sort_keys=True,
                default=str
            )
            data['user_deal'] = json.dumps(
                user_deal,
                indent=4,
                sort_keys=True,
                default=str
            )

        send_requisites = translate(
            user['language_code'],
            'admin_deal_send_requisites'
        ).format(**{
            "id": deal['id'],
            "username": escape_markdown(user_deal['username']),
            "telegram_id": user_deal['telegram_id'],
            "from_amount": deal['from_amount'],
            "from_name": deal['from_name'],
            "from_bank_name": deal['from_bank_name']
        })

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=send_requisites,
            reply_markup=''
        )
        return True

    if action_type == 'completed':
        deal['status'] = 'completed'
        deal['manager_id'] = user['id']
        try:
            deal_completed_text = translate(
                user_deal['language_code'],
                'deal_completed_user'
            ).format(**{
                "id": deal['id'],
                "to_name": deal['to_name'],
                "to_bank_name": deal['to_bank_name'],
                "to_amount": deal['to_amount'],
            })

            string_view_deal = translate(lang_user_deal, 'inline_deal_view_deal')
            string_open_dusput_deal = translate(lang_user_deal, 'inline_deal_open_dispute')
            string_open_main_menu = translate(lang_user_deal, 'inline_back_to_main_menu')
            string_crate_new_exchange = translate(lang_user_deal, 'inline_create_new_exchange')

            bot.send_message(
                user_deal['telegram_id'],
                text=deal_completed_text,
                reply_markup=MenuKeyboard.smart({
                    string_view_deal: {'callback_data': 'bot.my_exchanges.id_'+str(deal['id'])},
                    string_open_dusput_deal: {'callback_data': 'bot.deal_open_dispute_'+str(deal['id'])},
                    string_crate_new_exchange: {'callback_data': 'bot.set.new_exchange'},
                    string_open_main_menu: {'callback_data': 'bot.back_to_main_menu'},
                })
            )
            db.update_deal(deal['id'], {'status': 'completed'})
            # Снимаем блокировку
            cache.delete(cache_waiting_create_new_deal.format(deal['user_id']))
        except Exception as e:
            print(e)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=get_admin_deal_text(user, deal),
        reply_markup=AdminKeyboard.deal(user, deal)
    )

@bot.message_handler(is_chat=False, state=AdminDeal.requisites, role=['manager', 'admin'])
def send_requisites(message):
    """ Убеждаемся, что всё верно
    """
    with bot.retrieve_data(message.from_user.id) as data:
        deal = json.loads(data['deal'])
        user = json.loads(data['user'])
        data['requisites'] = json.dumps(message.text)
        confirmation_send_requisites = translate(
            user['language_code'],
            'user_deal_send_requisites_confirmation'
        ).format(
            str(message.text)
        )
        bot.send_message(
            message.from_user.id,
            confirmation_send_requisites,
            reply_markup=MenuKeyboard.accept_or_decline(
                user,
                callback_data_send_requisites,
                callback_data_admin_work_open_deal+str(deal['id'])
            )
        )

@bot.callback_query_handler(state=AdminDeal.requisites, is_chat=False, func=lambda call: call.data == callback_data_send_requisites, role=['manager', 'admin'])
def send_requisites(call):
    """ Отправляем реквизиты
    """
    with bot.retrieve_data(call.from_user.id) as data:
        deal = json.loads(data['deal'])
        user = json.loads(data['user'])
        user_deal = json.loads(data['user_deal'])

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=translate(user['language_code'], 'user_deal_send_requisites_success'),
            reply_markup=MenuKeyboard.back_to(
                user,
                data=(callback_data_admin_work_open_deal+str(deal['id'])),
                key_string='inline_back_to'
            )
        )
        try:
            requisites = escape_markdown(
                json.loads(data['requisites'])
            )
            requisites_text, kb = get_requisites_text(user, deal, requisites)

            bot.send_message(
                user_deal['telegram_id'],
                requisites_text,
                reply_markup=kb
            )
            db.update_deal(
                deal['id'],
                {'status': 'process', 'from_requisites': requisites}
            )
        except Exception as e:
            print(e)

    bot.delete_state(call.from_user.id)

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data == callback_data_admin_open_deals, role=['manager', 'admin'])
def admin_open_orders(call):
    """ Открывает список сделок (новые, в работе, споры)
    """
    user = db.get_user(call.from_user.id)
    deals = db.get_deals(
        name_id="status",
        data=['new', 'accepted', 'process', 'paid'],
        order_by='ASC',
        end_limit=50
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='Список сделок находящихся в процессе. В порядке убывания, от старых к новым.',
        reply_markup=AdminKeyboard.deals(user, deals, callback_data=callback_data_admin_work_open_deal)
    )

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data == callback_data_admin_open_disput_deals, role=['manager', 'admin'])
def admin_open_orders(call):
    """ Открывает список с проблемными сделками
    """
    user = db.get_user(call.from_user.id)
    deals = db.get_deals(
        name_id="status",
        data=['dispute'],
        end_limit=50
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='Список сделок находящихся в споре. В порядке убывания, от старых к новым.',
        reply_markup=AdminKeyboard.deals(user, deals, callback_data=callback_data_admin_work_open_deal)
    )


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_deal_chat))
def callback_data_open_chat(call):
    """ Открытие чата с пользователем
        по сделке
    """
    deal_id = call.data.replace(callback_data_deal_chat, "")
    user = db.get_user(call.from_user.id)
    deal = db.get_deal(deal_id)

    bot.edit_message_text(
        message_id=call.message.message_id,
        chat_id=call.message.chat.id,
        text=translate(
            user['language_code'],
            'deal_chat_start'
        ).format(**{
            "id": deal_id
        }),
        reply_markup=MenuKeyboard.back_to(
            user,
            data=callback_data_admin_work_open_deal+str(deal['id']),
            key_string='inline_back_to',
        )
    )

    bot.set_state(call.from_user.id, AdminDeal.chat)
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


@bot.message_handler(is_chat=False, state=AdminDeal.chat, content_types=['audio', 'animation', 'sticker', 'video_note', 'voice', 'contact', 'location', 'venue', 'dice', 'invoice', 'successful_payment'])
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

@bot.message_handler(is_chat=False, state=AdminDeal.chat, content_types=['text', 'photo', 'video', 'document'])
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
                    cl_decline=callback_data_admin_work_open_deal+str(deal['id']),
                    key_string_decline='inline_back_to',
                )
            )
            data['message_id'] = new_message.message_id
        except Exception as e:
            print(e)


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_deal_send_message), state=AdminDeal.chat)
def accept_send_message(call):
    """ Подтверждаем отправку сообщения
    """
    config = db.get_config()

    with bot.retrieve_data(call.from_user.id) as data:
        user = json.loads(data['user'])
        deal = json.loads(data['deal'])
        deal = db.get_deal(deal['id'])
        user_deal = db.get_user(deal['user_id'], name_id="id")

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
                    'deal_chat_send_message_success'
                ),
                reply_markup=MenuKeyboard.back_to(
                    user,
                    data=callback_data_admin_work_open_deal+str(deal['id']),
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
                user_deal,
                key_string='inline_reply_message',
                data=callback_data_open_user_chat+str(deal['id']),
            )

            user_deal_tid = user_deal['telegram_id']

            key_string = 'msg_chat_deal_disput_manager' if deal['status'] == 'dispute' else 'msg_chat_deal_manager'

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



@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_deal_set_profit), role=['manager', 'admin'])
def admin_set_profit(call):
    """ Задаём профит (прибыль от сделки)
    """
    user = db.get_user(call.from_user.id)
    deal_id = call.data.replace(callback_data_deal_set_profit, "")
    deal = db.get_deal(deal_id)

    bot.set_state(call.from_user.id, AdminDeal.profit)

    with bot.retrieve_data(call.from_user.id) as data:
        data['deal'] = json.dumps(
            deal,
            indent=4,
            sort_keys=True,
            default=str
        )
        data['user'] = json.dumps(
            user,
            indent=4,
            sort_keys=True,
            default=str
        )
        profit_text = translate(
            user['language_code'],
            'admin_deal_set_profit'
        ).format(
            deal['from_name'],
            deal['to_name'],
            deal['profit_asset']
        )

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=profit_text,
            reply_markup=MenuKeyboard.back_to(
                user,
                data=(callback_data_admin_work_open_deal+str(deal['id'])),
                key_string='inline_back_to'
            )
        )



@bot.message_handler(is_chat=False, state=AdminDeal.profit, role=['manager', 'admin'])
def save_profit_or_decline(message):
    """ Сохраняем профит
    """
    with bot.retrieve_data(message.from_user.id) as data:
        user = json.loads(data['user'])
        deal = json.loads(data['deal'])
        profit = 0
        profit_asset = deal['profit_asset']
        profit_input_asset = None
        assets = [deal['from_name'], deal['to_name'], deal['profit_asset']]

        kb = MenuKeyboard.back_to(
            user,
            data=(callback_data_admin_work_open_deal+str(deal['id'])),
            key_string='inline_back_to'
        )

        try:
            profit_info = message.text.split(" ")
            profit_input_asset = profit_info[1].upper()
            profit = float(profit_info[0])
        except Exception as e:
            pass

        if profit <= 0 or profit > deal['from_amount'] or profit_input_asset not in assets:
            bot.send_message(
                chat_id=message.chat.id,
                text=translate(user['language_code'], 'error_data_not_valid'),
                reply_markup=kb
            )
            return

        db.update_deal(
            deal['id'],
            {'profit': profit, 'profit_asset': profit_input_asset}
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=translate(user['language_code'], 'admin_deal_profit_fixed'),
            reply_markup=kb
        )

    bot.delete_state(message.from_user.id)
