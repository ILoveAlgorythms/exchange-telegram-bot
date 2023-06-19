from loader import config

# Принцип работы: словарь
# Формат:         locales[КодЯзыка][ЯзыковаяСтрока]
# Стиль:          Markdown
locales = {}

locales['ru'] = {
    'access_denied': '⛔ У вас нет прав для совершения этого действия',

    'warning_deal_manager_is_exists': '⚠️ Вы не можете изменять статус этой сделки. Эта сделка принадлежит другому менеджеру.',

    'exchange_comment_input_to_requisites': '\n\n*Комментарий:* {0}',

    'exchange_select_pair': 'Выберите валютную пару для обмена.',

    'start_text': '💰 Добро пожаловать! Выберите подходящий пункт в меню.',

    'exchange_select_from_bank_country': 'Выберите страну из которой будете отправлять {0}.',

    'exchange_select_to_bank_country': 'Выберите страну в которой находится ваш банковский счёт для получения {0}.',

    'exchange_select_to_bank': '🏦 Выберите банк, на который хотите получить *{0}*.',

    'exchange_select_to_network': '💎 Выберите сеть, в которой хотите получить *{0}*.',

    'exchange_select_from_network': '💎 Выберите сеть, из которой будете отправлять *{0}*.',

    'exchange_select_from_bank': '🏦 Выберите банк, в который хотите отправить *{0}*.',

    'exchange_input_from_amount': 'Введите сумму в *{0}*, которую хотите обменять на *{1}*.\n\n*Сумма:* {2}-{3} {0}',

    'exchange_input_to_amount': 'Введите сумму в *{0}*. Сумма автоматически конвертируется в *{1}*.\n\n*Сумма:* {2}-{3} {0}',

    'exchange_issuing_quotes': '⚠️ Вы готовы купить *{to_amount} {to_name}* за *{from_amount} {from_name}* по курсу *{rate_from_amount} {rate_from_name} = {rate_to_amount} {rate_to_name}*?\n\n💱 {from_bank_name} ({from_name}) *->* {to_bank_name} ({to_name})\n📄 Реквизиты {to_bank_name}: {to_bank_requisites}\n\n👉 Вы также подтверждаете, что согласны с условиями сервиса. Ознакомиться можно здесь: /agreement',

    'exchange_input_to_card_cumber': 'Введите номер банковской карты *{0}* на которую вы получите *{1}*.',

    'exchange_input_to_wallet_address': 'Введите адрес кошелька *{0}* на который вы получите *{1}*.',

    'page_not_found': 'Страница не найдена.',

    'deals_not_found': '⚠️ Нет сделок для отображения',

    'tickets_not_found': '⚠️ Нет тикетов для отображения',

    'admin_tickets_home': '📩 Список активных тикетов в поддержку',

    'exchange_deal_introduction': '👇 Ознакомьтесь внимательно с введёнными данными.',

    'error_data_not_valid': '🚫 Ошибка: Введены неверные данные.',

    'admin_deal_profit_fixed': '✅ Прибыль зафиксирована',

    'chapter_my_exchanges': '📋 *Мои сделки*\n\n🆕 — ожидает подтверждения менеджером;\n⚪ — в процессе;\n🟢 — завершённые сделки;\n🔴 — отменённые сделки.',

    'chapter_support': '📩 *Поддержка*\n\nЗаявки обрабатываются в течении 2-6 часов.',

    'exchange_deal_created': '🆕 *Сделка* `№{id}` *создана*\n\n*Отдаю:* {from_amount} {from_name} ({from_bank_name})\n*Получаю:* {to_amount} {to_name} ({to_bank_name})\n\n*Реквизиты {to_bank_name}:* `{requisites}`\n\n❗️ Ожидайте подтверждения сделки менеджером и выдачи реквизитов для оплаты.',

    # 'exchange_deal_created_notification': '🆕 *Сделка* `№{0}` *создана*\n\n*Пользователь:* @{1}\n*Отдаёт:* {2} {3}\n*Получает:* {4} {5}\n*Банк получателя:* {6}\n*Реквизиты получателя:* {7}\n\n',

    'my_exchange_deal_info': '📋 *Информация о сделке* `№{id}`\n\n*Отдаю:* {from_amount} {from_name} ({from_bank_name})\n*Получаю:* {to_amount} {to_name} ({to_bank_name})\n*Курс:* 1 {to_name} = {from_exchange_rate} {from_name}\n\n*Реквизиты {to_bank_name}:*\n{requisites}\n\n*Статус*: {status_emoji} {status_text}\n*Создано*: {datetime}\n*Обновлено:* {update_datetime}',

    'chat_home_notifications': '🔔 *Уведомления*\n\nВыберите какие уведомления хотите получать в этом чате. Можно подключить сразу все. Уведомления выбранной категории автоматически отключатся в этом чате (бот уведомит об этом) при переподключении его в другом чате.\n\n❗️ Чтобы не собирать все заявки в одну кучу, рекомендуется разделить чаты.',

    'chat_swith_notify_deals': '⚠️ Уведомленя о сделках были подключены в этом чате',

    'chat_swith_disabled_notify_deals': '⚠️ Уведомленя о сделках были отключены в этом чате',

    'chat_swith_notify_support': '⚠️ Уведомленя о тикетах в поддержку были подключены в этом чате',

    'chat_swith_disabled_notify_support': '⚠️ Уведомленя о тикетах в поддержку были отключены в этом чате',

    'bot_reply_cancel_action': '❌ Действие было отменено',

    'bot_agreement_is_accepted': '✅ Соглашение подтверждено',

    'user_deal_send_requisites': '💳 Введите реквизиты оплаты для пользователя по сделке №4 ({from_amount} {from_name} ({from_bank_name}) -> {to_amount} {to_name} ({to_bank_name}))',

    'user_deal_send_requisites_confirmation': '*Реквизиты для оплаты:*\n{0}\n\n❓ Отправляем их пользователю?',

    'user_deal_send_requisites_message': '⚪ *Сделка* `№{id}`\n\nПереведите *{from_amount} {from_name}* из *{from_bank_name}* для получения *{to_amount} {to_name}* на *{to_bank_name}*.\n\n*Реквизиты для оплаты:* `{requisites}`\n\n❗️ Совершите платёж в течении 15 минут. Сделка будет автоматически отменена системой по истечению указанного срока оплаты.',

    'user_deal_send_requisites_success': '✅ Реквизиты были отправлены пользователю, ожидайте подтверждения оплаты с его стороны.',

    'user_deal_accept_confirmation_or_message': '❗️ Если менеджер запросил скриншот об оплате или другую информацию, прикрепите её на этом этапе одним сообщением.',

    'user_deal_add_data_success': '✅ Данные были прикреплены.',

    'user_deal_change_status_paid': '✅ Вы отметили сделку `№{0}` как оплаченную.\n\nОжидайте ответ менеджера.',

    'admin_deal_set_profit': '📈 *Введите прибыль полученную от сделки*\n\nУкажите её в поддерживаемом активе. *{0}*, *{1}* или *{2}*\n\nПример: 10 {2} / 10.55 {0} / 10,12 {1}',

    'user_deal_change_status_paid_notification': '✅ Сделка `№{id}` оплачена\n\n*{from_amount} {from_name}* были переведены на *{from_bank_name}*\n\n❗️ Пользователь отметил сделку как *оплаченная*. Проверьте корректность этой информации.',

    'deal_accepted_manager': '👌 *Сделка* №`{0}` *принята в работу*\n\nМенеджер отправит реквизиты для оплаты в течении нескольких минут.',

    'deal_message_manager': '⚠️ Сообщение от менеджера по сделке `№{id}`\n\n*Сообщение:*\n{message}',

    'ticket_message_manager': '⚠️ Сообщение от менеджера по заявке `№{id}`\n\n*Сообщение:*\n{message}',

    'deal_declined_manager': '❌ Сделка `№{0}` была отменена менеджером.\n\n Приносим свои извинения.',

    'deal_declined_time_exceed': '❌ Сделка `№{0}` отменена.\n*Причина*: истекло время ожидания.\n\n\n Приносим свои извинения.',

    'deal_not_available': '❌ Это действие недоступно с указанной сделкой.',

    'deal_file_not_supported': '❌ Формат данных некорректен.\n\nПрикрепите фото, видео или документ с описанием.',

    'deal_completed_user': '✅ *Сделка* `№{id}` *исполнена*\n\n*{to_amount} {to_name}* были переведены на *{to_bank_name}*.\n\n❗️ Если средства не поступили на ваш счёт или возникли другие вопросы, откройте спор.',

    'user_support_select_reason': '💬 Выберите тему обращения.',

    'user_support_input_message': '💬 Введите ваше сообщение для менеджера.',

    'user_support_finally_ticket': '💬 *Создание тикета*\n\n*Причина:* {0}\n*Сообщение:*\n{1}',

    'user_support_ticket_created': '☑️ *Тикет №{0} создан*\n\nВ ближайшее время с вами свяжется наш менеджер.',

    'user_support_ticket_created_notification': '☑️ *Тикет №{0}*\n\n*Причина:* {1}\n*Сообщение:* {2}',

    'user_from_notification_view_deal': '📋 Откройте сделку `№{id}`',

    'user_from_notification_view_ticket': '☑️ Откройте тикет `№{id}`',


    'admin_search_deal_not_found': '😔 Сделка не найдена, попробуйте ввести другой ID.',

    'admin_search_user_not_found': '😔 Пользователь не найден',

    'admin_user_is_unban': '✅ Пользователь `{0}` (@{1}) разбанен',

    'admin_user_is_banned': '✅ Пользователь `{0}` (@{1}) забанен',

    'admin_search_deals_not_found': '😔 Сделок у пользователя [{telegram_id}](tg://user?id={telegram_id}) (@{username}) не найдено.',

    'admin_search_deals_found': '📋 Список последних сделок пользователя [{telegram_id}](tg://user?id={telegram_id}) (@{username})',


    'admin_page_edit_text': '⚠️ Введите новый текст для страницы *{0}*',
    'admin_page_add_document': '⚠️ Прикрепите документ для страницы *{0}*',
    'admin_page_document_attached': '✅ Документ к странице *{0}* успешно прикреплён',
    'admin_page_document_deleted': '✅ Документ у страницы *{0}* успешно удалён',

    'admin_page_edit_country_name': '⚠️ Введите новое название страны *{0}*',
    'admin_page_edit_country_code': '⚠️ Введите новый код страны *{0}*',

    'admin_page_edit_bank_name': '⚠️ Введите новое название банка *{0}*',
    'admin_page_edit_bank_country': '⚠️ Введите новый код банка *{0}*',
    'admin_page_edit_bank_slug': '⚠️ Введите новый slug банка *{0}*',

    'admin_page_home': '📑 Список страниц для редактирования.',

    'admin_page_edit_home': '📑 Редактирование страницы *{0}*\n\n*Cодержимое:*\n{1}',

    'admin_page_banks': '🏦 Список банков для редактирования.',

    'admin_page_countries': '🗺 Список стран для редактирования.',

    'admin_country_edit_home': '🌎 Редактирование страны\n\n*Название*: {0}\n*Код:* {1}',

    'admin_bank_edit_home': '🏦 Редактирование банка\n\n*Название*: {0}\n*Код страны:* {1}\n\n*Идентификатор:* {2}\n\n*Прикреплённые счета (с оборотом за всё время):*',

    'admin_data_bank_add_accounts': '💳 *Добавление счетов для {bank_name}*\n\nВводите данные счета в следующем формате: _Номер счёта, ФИО дропа (инфа), Лимит акка в сутки (числом)_\n\nВы можете добавлять несколько счетов, просто вводите каждый с новой строки.\n\n_Например:\n427655000001111, Кириенко Григорий Васильевич, 10000\n427655000002222, Семёнов Семён Олегович, 1000_',
    'admin_data_bank_add_accounts_success': '✅ *Счета успешно добавлены*',
    'admin_data_bank_all_stroke': '\n\nВсе счета были успешно добавлены',
    'admin_data_bank_not_all_stroke': '\n\nНе все счета были успешно добавлены, строки ниже не соответствуют требуемому формату:\n',

    'admin_page_pairs': '💱 Список валютных пар для редактирования.',

    'admin_page_success_edit': '✅ Текст страницы *{0}* обновлён',

    'admin_limit_success_edit': '✅ Лимит успешно обновлён',

    'admin_data_success_edit': '✅ Данные были успешно обновлены',
    'admin_data_parameters_not_found': '⚠️ Входные параметры для команды не были указаны',

    'admin_data_pair_view': '💱 *Информация о паре {from_name} -> {to_name}*\n\n*Отдаю:* {from_name}\n*Тип:* {from_type}\n*Страна банков:* {from_country_code}\n*Мин. сумма:* {min_from_amount} {from_name}\n*Макс. сумма:* {max_from_amount} {from_name}\n\n*Получаю:* {to_name}\n*Страна банков:* {to_country_code}\n*Комментарий для ввода реквизитов:* {to_requisites_comment}\n*Тип:* {to_type}\n\n*Спред:* {spread}%\n\n*Парсер цен:* {price_handler}\n*from_handler_name:* {from_handler_name}\n*to_handler_name:* {to_handler_name}\n*handler_inverted:* {handler_inverted}\n\n*Создана:* {created_at}\n*Обновлена:* {updated_at}\n\n⬇️ __Выберите параметр для редактирования.__',

    'admin_data_pair_delete': '💱 Вы действительно хотите удалить пару *{from_name} -> {to_name}*?\n\n⛔ __Действие невозможно отменить.__',

    'admin_data_pair_delete_success': '✅ Пара *{from_name} -> {to_name}* удалена.',

    'admin_data_bank_delete': '🏦 Вы действительно хотите удалить банк *{name}*?\n\n⛔ __Действие невозможно отменить.__',

    'admin_data_bank_delete_success': '✅ Банк *{name}* удален.',

    'admin_data_country_delete': '🌐 Вы действительно хотите удалить страну *{name}*?\n\n⛔ __Действие невозможно отменить.__',

    'admin_data_country_delete_success': '✅ Страна *{name}* удален.',

    'admin_search_home': '🔎 *Поиск сделок*\n\nПервый фильтр отобразит данные о сделке по ID, второй покажет последние сделки пользователя для идентификации.',

    'admin_ticket_view': '*Информация по тикету* `№{id}`\n\n*Пользователь:* [{telegram_id}](tg://user?id={telegram_id}) (@{username})\n*Причина:* {ticket_title}\n*Обращение:*\n{ticket_text}\n\n*Статус*: {status}\n*Создан:* {created_at}',
    'admin_ticket_update': '*Статус тикета* `№{id}` обновлён',

    'admin_search_by_id_home': '🔎 Введите числовой идентификатор сделки',

    'admin_search_by_user_deals_home': '🔎 Введите telegram id или логин пользователя для отображения сделок',

    'admin_deal_send_requisites': '💳 Введите реквизиты пользователю [{telegram_id}](tg://user?id={telegram_id}) (@{username}) для перевода *{from_amount} {from_name}* на *{from_bank_name}* по сделке `№{id}`',

    'admin_exchange_deal_info': '📋 *Информация по сделке* `№{id}`\n\n*Менеджер:* {manager}\n*Пользователь:* [{telegram_id}](tg://user?id={telegram_id}) (@{username})\n\n*Отдаёт:* {from_amount} {from_name} ({from_bank_name})\n*Получает:* {to_amount} {to_name} ({to_bank_name})\n*Курс:* 1 {to_name} = {from_exchange_rate} {from_name}\n\n*Реквизиты {from_bank_name}:*\n`{from_requisites}`\n*Реквизиты {to_bank_name}:*\n`{requisites}`\n\n*Спред:* {spread}%\n*Прибыль:* {profit} {profit_asset}\n\n*Статус:* {status_emoji} {status_text}\n*Создано:* {datetime}\n*Обновлено:* {update_datetime}',

    'user_data': '[{telegram_id}](tg://user?id={telegram_id}) (@{username})',

    'deal_create_disput_start': '📋 *Открытие спора по сделке* `№{id}`\n\nПожалуйста, укажите как можно больше полезной информации для менеджера. Это поможет эффективно решить вашу проблему. При желании вы можете прикрепить фото, видео или документ.',

    'deal_chat_start': '📋 *Чат по сделке* `№{id}` *открыт*\n\nВведите сообщение.',

    'ticket_chat_start': '📋 *Чат по тикету* `№{id}` *открыт*\n\nВведите сообщение.',

    'deal_chat_message_added': '📋 *Чат по сделке* `№{id}`\n\nСообщение прикреплено.',

    'deal_create_disput_data_pinned': '📋 *Данные прикреплены* `№{id}`\n\Отправляем заявку менеджеру?',

    'deal_create_disput_data_created': '📋 *Спор по сделке* `№{id}` *открыт*\n\n❗️ Ожидайте ответа менеджера в ближайшее время.',

    'deal_chat_send_message_success': 'Сообщение отправлено. При желании можете ввести ещё или вернуться к сделке.',
    'ticket_chat_send_message_success': 'Сообщение отправлено. При желании можете ввести ещё или вернуться к тикету.',
    'deal_chat_send_manager_message_success': '💬 Сообщение отправлено. Ожидайте ответа.',

    'deal_create_disput_data_created_notification': '📋 *Открыт спор по сделке* `№{id}`',
    'edit_pair_parameter': '⚠️ Введите новое значение для параметра `{0}`',

    'exceed_limit_deal': '⚠️ Вы не можете создавать несколько заявок одновременно',

    'exceed_limit_ticket': '⚠️ Тикеты можно создавать только раз в 5 минут',

    'user_is_banned': '⚠️ Ваш аккаунт заблокирован. Вы не можете совершать сделки и использовать функции бота.',

    'deal_system_canceled': '❌ *Сделка* `№{id}` *отменена системой*\n\nВы не произвели оплату в течении указанного времени. За дополнительной информацией обратитесь в службу поддержки.',

    'create_pair_success': '💸 Пара *{from_name} -> {to_name}* успешно создана\n\nПерейдите к редактированию и настройте пару.',
    'create_pair_input_from_name': '💸 *Создание валютной пары*\n\nВведите тикер отдаваемого актива *RUB ->* EUR',
    'create_pair_input_to_name': '❗️ Введите тикер получаемого актива RUB *-> EUR*',
    'create_pair_input_from_amount': '❗️ Введите минимальную-максимальную сумму которую пользователь может отдать в активе *{0}*\n\n__Формат: 100-10000__',
    'create_pair_input_from_country_code': '❗️ Введите код страны для отображения списка банков для актива *{0}*',
    'create_pair_input_spread': '❗️ Введите спред для пары числом.\n\n __Например: 3__',
    'create_pair_view_info': '*Создание пары*\n\n*Отдаваемый актив:* {from_name}\n*Мин/Макс сумма:* {from_min_amount}-{from_max_amount} {from_name}\n*Страна банков для {from_name}:* {from_country_code}\n\n*Получаемый актив:* {to_name}\n*Страна банков для {to_name}:* {to_country_code}\n\n*Спред:* {spread}%\n\n❗️ __from_handler_name, to_handler_name и другие данные вы можете указать после создания пары в разделе редактирования. Учтите, что после создания пара не отображается в списке обменов и её нужно активировать.__',

    'admin_technical_break_on': '❗️ *Бот перешёл в режим технического перерыва*\n\nПользователи не смогут создавать сделки в этом режиме.\n\nПриятного отдыха!',
    'admin_technical_break_off': '✅ *Бот перешёл в рабочий режим*\n\nПриятной работы!',
    'technical_break': '❗️ Обмены производятся в период с 8:00 до 23:00 по Московскому времени.',

    'admin_create_country_name': '🌐 Введите название страны',
    'admin_create_country_code': '🌐 Введите код страны *(ru, de..)*, это нужно для идентификации банков при создании валютной пары',
    'admin_create_country_info': '🌐 Вы готовы создать страну *{0}* с языковым кодом *{1}*?',
    'admin_create_country_success': '🌐 Страна создана',

    'admin_create_bank_name': '🏦 Введите название банка',
    'admin_create_bank_code': '🏦 Введите код страны *(ru, de..)*, это нужно для привязки банка к стране (категории)',
    'admin_create_bank_info': '🏦 Вы готовы создать банк *{0}* с кодом страны *{1}*?',
    'admin_create_bank_success': '🏦 Банк создан',


    'admin_user_is_admin': '✅ Пользователь `{0}` (@{1}) повышен до администратора.',
    'admin_user_is_not_admin': '✅ Пользователь `{0}` (@{1}) разжалован до пользователя.',
    'admin_cant_ban_yourself': '😔 Вы не можете разжаловать самого себя.',

    'admin_limits_info': '*📛 Лимиты*\n\n*Ограничение сделок:*\nМаксимум *{limit_deals_per} {limit_deals_per_plural}* одновременно, после следует ограничение на *{time_limit_deals} {time_limit_deals_plural}*\n\n*Ограничение на открытие спора:*\nПользователь может открыть спор только в первые *{dispute_deal_limit} {dispute_deal_limit_plural}* после успешного завершения сделки.\n\n⚠️ Выберите пункт ниже для редактирования',

    'admin_edit_limits_deals': '⚠️ Введите новый лимит по сделкам\n\n__Пример: 2-60 (2 сделки и 60 минут ограничения)',
    'admin_edit_limits_dispute_deals': '⚠️ Введите новый лимит по открытию спора\n\n__Пример: 15 (15 минут)',

    'input_conext_not_found': '🙅‍♂️ *Ввод вне контекста*\n\nВведите команду /start для перехода в главное меню',

    'input_spam_detection': '🙅‍♂️ *Спам-фильтр заблокировал ваши запросы*',


    # Message template
    'msg_deal': '📋 Сделка №{id}',
    'msg_deal_attachment': '💬 *Вложение от пользователя по сделке* `№{id}`\n\n*Сообщение:*\n{text}',
    'msg_chat_deal_manager': '💬 *Новое сообщение от менеджера по сделке* `№{id}`\n\n*Сообщение:*\n{text}',
    'msg_chat_deal_user': '💬 *Новое сообщение от пользователя по сделке* `№{id}`\n\n*Сообщение:*\n{text}',
    'msg_chat_deal_disput_manager': '💬 *Cообщение от менеджера по спорной сделке* `№{id}`\n\n*Сообщение:*\n{text}',
    'msg_chat_ticket_manager': '💬 *Cообщение от менеджера по тикету* `№{id}`\n\n*Сообщение:*\n{text}',

    # Inline кнопки
    'inline_create_new_exchange': '💸 Создать новую заявку',
    'inline_new_exchange': '💸 Новый обмен',
    'inline_my_exchanges': '📋 Мои сделки',
    'inline_faq': '❔ FAQ',
    'inline_support': '📩 Поддержка',
    'inline_affilate_program': '💎 Партнёрская программа',
    'inline_back_to': '◀️ Назад',
    'inline_admin_panel': '🔐 Админ панель',
    'inline_deal_input_profit': '💰 Указать прибыль',
    'inline_back_to_main_menu': '◀️ Назад в главное меню',
    'inline_admin_exchange_pair_name': '{2} {0} в {1}',
    'inline_exchange_pair_name': '{0} в {1}',
    'inline_send_message_to_support': '✅ Отправить',
    'inline_reply_message': '✍ Ответить',
    'inline_decline_message_to_support': '❌ Отменить отправку',
    'inline_exchange_accept_agreement': '✅ Принимаю',
    'inline_exchange_decline_agreement': '❌ Отказываюсь',
    'inline_exchange_accept': '✅ Да',
    'inline_exchange_decline': '❌ Нет',
    'inline_admin_params_exchange': '⚙️ Настройки системы',
    'inline_admin_orders': '📖 Открытые сделки ({0})',
    'inline_admin_problems_with_orders': '🚫 Проблемы со сделками ({0})',
    'inline_admin_support_requests': '📩 Обращения в поддержку ({0})',
    'inline_admin_logs': '📗 Поиск информации',
    'inline_enabled_deals_notifications': 'Уведомлять о новых сделках',
    'inline_enabled_support_notifications': 'Уведомлять о тикетах в поддержку',
    'inline_admin_pages': '📑 Страницы',
    'inline_params_rooms': '🏘 Комнаты',
    'inline_params_export': '📊 Выгрузка данных',
    'inline_params_affilate_program': '💎 Партнёрская программа',
    'inline_admin_edit_page': '✏️ Изменить текст',
    'inline_admin_attachment_document_page': '📎 Прикрепить документ',
    'inline_admin_delete_document_page': '❌ Удалить документ',
    'inline_admin_notification_get_deal': '➡️ Перейти к сделке',
    'inline_admin_notification_get_ticket': '➡️ Перейти к тикету',
    'inline_admin_search_id': '🆔 Поиск по ID',
    'inline_admin_search_username_or_uid': '🆔 Поиск по логину или ID пользователя',
    'inline_send': '💳 Отправить',
    'inline_create_support_ticket': '📩 Создать тикет',
    'inline_deal_change_status_decline': '❌ Отменить сделку',
    'inline_deal_view_deal': '🧾 Чек',
    'inline_deal_open_dispute': '❌ Открыть спор',
    'inline_deal_send_message': '✅ Отправить',
    'inline_deal_user_deal_paid_': '✅ Я оплатил',
    'inline_accept_delete': '❌ Удалить',
    'inline_deal_open_chat': '💬 Открыть чат',
    'inline_ticket_open_chat': '💬 Открыть чат',
    'inline_deal_change_status_accept': '✅ Начать сделку',
    'inline_deal_change_status_completed': '✅ Завершить сделку',
    'inline_deal_change_status_close': '✅ Закрыть сделку',
    'inline_deal_change_status_disput': '❌ Открыть спор',
    'inline_deal_change_status_process': '💳 Выдать реквизиты для оплаты',
    'inline_admin_countries': '🗺 Страны',
    'inline_admin_banks': '🏦 Банки',
    'inline_admin_pairs': '💱 Валютные пары',
    'inline_admin_edit_country_name': 'Изменить название',
    'inline_admin_edit_country_code': 'Изменить код страны',
    'inline_admin_pair_edit_from_name': 'Название первого актива',
    'inline_admin_pair_edit_from_country_code': 'Страна банков для первого актива',
    'inline_admin_pair_edit_min_from_amount': 'Мин. сумма первого актива',
    'inline_admin_pair_edit_max_from_amount': 'Макс. сумма первого актива',
    'inline_admin_pair_edit_to_name': '- Название второго актива',
    'inline_admin_pair_edit_to_country_code': 'Страна банков для второго актива',
    'inline_admin_pair_edit_spread': '% Спред',
    'inline_admin_pair_edit_from_handler_name': 'from_handler_name',
    'inline_admin_pair_edit_to_handler_name': 'to_handler_name',
    'inline_admin_pair_edit_handler_inverted': 'handler_inverted',
    'inline_admin_pair_edit_price_handler': 'Ценовой канал',
    'inline_admin_pair_edit_auto_requisites': 'Авто реквизиты',
    'inline_admin_pair_edit_to_type': 'Тип актива (получаю)',
    'inline_admin_pair_edit_from_type': 'Тип актива (отдаю)',
    'inline_admin_pair_edit_to_requisites_comment': '💬 Комментарий для реквизитов (отдаю)',
    'inline_ticket_change_status_answered': '✅ Пометить как решенный',
    'inline_create': '✅ Создать',
    'inline_cancel': '❌ Отменить',
    'inline_pair_create': '✅ Создать пару',
    'inline_create_pair': '💰 Создать валютную пару',
    'inline_to_pair': '💰 Перейти к паре',
    'inline_admin_pair_auto_requisites_active': '🟢 Авто реквизиты: вкл',
    'inline_admin_pair_auto_requisites_inactive': '🔴 Авто реквизиты: выкл',
    'inline_admin_pair_active': '🟢 Пара активна',
    'inline_admin_pair_inactive': '🔴 Пара неактивна',
    'inline_bot_active': '🟢 Отключить перерыв',
    'inline_bot_inactive': '🔴 Включить перерыв',
    'inline_create_country': '🌐 Создать страну',
    'inline_to_country': '🌐 Перейти к стране',
    'inline_admin_edit_bank_name': 'Изменить название',
    'inline_admin_edit_bank_country': 'Изменить страну (категорию)',
    'inline_admin_edit_bank_slug': 'Изменить ссылку (для фильтра)',
    'inline_admin_add_bank_accoount': '💳 Добавить счета',
    'inline_create_bank': '🏦 Создать банк',
    'inline_to_bank': '🏦 Перейти к банку',
    'inlint_delete_pair': '❌ Удалить пару',
    'inline_input_asset_name': 'Ввести в {0}',
    'inline_params_limits': '📛 Лимиты',
    'inline_params_limits_edit_deals': 'Лимит сделки',
    'inline_params_limits_edit_dispute_deals': 'Лимит спора',
    'inline_admin_stats_bank_accoount': '🎡 Оборот по счетам',

    # Reply кнопки
    'reply_exchange_cancel': '❌ Отменить',


    # Dict
    'dict_ticket_status': {
        'open': '🆕 открыт',
        'answered': '🟢 решён'
    },
    'dict_pair_status': {
        'active': '🟢',
        'inactive': '🔴'
    },
    'dict_deal_status': {
        'new': '🆕',
        'accepted': '⏳',
        'process': '⚪',
        'paid': '💸',
        'dispute': '⭕',
        'completed': '🟢',
        'declined': '🔴'
    },
    'dict_deal_status_text': {
        'new': 'Ожидает подтверждения',
        'accepted': 'Подтверждено',
        'process': 'В процессе',
        'paid': 'Оплачено',
        'dispute': 'Открыт спор',
        'completed': 'Завершено',
        'declined': 'Отклонено'
    },
    'dict_notifications_status': {
        'connected': '✅ ', # с пробелом
        'unconeccted': '➕ ' # с пробелом
    },

    # List's
    'list_support_request_reasons': [
        'Проблемы со сделкой',
        'Сотрудничество',
        'Идея',
        '❌ Отменить', # используется с фильтром IsCancelAction
    ]
}

locales['en'] = {

}

def translate(code: str, key: str) -> str:
    """ Возвращает языковую строку

        :code: str код языка
        :key: str языковая строка
    """
    return locales.get(code, config['DEFAULT']['language']).get(key, 'StringNotFound')
