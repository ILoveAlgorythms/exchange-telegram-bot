from loader import bot, db
from states.states import AdminDealSearch
from bot_locale.translate import translate
from keyboards.inline.menu import AdminKeyboard, MenuKeyboard
from telebot.formatting import escape_markdown, escape_html
from utils.message_templates import get_admin_deal_text

callback_data_admin_search_deal = 'admin.search_deals'
callback_data_admin_search = 'admin.search_deal_' # by_id
callback_data_admin_work_open_deal = 'admin.open_work_deal_'

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data == callback_data_admin_search_deal, is_admin=True)
def admin_search(call):
    """ Открывает параметры
        поиска ордеров (по айди ордера или показать все ордера юзера)
    """
    user = db.get_user(call.from_user.id)

    bot.delete_state(call.from_user.id)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=translate(user['language_code'], 'admin_search_home'),
        reply_markup=AdminKeyboard.search(user)
    )

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_search), is_admin=True)
def admin_search(call):
    """ Задаёт состояние поиску
        (поиск сделки по id или сделок пользователя по id/username)
    """
    user = db.get_user(call.from_user.id)
    calldata = call.data.replace(callback_data_admin_search, "")
    msg = "Empty"

    if calldata == 'by_id':
        msg = translate(user['language_code'], 'admin_search_by_id_home')
        bot.set_state(call.from_user.id, AdminDealSearch.by_id)

    if calldata == 'by_username_or_uid':
        msg = translate(user['language_code'], 'admin_search_by_user_deals_home')
        bot.set_state(call.from_user.id, AdminDealSearch.uid_or_uname)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=msg,
        reply_markup=MenuKeyboard.back_to(
            user,
            key_string='inline_back_to',
            data=callback_data_admin_search_deal
        )
    )


@bot.message_handler(is_chat=False, state=AdminDealSearch.by_id, is_admin=True)
def search_deal_by_id(message):
    """ Поиск сделки по ID
        Вернёт сделку, если есть совпадение
    """
    user = db.get_user(message.from_user.id)
    lang = user['language_code']
    deal = db.get_deal(message.text)

    if deal is None:
        # Если сделка не нашлась
        bot.send_message(
            message.from_user.id,
            text=translate(lang, 'admin_search_deal_not_found'),
            reply_markup=MenuKeyboard.back_to(
                user,
                key_string='inline_back_to',
                data=callback_data_admin_search_deal
            )
        )
        return

    bot.send_message(
        message.from_user.id,
        get_admin_deal_text(user, deal),
        reply_markup=AdminKeyboard.deal(
            user,
            deal,
            back_menu=callback_data_admin_search_deal
        )
    )


@bot.message_handler(is_chat=False, state=AdminDealSearch.uid_or_uname, is_admin=True)
def search_deal_by_uid_or_uname(message):
    """ Поиск сделок пользователя
        Вернёт список сделок, если есть совпадение
    """
    user = db.get_user(message.from_user.id)
    lang = user['language_code']

    uid_or_uname = message.text.strip().replace("@", "").replace("#", "")
    user_deal = db.get_user(
        user_id=uid_or_uname,
        sql=f"""OR username = "{uid_or_uname}" """
    )
    deals = None
    text = ""

    if user_deal is None:
        text = translate(lang, 'admin_search_user_not_found')

    if user_deal is not None:
        deals = db.get_deals(data=user_deal['id'])

    if user_deal is not None and deals == []:
        text = translate(
            lang,
            'admin_search_deals_not_found'
        ).format(**{
            "telegram_id": user_deal['telegram_id'],
            "username": user_deal['username'],
        })

    if user_deal is None or deals == []:
        # Если сделка не нашлась
        bot.send_message(
            message.from_user.id,
            text=text,
            reply_markup=MenuKeyboard.back_to(
                user,
                key_string='inline_back_to',
                data=callback_data_admin_search_deal
            )
        )
        return

    text = translate(
        lang,
        'admin_search_deals_found'
    ).format(**{
        "telegram_id": user_deal['telegram_id'],
        "username": escape_markdown(user_deal['username']),
    })
    bot.send_message(
        message.from_user.id,
        text,
        reply_markup=AdminKeyboard.deals(
            user,
            deals,
            callback_data=callback_data_admin_work_open_deal,
        )
    )

    # bot.delete_state(message.from_user.id)
    # Не стал удалять состояние при успешном
    # поиске. Состояние сбросится самостоятельно
    # по кнопке "Назад" или по cmd /start
    # В текущей ситуации считаю это более практичным
    # нежели чем после каждого поиска заходить заново
    # в раздел с логами и выбирать нужный фильтр для поиска.
