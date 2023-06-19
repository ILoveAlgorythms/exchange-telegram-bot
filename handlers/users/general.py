from loader import bot, db, ROOT_DIR
from bot_locale.translate import translate
from keyboards.inline.menu import MenuKeyboard
from telebot.util import extract_arguments
from utils.misc.data import cryptoexchange_parse_rate
import json

callback_data_select_user_deal = 'bot.my_exchanges.id_'
callback_data_admin_work_open_deal = 'admin.open_work_deal_'
callback_data_admin_work_open_ticket = 'admin.open_work_ticket_'

@bot.message_handler(is_chat=False, commands=['start'])
def start_handler(message):
    """ BOT /start
        Создаёт пользователя, если его нет
        или отображает главное меню,
        если пользователь существует
    """
    user = db.get_user(message.from_user.id)
    if not user:
        db.create_user(message.from_user)
        user = db.get_user(message.from_user.id)

    # Очищает любое состояние после вызова команды
    bot.delete_state(message.from_user.id)

    text = translate(user['language_code'], 'start_text')
    kb = MenuKeyboard.home(user)

    if user['role'] in ['manager', 'admin']:
        args = extract_arguments(message.text)

        if args.startswith("order"):
            # Открыть сделку
            order_id = args.replace("order", "")
            text = translate(user['language_code'], 'user_from_notification_view_deal').format(**{
                "id": order_id
            })
            kb = MenuKeyboard.back_to(
                user,
                key_string='inline_admin_notification_get_deal',
                data=callback_data_admin_work_open_deal+order_id
            )

        if args.startswith("ticket"):
            # Открыть тикет
            ticket_id = args.replace("ticket", "")
            text = translate(user['language_code'], 'user_from_notification_view_ticket').format(**{
                "id": ticket_id
            })
            kb = MenuKeyboard.back_to(
                user,
                key_string='inline_admin_notification_get_ticket',
                data=callback_data_admin_work_open_ticket+ticket_id
            )

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=kb
    )

@bot.message_handler(is_chat=False, commands=['agreement'])
def start_handler(message):
    """ BOT /agreement
        Отображает соглашение
    """
    user = db.get_user(message.from_user.id)
    page = db.get_page(slug=2, name_id='id') or {}

    if page.get("document") != "null":
        document = json.loads(page['document'])
        file = document['file_id']

        try:
            bot.get_file(file)
        except Exception as e:
            file = open(ROOT_DIR + document['path'], 'rb')

        bot.send_document(
            chat_id=message.chat.id,
            document=file,
            caption=page.get(
                'page_content',
                translate(user['language_code'], 'page_not_found')
            ),
            reply_markup=MenuKeyboard.back_to(user)
        )

        return

    bot.send_message(
        chat_id=message.chat.id,
        text=page.get(
            'page_content',
            translate(user['language_code'], 'page_not_found')
        ),
        reply_markup=MenuKeyboard.back_to(user)
    )


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data == 'bot.back_to_main_menu')
def bot_to_main_menu(call):
    """ Функция возвращения в главное меню
        Очищает любой State в любой ситуации
    """
    user = db.get_user(call.from_user.id)

    bot.delete_state(call.from_user.id)

    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=translate(user['language_code'], 'start_text'),
            reply_markup=MenuKeyboard.home(user)
        )
    except Exception as e:
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=''
        )
        bot.send_message(
            chat_id=call.message.chat.id,
            text=translate(user['language_code'], 'start_text'),
            reply_markup=MenuKeyboard.home(user)
        )

# ========================Отображение данных о сделке========================
@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_select_user_deal))
def view_user_deal(call):
    """ Отображает данные сделки
    """
    deal_id = call.data.replace(callback_data_select_user_deal, "")
    user = db.get_user(call.from_user.id)
    deal = db.get_deal(deal_id)

    if deal is None or deal['user_id'] != user['id']:
        # Ничего не делаем
        return

    deal_status = translate(user['language_code'], 'dict_deal_status')
    deal_status_text = translate(user['language_code'], 'dict_deal_status_text')

    deal_text = translate(
        user['language_code'],
        'my_exchange_deal_info'
    ).format(**{
        "id":                 deal['id'],
        "from_amount":        deal['from_amount'],
        "from_name":          deal['from_name'],
        "from_bank_name":     deal['from_bank_name'],
        "from_exchange_rate": deal['exchange_rate'],
        "to_amount":          deal['to_amount'],
        "to_name":            deal['to_name'],
        "to_bank_name":       deal['to_bank_name'],
        "requisites":         deal['requisites'],
        "status_emoji":       deal_status[deal['status']],
        "status_text":        deal_status_text[deal['status']].lower(),
        "datetime":           deal['created_at'],
        "update_datetime":    deal['updated_at'],
    })
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=deal_text,
        reply_markup=MenuKeyboard.back_to(user, key_string='inline_back_to', data='bot.main.my_exchanges')
    )

@bot.callback_query_handler(is_chat=False,
func=lambda call: call.data.startswith('bot.main.'))
def bot_main_callback_funcions(call):
    """ Обрабатывает основные inline-кнопки в боте,
        Текстовые разделы, Cписок ордеров пользователя, Поддержка
    """
    calldata = call.data.replace('bot.main.', '')
    user = db.get_user(call.from_user.id)

    if calldata == 'my_exchanges':
        # Выводит информацию о сделках пользователя
        #
        user_deals = db.get_deals(user['id'], end_limit=5)
        lang = user['language_code']

        deal_text = translate(lang, 'chapter_my_exchanges')
        deal_status = translate(lang, 'dict_deal_status')
        stroke = "\n\n"

        for deal in user_deals:
            stroke += f"{deal_status[deal['status']]} {deal['created_at']} /TEST\n{deal['from_amount']} {deal['from_name']} ➡️ {deal['to_amount']} {deal['to_name']}\n\n"

        deal_text += stroke

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=deal_text,
            reply_markup=MenuKeyboard.deals(user, user_deals, callback_data_select_user_deal)
        )

    if calldata == 'support':
        # Выводит информацию о тикетах пользователя
        #

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=translate(user['language_code'], 'chapter_support'),
            reply_markup=MenuKeyboard.support(user)
        )

        bot.delete_state(call.from_user.id)

    if calldata.startswith('page.'):
        # Выводит текстовую страницу из БД
        # Inline Data: bot.main.page.[slug]
        #
        slug = calldata.replace('page.', '')
        page = db.get_page(slug=slug) or {}



        if page.get("document") != "null":
            document = json.loads(page['document'])
            file = document['file_id']

            try:
                bot.get_file(file)
            except Exception as e:
                file = open(ROOT_DIR + document['path'], 'rb')

            bot.send_document(
                chat_id=call.message.chat.id,
                document=file,
                caption=page.get(
                    'page_content',
                    translate(user['language_code'], 'page_not_found')
                ),
                reply_markup=MenuKeyboard.back_to(user)
            )

            return

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=page.get(
                'page_content',
                translate(user['language_code'], 'page_not_found')
            ),
            reply_markup=MenuKeyboard.back_to(user)
        )
