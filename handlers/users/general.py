from loader import bot, db, ROOT_DIR
from bot_locale.translate import _
from keyboards.inline.menu import MenuKeyboard
from telebot.util import extract_arguments
from utils.misc.data import cryptoexchange_parse_rate
from utils.message_templates import get_user_deal_text
from utils.misc.view_page import page_send_message
import json
from math import ceil

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

    text = _(user['language_code'], 'start_text')
    kb = MenuKeyboard.home(user)

    if user['role'] in ['manager', 'admin']:
        args = extract_arguments(message.text)

        if args.startswith("order"):
            # Открыть сделку
            order_id = args.replace("order", "")
            text = _(user['language_code'], 'user_from_notification_view_deal').format(**{
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
            text = _(user['language_code'], 'user_from_notification_view_ticket').format(**{
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

@bot.message_handler(is_chat=False, func=lambda m: m.text == '🏚 Главное меню')
def home_menu(message):
    """ Главное меню ReplyButton
    """
    user = db.get_user(message.from_user.id)

    # Очищает любое состояние после вызова команды
    bot.delete_state(message.from_user.id)
    text = _(user['language_code'], 'start_text')
    kb = MenuKeyboard.home(user)

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

    page_send_message(message.from_user.id, user, page, MenuKeyboard.back_to(user))

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
            text=_(user['language_code'], 'start_text'),
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
            text=_(user['language_code'], 'start_text'),
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

    deal_text, kb = get_user_deal_text(user, deal)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=deal_text,
        reply_markup=kb
    )

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith('deal_page'))
def view_user_deal(call):
    """ Отображает данные сделок (пагинация)
    """
    deal_page = call.data.replace(deal_page, "")
    user = db.get_user(call.from_user.id)
    deal = db.get_deal(deal_id)

    if deal is None or deal['user_id'] != user['id']:
        # Ничего не делаем
        return

    deal_text, kb = get_user_deal_text(user, deal)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=deal_text,
        reply_markup=kb
    )

# ========================Отображение данных о сделке========================
@bot.message_handler(is_chat=False, func=lambda message: message.text.startswith('/D'))
def view_user_deal_by_uid(message):
    """ Отображает данные сделки по UID
    """
    deal_uid = message.text.replace("/D", "")
    if len(deal_uid) < 6: return

    user = db.get_user(message.from_user.id)
    deal = db.get_deal(deal_uid, name_id="uid")

    if deal is None or deal['user_id'] != user['id']:
        # Ничего не делаем
        return

    deal_text, kb = get_user_deal_text(user, deal)

    bot.send_message(
        chat_id=message.from_user.id,
        text=deal_text,
        reply_markup=kb
    )

@bot.callback_query_handler(is_chat=False,
func=lambda call: call.data.startswith('bot.deal_page_'))
def deal_page_pagination(call):
    """ Мини-пагинация

        (ужасная реализация, переписать)
    """
    limit_per_page = 5

    current_page = int(call.data.replace('bot.deal_page_', ''))
    user = db.get_user(call.from_user.id)
    deal_count = db.get_count("deals", sql=f"WHERE user_id = {user['id']}")

    pages = ceil(deal_count / limit_per_page)
    start_limit = 0 # default start limit
    end_limit = start_limit + limit_per_page # default end limit

    if current_page != 1:
        start_limit = (current_page - 1) * limit_per_page

    if current_page == pages and deal_count % limit_per_page != 0:
        end_limit = start_limit + deal_count % limit_per_page

    user_deals = db.get_deals(user['id'], start_limit=start_limit, end_limit=end_limit)

    lang = user['language_code']

    deal_text = _(lang, 'chapter_my_exchanges')
    deal_status = _(lang, 'dict_deal_status')
    stroke = "\n\n"

    for deal in user_deals:
        stroke += f"{deal_status[deal['status']]} {deal['created_at']} /D{deal['uid']}\n{deal['from_amount']} {deal['from_name']} ➡️ {deal['to_amount']} {deal['to_name']}\n\n"

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=stroke,
        reply_markup=MenuKeyboard.object_pagination(current_page, pages)
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
        # Пардон за сумбурное написание всего этого добра...
        #
        deal_count = db.get_count("deals", sql=f"WHERE user_id = {user['id']}")
        current_page, pages = 1, ceil(deal_count / 5)

        user_deals = db.get_deals(user['id'], end_limit=5)

        lang = user['language_code']

        deal_text = _(lang, 'chapter_my_exchanges')
        deal_status = _(lang, 'dict_deal_status')
        stroke = "\n\n"

        if user_deals:
            for deal in user_deals:
                stroke += f"{deal_status[deal['status']]} {deal['created_at']} /D{deal['uid']}\n{deal['from_amount']} {deal['from_name']} ➡️ {deal['to_amount']} {deal['to_name']}\n\n"

        if not user_deals:
            stroke = _(lang, 'deals_not_found')

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=deal_text,
        )

        bot.send_message(
            chat_id=call.message.chat.id,
            text=stroke,
            reply_markup=MenuKeyboard.object_pagination(current_page, pages)
        )

    if calldata == 'support':
        # Выводит информацию о тикетах пользователя
        #

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=_(user['language_code'], 'chapter_support'),
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
                    _(user['language_code'], 'page_not_found')
                ),
                reply_markup=MenuKeyboard.back_to(user)
            )

            return

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=page.get(
                'page_content',
                _(user['language_code'], 'page_not_found')
            ),
            reply_markup=MenuKeyboard.back_to(user)
        )
