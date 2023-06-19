from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from loader import db, me
from bot_locale.translate import translate

class AdminKeyboard:
    back_inline_keyboard = None

    @staticmethod
    def home(user, stats, config):
        """ Главное меню админки
        """
        lang = user['language_code']
        is_break = 'inline_bot_active' if config['technical_break'] == 1 else 'inline_bot_inactive'
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(translate(lang, 'inline_admin_orders').format(stats['deals']), callback_data='admin.open_deals')],
            [InlineKeyboardButton(translate(lang, 'inline_admin_problems_with_orders').format(stats['dealsd']), callback_data='admin.open_disput_deals')],
            [InlineKeyboardButton(translate(lang, 'inline_admin_support_requests').format(stats['open_tickets']), callback_data='admin.support_tickets')],
            [InlineKeyboardButton(translate(lang, 'inline_admin_logs'), callback_data='admin.search_deals')],
            [InlineKeyboardButton(translate(lang, is_break), callback_data='admin.params_change_techinal_break')],
        ])

        if 'admin' in user['role']:
            kb.add(InlineKeyboardButton(translate(lang, 'inline_admin_params_exchange'), callback_data='admin.params'))

        kb.add(InlineKeyboardButton(translate(lang, 'inline_back_to_main_menu'), callback_data='bot.back_to_main_menu'))

        return kb


    @staticmethod
    def countries(user, countries, callback_data, back_menu=True, back_menu_data='bot.back_to_main_menu', is_create=False):
        """ Выбора страны
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup()

        for country in countries:
            kb.row(
                InlineKeyboardButton(
                    f"{country['name']} ({country['slug']})",
                    callback_data=f'{callback_data}{country["id"]}'
                ),
                InlineKeyboardButton(
                    '❌',
                    callback_data=f'admin.params_country_delete_{country["id"]}'
                ),
            )

        if is_create:
            kb.add(
                InlineKeyboardButton(translate(lang, 'inline_create_country'), callback_data='admin.params_country_create')
            )

        if back_menu:
            kb.add(
                InlineKeyboardButton(translate(lang, 'inline_back_to'), callback_data=back_menu_data)
            )

        return kb


    @staticmethod
    def banks(user, banks, callback_data, back_menu=True, back_menu_data='bot.back_to_main_menu', is_create=False):
        """ Выбора банков
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup()

        for bank in banks:
            kb.row(
                InlineKeyboardButton(
                    bank['name'],
                    callback_data=f'{callback_data}{bank["id"]}'
                ),
                InlineKeyboardButton(
                    '❌',
                    callback_data=f'admin.params_bank_delete_{bank["id"]}'
                ),
            )

        if is_create:
            kb.add(
                InlineKeyboardButton(translate(lang, 'inline_create_bank'), callback_data='admin.params_bank_create')
            )

        if back_menu:
            kb.add(
                InlineKeyboardButton(translate(lang, 'inline_back_to'), callback_data=back_menu_data)
            )

        return kb

    @staticmethod
    def pairs(user, pairs, callback_data, back_menu_data='bot.back_to_main_menu', key_string_back_to='inline_back_to_main_menu'):
        """ Выбор валютных пар
        !-! Добавить пагинацию
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup(row_width=2)

        # Клавиатура с валютными парами
        # RUB -> EUR
        # EUR -> RUB
        for pair in pairs:
            pair_status = translate(lang, 'dict_pair_status')

            pair_status = pair_status['active'] if pair['is_active'] == 1 else pair_status['inactive']

            pair_name = translate(lang, 'inline_admin_exchange_pair_name').format(
                pair['from_name'],
                pair['to_name'],
                pair_status
            )
            kb.row(
                InlineKeyboardButton(
                    pair_name,
                    callback_data=f'{callback_data}{pair["id"]}'
                ),
                InlineKeyboardButton(
                    '❌',
                    callback_data=f'admin.params_pair_delete_{pair["id"]}'
                )
            )

        kb.add(
            InlineKeyboardButton(translate(lang, 'inline_create_pair'), callback_data='admin.params_pair_create')
        )

        kb.add(
            InlineKeyboardButton(translate(lang, key_string_back_to), callback_data=back_menu_data)
        )

        return kb

    @staticmethod
    def edit_pair(user, pair, params):
        """ Валютная пара (меню для редактирования)
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup()
        pair_id = str(pair['id'])
        pair_status_string = 'inline_admin_pair_active' if pair['is_active'] == 1 else 'inline_admin_pair_inactive'
        pair_auto_requisites_string = 'inline_admin_pair_auto_requisites_active' if pair['auto_requisites'] == 1 else 'inline_admin_pair_auto_requisites_inactive'

        for k, v in params.items():
            kb.add(
                InlineKeyboardButton(
                    translate(lang, v),
                    callback_data=f'admin.params_pair_edit_{k}|{pair_id}'
                ),
            )

        kb.add(
            InlineKeyboardButton(
                translate(lang, pair_auto_requisites_string),
                callback_data=f'admin.params_pair_edit_auto_requisites|{pair_id}'
            ),
        )

        kb.add(
            InlineKeyboardButton(
                translate(lang, pair_status_string),
                callback_data=f'admin.params_pair_edit_status|{pair_id}'
            ),
        )

        kb.add(
            InlineKeyboardButton(
                translate(lang, 'inlint_delete_pair'),
                callback_data=f'admin.params_pair_delete_{pair_id}'
            ),
        )

        kb.add(
            InlineKeyboardButton(
                translate(lang, 'inline_back_to'),
                callback_data='admin.params_pairs'
            ),
        )

        return kb

    @staticmethod
    def params_exchange(user):
        """ Настройки бота
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(translate(lang, 'inline_admin_countries'), callback_data='admin.params_countries'), InlineKeyboardButton(translate(lang, 'inline_admin_banks'), callback_data='admin.params_banks')],
            [InlineKeyboardButton(translate(lang, 'inline_admin_pairs'), callback_data='admin.params_pairs'), InlineKeyboardButton(translate(lang, 'inline_admin_pages'), callback_data='admin.pages')],
            [InlineKeyboardButton(translate(lang, 'inline_params_limits'), callback_data='admin.params_limits'), InlineKeyboardButton(translate(lang, 'inline_params_rooms'), callback_data='admin.params_rooms')],
            [InlineKeyboardButton(translate(lang, 'inline_params_export'), callback_data='admin.params_export'), InlineKeyboardButton(translate(lang, 'inline_params_affilate_program'), callback_data='admin.params_affilate')],
            [InlineKeyboardButton(translate(lang, 'inline_back_to'), callback_data='admin.back_to_home')],
        ])

        return kb

    @staticmethod
    def deals(user, deals, callback_data, back_menu=True):
        """ Список сделок в админке
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup()
        deal_status = translate(lang, 'dict_deal_status')

        if len(deals) == 0:
            kb.add(
                InlineKeyboardButton(
                    translate(lang, 'deals_not_found'),
                    callback_data='bot.none'
                )
            )

        for deal in deals:
            kb.add(
                InlineKeyboardButton(
                    f"№{deal['id']} {deal_status[deal['status']]} {deal['from_amount']} {deal['from_name']} ({deal['from_bank_name']}) -> {deal['to_amount']} {deal['to_name']} ({deal['to_bank_name']}) ",
                    callback_data=f'{callback_data}{deal["id"]}'
                )
            )

        kb.add(
            InlineKeyboardButton(translate(lang, 'inline_back_to'), callback_data='admin.back_to_home')
        )


        return kb

    @staticmethod
    def tickets(user, tickets, callback_data, back_menu=True):
        """ Список тикетов
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup()

        if len(tickets) == 0:
            kb.add(
                InlineKeyboardButton(
                    translate(lang, 'tickets_not_found'),
                    callback_data='bot.none'
                )
            )

        for ticket in tickets:
            ticket_user = db.get_user(ticket['user_id'], name_id="id")
            kb.add(
                InlineKeyboardButton(
                    f"№{ticket['id']} / {ticket['title']}",
                    callback_data=callback_data+str(ticket['id'])
                )
            )

        kb.add(
            InlineKeyboardButton(translate(lang, 'inline_back_to'), callback_data='admin.back_to_home')
        )


        return kb

    @staticmethod
    def search(user):
        """ Парамертры сделки
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup()


        kb.row(
            InlineKeyboardButton(
                translate(lang, 'inline_admin_search_id'),
                callback_data='admin.search_deal_by_id'
            ),
        )

        kb.row(
            InlineKeyboardButton(
                translate(lang, 'inline_admin_search_username_or_uid'),
                callback_data='admin.search_deal_by_username_or_uid'
            ),
        )

        kb.add(
            InlineKeyboardButton(translate(lang, 'inline_back_to'), callback_data='admin.back_to_home')
        )

        return kb

    @staticmethod
    def deal(user, deal, back_menu='admin.open_deals'):
        """ Парамертры сделки
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup()

        if deal['status'] == 'new':
            kb.add(
               InlineKeyboardButton(translate(lang, 'inline_deal_change_status_accept'), callback_data='admin.deal_change_status_accepted_'+str(deal['id']))
            )

        if deal['status'] in ['accepted']: # maybe 'paid'
            kb.add(
               InlineKeyboardButton(translate(lang, 'inline_deal_change_status_process'), callback_data='admin.deal_change_status_process_'+str(deal['id']))
            )

        if deal['status'] in ['accepted', 'process', 'dispute', 'paid', 'declined', 'completed']:
            kb.add(
               InlineKeyboardButton(translate(lang, 'inline_deal_open_chat'), callback_data='admin.deal_open_chat_'+str(deal['id']))
            )

        if deal['status'] in ['accepted', 'dispute', 'paid', 'declined']:
            kb.add(
               InlineKeyboardButton(translate(lang, 'inline_deal_change_status_completed'), callback_data='admin.deal_change_status_completed_'+str(deal['id']))
            )

        if deal['status'] in ['new', 'accepted', 'process', 'dispute', 'paid']:
            kb.add(
               InlineKeyboardButton(translate(lang, 'inline_deal_change_status_decline'), callback_data='admin.deal_change_status_declined_'+str(deal['id']))
            )

        if deal['status'] in ['completed'] and deal['profit'] == 0:
            kb.add(
               InlineKeyboardButton(translate(lang, 'inline_deal_input_profit'), callback_data='admin.deal_set_profit_'+str(deal['id']))
            )

        if deal['status'] == 'dispute':
            back_menu = 'admin.open_disput_deals'

        kb.add(
           InlineKeyboardButton(translate(lang, 'inline_back_to'), callback_data=back_menu)
        )

        return kb

    @staticmethod
    def ticket(user, ticket, back_menu='admin.support_tickets'):
        """ Парамертры тикета
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup()

        kb.add(
           InlineKeyboardButton(translate(lang, 'inline_ticket_open_chat'), callback_data='admin.ticket_open_chat_'+str(ticket['id']))
        )

        if ticket['status'] == 'open':
            kb.add(
               InlineKeyboardButton(translate(lang, 'inline_ticket_change_status_answered'), callback_data='admin.ticket_change_status_answered_'+str(ticket['id']))
            )

        kb.add(
           InlineKeyboardButton(translate(lang, 'inline_back_to'), callback_data=back_menu)
        )

        return kb


    @staticmethod
    def pages(user, pages):
        """ Страницы
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup()

        for page in pages:
            kb.row(
                InlineKeyboardButton(
                    page['page_title'],
                    callback_data='admin.pages.preview_'+str(page['id'])
                ),
            )

        kb.add(
            InlineKeyboardButton(
                translate(lang, 'inline_back_to'),
                callback_data='admin.params'
            ),
        )

        return kb

    @staticmethod
    def page_edit(user, page):
        """ Страницы
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup()

        kb.add(
            InlineKeyboardButton(
                translate(lang, 'inline_admin_edit_page'),
                callback_data='admin.pages.edit_'+str(page['id'])
            ),
            InlineKeyboardButton(
                translate(lang, 'inline_admin_attachment_document_page'),
                callback_data='admin.pages.add_document_page_'+str(page['id'])
            )
        )

        if page['document'] != 'null':
            kb.add(
                InlineKeyboardButton(
                    translate(lang, 'inline_admin_delete_document_page'),
                    callback_data='admin.pages.delete_document_page_'+str(page['id'])
                )
            )

        kb.add(
            InlineKeyboardButton(
                translate(lang, 'inline_back_to'),
                callback_data='admin.pages'
            ),
        )

        return kb

    @staticmethod
    def page_country(user, country):
        """ Страницы
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup()

        kb.add(
            InlineKeyboardButton(
                translate(lang, 'inline_admin_edit_country_name'),
                callback_data='admin.params_country_edit_name_'+str(country['id'])
            )
        )

        kb.add(
            InlineKeyboardButton(
                translate(lang, 'inline_admin_edit_country_code'),
                callback_data='admin.params_country_edit_slug_'+str(country['id'])
            )
        )

        kb.add(
            InlineKeyboardButton(
                translate(lang, 'inline_back_to'),
                callback_data='admin.params_countries'
            ),
        )

        return kb

    @staticmethod
    def edit_bank(user, bank):
        """ Банк
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup()

        kb.add(
            InlineKeyboardButton(
                translate(lang, 'inline_admin_edit_bank_name'),
                callback_data='admin.params_bank_edit_name_'+str(bank['id'])
            )
        )

        kb.add(
            InlineKeyboardButton(
                translate(lang, 'inline_admin_edit_bank_country'),
                callback_data='admin.params_bank_edit_country_'+str(bank['id'])
            )
        )

        kb.add(
            InlineKeyboardButton(
                translate(lang, 'inline_admin_edit_bank_slug'),
                callback_data='admin.params_bank_edit_slug_'+str(bank['id'])
            )
        )

        kb.add(
            InlineKeyboardButton(
                translate(lang, 'inline_admin_add_bank_accoount'),
                callback_data='admin.params_bank_add_bank_account_'+str(bank['id'])
            )
        )

        kb.add(
            InlineKeyboardButton(
                translate(lang, 'inline_admin_stats_bank_accoount'),
                callback_data='admin.params_bank_stats_bank_accounts_'+str(bank['id'])
            )
        )

        kb.add(
            InlineKeyboardButton(
                translate(lang, 'inline_back_to'),
                callback_data='admin.params_banks'
            ),
        )

        return kb

