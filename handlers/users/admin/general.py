from loader import bot, db
from states.states import ExchageState
from bot_locale.translate import translate
from keyboards.inline.menu import AdminKeyboard, MenuKeyboard
from telebot.util import extract_arguments, escape
from telebot.formatting import escape_markdown

callback_data_admin_back_to_home = 'admin.back_to_home'
callback_data_admin_params = 'admin.params'
callback_data_admin_open_tickets = 'admin.support_tickets'
callback_data_admin_work_open_ticket = 'admin.open_work_ticket_'
callback_data_admin_change_tecnical_break = 'admin.params_change_techinal_break'

@bot.message_handler(is_chat=False, commands=['admin'], is_admin=True)
def admin_home(message):
    """ BOT /admin
        Отображает панель администратора
    """
    # Кол-во открытых сделок
    open_deals_count = db.get_count(
        table='deals',
        sql="""
            WHERE status IN ('new','accepted','process', 'paid')
        """
    )
    # Кол-во оспариваемых сделок
    duspute_deals_count = db.get_count(
        table='deals',
        sql="""
            WHERE status = 'dispute'
        """
    )
    # Кол-во открытых тикетов
    open_ticket_count = db.get_count(
        table='dialogs',
        sql="""
            WHERE status = 'open' AND type = 'support'
        """
    )

    bot.delete_state(message.from_user.id)

    user = db.get_user(message.from_user.id)
    config = db.get_config()

    bot.send_message(
        message.from_user.id,
        'Admin, Hello!',
        reply_markup=AdminKeyboard.home(
            user,
            stats={
                'deals': open_deals_count,
                'dealsd': duspute_deals_count,
                'open_tickets': open_ticket_count
            },
            config=config
        )
    )

@bot.message_handler(is_chat=False, commands=['set_admin'], is_admin=True)
def set_admin(message):
    """ BOT /set_admin
        Даёт/забирает админку у пользователя по id/username
    """
    user = db.get_user(message.from_user.id)

    msg = '-'
    argument = extract_arguments(message.text)
    uid_or_uname = escape(argument).replace("@", "").replace("#", "")

    search_user = db.get_user(
        user_id=uid_or_uname,
        sql=f"""OR username = "{uid_or_uname}" """
    )

    if argument is None:
        bot.send_message(
            message.from_user.id,
            translate(user['language_code'], 'admin_data_parameters_not_found')
        )
        return

    if search_user is None:
        bot.send_message(
            message.from_user.id,
            translate(user['language_code'], 'admin_search_user_not_found')
        )
        return

    if user['id'] == search_user['id']:
        bot.send_message(
            message.from_user.id,
            translate(user['language_code'], 'admin_cant_ban_yourself')
        )
        return

    if search_user['is_admin'] == 1:
        db.update_user(search_user['telegram_id'], args={'is_admin': 0})
        msg = translate(user['language_code'], 'admin_user_is_not_admin').format(search_user['telegram_id'], escape_markdown(search_user['username']))

    if search_user['is_admin'] == 0:
        db.update_user(search_user['telegram_id'], args={'is_admin': 1})
        msg = translate(user['language_code'], 'admin_user_is_admin').format(search_user['telegram_id'], escape_markdown(search_user['username']))

    bot.send_message(
        message.from_user.id,
        text=msg
    )

@bot.message_handler(is_chat=False, commands=['ban'], is_admin=True)
def admin_home(message):
    """ BOT /ban
        Бан/Разбан пользователя по id/username
    """
    user = db.get_user(message.from_user.id)

    msg = ''
    argument = extract_arguments(message.text)
    uid_or_uname = escape(argument).replace("@", "").replace("#", "")

    search_user = db.get_user(
        user_id=uid_or_uname,
        sql=f"""OR username = "{uid_or_uname}" """
    )

    if argument is None:
        bot.send_message(
            message.from_user.id,
            translate(user['language_code'], 'admin_data_parameters_not_found')
        )
        return

    if search_user is None:
        bot.send_message(
            message.from_user.id,
            translate(user['language_code'], 'admin_search_user_not_found')
        )
        return

    if search_user['is_banned'] == 1:
        db.update_user(search_user['telegram_id'], args={'is_banned': 0})
        msg = translate(user['language_code'], 'admin_user_is_unban').format(search_user['telegram_id'], escape_markdown(search_user['username']))

    if search_user['is_banned'] == 0:
        db.update_user(search_user['telegram_id'], args={'is_banned': 1})
        msg = translate(user['language_code'], 'admin_user_is_banned').format(search_user['telegram_id'], escape_markdown(search_user['username']))

    bot.send_message(
        message.from_user.id,
        text=msg
    )


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data == callback_data_admin_open_tickets, is_admin=True)
def admin_open_tickets(call):
    """ Список открытых тикетов
    """
    user = db.get_user(call.from_user.id)
    tickets = db.get_dialogs(
        name_id="type",
        data=['support'],
        sql="""
            AND status = 'open'
        """
    )

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=translate(user['language_code'], 'admin_tickets_home'),
        reply_markup=AdminKeyboard.tickets(user, tickets, callback_data_admin_work_open_ticket)
    )


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data == callback_data_admin_change_tecnical_break, is_admin=True)
def admin_change_technical_break(call):
    """ Включение/отключение обменов
    """
    user = db.get_user(call.from_user.id)
    config = db.get_config()

    status = {
        0: ['admin_technical_break_on', 1],
        1: ['admin_technical_break_off', 0]
    }

    update_config = db.update_config({'technical_break': status[config['technical_break']][1]})

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=translate(user['language_code'], status[config['technical_break']][0]),
        reply_markup=MenuKeyboard.back_to(
            user,
            data=callback_data_admin_back_to_home,
            key_string='inline_back_to',
        )
    )

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data == callback_data_admin_params, is_admin=True)
def admin_back_to_home(call):
    """ Параметры обмена
    """
    user = db.get_user(call.from_user.id)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f'Params exchange',
        reply_markup=AdminKeyboard.params_exchange(user)
    )

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_back_to_home), is_admin=True)
def admin_back_to_home(call):
    """ Открывает панель администратора
        через callback кнопки
    """
    user = db.get_user(call.from_user.id)
    users_count = db.get_count(table='users')
    config = db.get_config()
    bot.delete_state(call.from_user.id)
    # Кол-во открытых сделок
    open_deals_count = db.get_count(
        table='deals',
        sql="""
           WHERE status IN ('new','accepted','process', 'paid')
        """
    )
    # Кол-во сделок оспариваемых
    duspute_deals_count = db.get_count(
        table='deals',
        sql="""
            WHERE status = 'dispute'
        """
    )
    # Кол-во открытых тикетов
    open_ticket_count = db.get_count(
        table='dialogs',
        sql="""
            WHERE status = 'open' AND type = 'support'
        """
    )

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f'Total users: {users_count}',
        reply_markup=AdminKeyboard.home(
            user,
            stats={
                'deals': open_deals_count,
                'dealsd': duspute_deals_count,
                'open_tickets': open_ticket_count
            },
            config=config
        )
    )