class MenuKeyboard:
    """ Клавиатуры
    """
    @staticmethod
    def home(user):
        """ Главное меню
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(translate(lang, 'inline_new_exchange'), callback_data='bot.set.new_exchange'),
            InlineKeyboardButton(translate(lang, 'inline_my_exchanges'), callback_data='bot.main.my_exchanges')],
            [InlineKeyboardButton(translate(lang, 'inline_faq'), callback_data='bot.main.page.faq'),
            InlineKeyboardButton(translate(lang, 'inline_support'), callback_data='bot.main.support')],
            [InlineKeyboardButton(translate(lang, 'inline_affilate_program'), callback_data='bot.main.affilate_program')],
        ])

        if user['role'] in ['manager', 'admin']:
            kb.add(
                InlineKeyboardButton(translate(lang, 'inline_admin_panel'), callback_data='admin.back_to_home')
            )

        return kb

    @staticmethod
    def back_to(user, key_string=None, data=None):
        """ Возврат в главное меню
        """
        lang = user['language_code']
        translate_string_key = 'inline_back_to_main_menu'
        callback_data = 'bot.back_to_main_menu'

        if key_string is not None:
            translate_string_key = key_string

        if data is not None:
            callback_data = data

        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(translate(lang, translate_string_key), callback_data=callback_data)]
        ])
        return kb

    @staticmethod
    def exchange_accept_or_decline(user):
        """ Принятие/отклонение
            условий обмена (создание сделки)
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(translate(lang, 'inline_exchange_decline'), callback_data='bot.back_to_main_menu'),
                InlineKeyboardButton(translate(lang, 'inline_exchange_accept'), callback_data='bot.set.exchage_accept'),
            ]
        ])
        return kb

    @staticmethod
    def agreement_accept_or_decline(user):
        """ Соглашение с условиями сервиса

        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(translate(lang, 'inline_exchange_decline_agreement'), callback_data='bot.back_to_main_menu'),
                InlineKeyboardButton(translate(lang, 'inline_exchange_accept_agreement'), callback_data='bot.accept_agreement'),
            ]
        ])
        return kb

    @staticmethod
    def ticket_create_or_decline(user):
        """ Отправка/отклонение
            запроса в поддержку
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(translate(lang, 'inline_send_message_to_support'), callback_data='bot.support.create.accept'),
                InlineKeyboardButton(translate(lang, 'inline_decline_message_to_support'), callback_data='bot.main.support'),
            ]
        ])
        return kb

    @staticmethod
    def support(user):
        """ Отправка/отклонение
            запроса в поддержку
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(translate(lang, 'inline_create_support_ticket'), callback_data='bot.support.create')],
            [InlineKeyboardButton(translate(lang, 'inline_back_to'), callback_data='bot.back_to_main_menu')]
        ])
        return kb

    @staticmethod
    def accept_or_decline(user, cl_accept, cl_decline, key_string_accept='inline_send', key_string_decline='inline_back_to'):
        """ Отправка/отклонение
            действия
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(translate(lang, key_string_accept), callback_data=cl_accept)],
            [InlineKeyboardButton(translate(lang, key_string_decline), callback_data=cl_decline)],
        ])
        return kb

    @staticmethod
    def reply_keyboard_parse(items):
        kb = ReplyKeyboardMarkup(one_time_keyboard=True)

        for item in items:
            kb.add(KeyboardButton(item))

        return kb

    @staticmethod
    def notification_deal(user, order_id):
        """ Клавиатуры для перехода в бот из
            группы уведомлений (СДЕЛКИ)
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(translate(lang, 'inline_admin_notification_get_deal'), url=f'https://t.me/{me.username}?start=order{order_id}'),
            ]
        ])
        return kb

    @staticmethod
    def notification_ticket(user, ticket_id):
        """ Клавиатуры для перехода в бот из
            группы уведомлений (ТИКЕТЫ В ПОДДЕРЖКУ)
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(translate(lang, 'inline_admin_notification_get_ticket'), url=f'https://t.me/{me.username}?start=ticket{ticket_id}'),
            ]
        ])
        return kb

    @staticmethod
    def pairs(user, pairs, callback_data, back_menu=True, back_menu_data='bot.back_to_main_menu', key_string_back_to='inline_back_to_main_menu', is_create=False):
        """ Выбор валютных пар
        !-! Добавить пагинацию
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup(row_width=2)

        # Клавиатура с валютными парами
        # RUB -> EUR
        # EUR -> RUB
        for pair in pairs:
            pair_name = translate(lang, 'inline_exchange_pair_name').format(
                pair['from_name'],
                pair['to_name']
            )
            kb.row(
                InlineKeyboardButton(
                    pair_name,
                    callback_data=f'{callback_data}{pair["id"]}'
                )
            )

        if is_create:
            kb.add(
                InlineKeyboardButton(translate(lang, 'inline_create_pair'), callback_data='admin.params_pair_create')
            )

        if back_menu:
            kb.add(
                InlineKeyboardButton(translate(lang, key_string_back_to), callback_data=back_menu_data)
            )

        return kb

    @staticmethod
    def banks(user, banks, callback_data, back_menu=True, back_menu_data='bot.back_to_main_menu', is_create=False):
        """ Выбора банков
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup()

        for bank in banks:
            kb.add(
                InlineKeyboardButton(
                    bank['name'],
                    callback_data=f'{callback_data}{bank["id"]}'
                )
            )

        if is_create:
            kb.add(
                InlineKeyboardButton(translate(lang, 'inline_create_bank'), callback_data='admin.params_bank_create')
            )

        if back_menu:
            kb.add(
                InlineKeyboardButton(translate(lang, 'inline_back_to'), callback_data=back_menu_data)
            )

        return kb

    @staticmethod
    def countries(user, countries, callback_data, back_menu=True, back_menu_data='bot.back_to_main_menu', is_create=False):
        """ Выбора страны
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup()

        for country in countries:
            kb.add(
                InlineKeyboardButton(
                    f"{country['name']} ({country['slug']})",
                    callback_data=f'{callback_data}{country["id"]}'
                )
            )

        if is_create:
            kb.add(
                InlineKeyboardButton(translate(lang, 'inline_create_country'), callback_data='admin.params_country_create')
            )

        if back_menu:
            kb.add(
                InlineKeyboardButton(translate(lang, 'inline_back_to'), callback_data=back_menu_data)
            )

        return kb

    @staticmethod
    def deals(user, deals, callback_data, back_menu=True):
        """ Сделки пользователя
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup()
        deal_status = translate(lang, 'dict_deal_status')

        if len(deals) == 0:
            kb.add(
                InlineKeyboardButton(
                    translate(lang, 'deals_not_found'),
                    callback_data='bot.none'
                )
            )

        for deal in deals:
            kb.add(
                InlineKeyboardButton(
                    f"{deal_status[deal['status']]} {deal['from_amount']} {deal['from_name']} ({deal['from_bank_name']}) -> {deal['to_amount']} {deal['to_name']} ({deal['to_bank_name']}) ",
                    callback_data=f'{callback_data}{deal["id"]}'
                )
            )

        kb.add(
            InlineKeyboardButton(translate(lang, 'inline_back_to'), callback_data='bot.back_to_main_menu')
        )

        return kb

    @staticmethod
    def reply_exchange_cancel(user):
        """ Отмена сделки
        """
        lang = user['language_code']
        finish_exchange = ReplyKeyboardMarkup(resize_keyboard=True)
        finish_exchange.add(KeyboardButton(translate(lang, 'reply_exchange_cancel')))

        return finish_exchange

    @staticmethod
    def smart(json, row_width=1):
        """ Кастомная клавиатура из JSON
        """
        from telebot.util import quick_markup

        return quick_markup(json, row_width=row_width)

    @staticmethod
    def remove_reply():
        """ Удаляет reply-клавиатуру
        """
        return ReplyKeyboardRemove(selective=False)


class ChatKeyboard:
    @staticmethod
    def home(user, chat_id, config):
        """ Главное меню в чате
            Подключение уведомлений
        """
        lang = user['language_code']
        kb = InlineKeyboardMarkup()
        status_text = translate(user['language_code'], 'dict_notifications_status')

        # Уведомления о новых сделках
        dn_status = status_text['connected'] if chat_id == config['notifications_deal_chat_id'] else status_text['unconeccted']
        # Уведомления о тикетах поддержки
        sn_status = status_text['connected'] if chat_id == config['notifications_support_chat_id'] else status_text['unconeccted']

        kb.add(
            InlineKeyboardButton(dn_status + translate(lang, 'inline_enabled_deals_notifications'), callback_data='admin.chat.notifications_switch_deals')
        )
        kb.add(
            InlineKeyboardButton(sn_status + translate(lang, 'inline_enabled_support_notifications'), callback_data='admin.chat.notifications_switch_support')
        )

        return kb
