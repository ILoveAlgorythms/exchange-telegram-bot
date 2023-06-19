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
callback_data_exchange_accept = 'bot.set.exchage_accept'
callback_data_accept_agreement = 'bot.accept_agreement'
callback_data_accept_deal_accept = 'bot.deal_change_status_accept_'
callback_data_accept_deal_paid = 'bot.deal_change_status_paid_'
callback_data_open_user_chat = 'bot.deal_open_user_chat_'
callback_data_deal_send_message = 'bot.deal_send_message_chat'
callback_data_admin_work_open_deal = 'admin.open_work_deal_'
cache_waiting_create_new_deal = '{0}_deal_locked_time'

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

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith('bot.set.new_exchange'))
def state_a1(call):
    """ Выбор пары для обмена
    """
    user = db.get_user(call.from_user.id)
    config = db.get_config()

    if config['technical_break'] == 1:
        bot.answer_callback_query(
            call.id,
            translate(user['language_code'], 'technical_break'),
            show_alert=True
        )
        return

    if user['is_agreement'] == False:
        # Просим пользователя принять соглашение
        # перед дальнейшим использованием обменника
        agreement_page = db.get_page("agreement")

        if agreement_page.get("document") != "null":
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id
            )

            document = json.loads(agreement_page['document'])
            file = document['file_id']

            try:
                bot.get_file(file)
            except Exception as e:
                file = open(ROOT_DIR + document['path'], 'rb')

            bot.send_document(
                chat_id=call.message.chat.id,
                document=file,
                caption=agreement_page.get(
                    'page_content',
                    translate(user['language_code'], 'page_not_found')
                ),
                reply_markup=MenuKeyboard.agreement_accept_or_decline(user)
            )

            return

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=agreement_page['page_content'],
            reply_markup=MenuKeyboard.agreement_accept_or_decline(user)
        )

        return

    pairs = db.get_pairs()

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=translate(user['language_code'], 'exchange_select_pair'),
        reply_markup=MenuKeyboard.pairs(user, pairs, callback_data_select_pair)
    )
    # Даём возможность выбрать банк
    bot.set_state(call.from_user.id, ExchageState.A2)

@bot.callback_query_handler(
    is_chat=False,
    func=lambda call: call.data.startswith(callback_data_select_pair),
    state=ExchageState.A2
)
def state_a2(call):
    """ Выбор банка из которого будут
        отправлены средства
    """
    pair_id = call.data.replace(callback_data_select_pair, "")
    user = db.get_user(call.from_user.id)
    user_id = call.from_user.id
    pair = db.get_pair(pair_id)
    banks = db.get_banks({'country_code': pair['from_country_code']})

    with bot.retrieve_data(user_id) as data:
        data['user'] = json.dumps(
            user,
            indent=4,
            sort_keys=True,
            default=str
        )
        data['pair'] = json.dumps(
            pair,
            indent=4,
            sort_keys=True,
            default=str
        )

        key_string = 'exchange_select_from_network' if pair['from_type'] == 'crypto' else 'exchange_select_from_bank'
        exchange_text = translate(
            user['language_code'],
            key_string
        ).format(
            pair['from_name']
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=exchange_text,
            reply_markup=MenuKeyboard.banks(user, banks, callback_data_select_from_bank)
        )
        data['a2_mid'] = call.message.message_id
    # Даём возможность ввести номер карты
    bot.set_state(call.from_user.id, ExchageState.A3)


@bot.callback_query_handler(
    is_chat=False,
    func=lambda call: call.data.startswith(callback_data_select_from_bank),
    state=ExchageState.A3
)
def state_a2(call):
    """ Выбор банка в который будут зачислены средства
    """
    bank_id = call.data.replace(callback_data_select_from_bank, "")
    from_bank = db.get_bank(bank_id)

    with bot.retrieve_data(call.from_user.id) as data:
        data['from_bank'] = json.dumps(from_bank, indent=4, sort_keys=True, default=str)
        pair = json.loads(data['pair'])
        user = json.loads(data['user'])
        banks = db.get_banks({'country_code': pair['to_country_code']})

        key_string = 'exchange_select_to_network' if pair['to_type'] == 'crypto' else 'exchange_select_to_bank'
        exchange_text = translate(
            user['language_code'],
            key_string
        ).format(
            pair['to_name']
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=exchange_text,
            reply_markup=MenuKeyboard.banks(user, banks, callback_data_select_to_bank)
        )
        data['a3_mid'] = call.message.message_id
    # Даём возможность ввести номер карты
    bot.set_state(call.from_user.id, ExchageState.A4)

@bot.callback_query_handler(
    is_chat=False,
    func=lambda call: call.data.startswith(callback_data_select_to_bank),
    state=ExchageState.A4
)
def state_a4(call):
    """ Ввод номера счёта
    """
    bank_id = call.data.replace(callback_data_select_to_bank, "")
    user_id = call.from_user.id
    user = db.get_user(user_id)
    bank = db.get_bank(bank_id)

    with bot.retrieve_data(user_id) as data:
        data['to_bank'] = json.dumps(bank, indent=4, sort_keys=True, default=str)
        pair = json.loads(data['pair'])
        key_string = 'exchange_input_to_wallet_address' if pair['to_type'] == 'crypto' else 'exchange_input_to_card_cumber'


        # Выводим котировки
        exchange_text = translate(
            user['language_code'],
            key_string
        ).format(
            bank['name'],
            pair['to_name']
        )

        if pair['to_requisites_comment'] != '-': # пока дефис
            exchange_text += translate(
                user['language_code'],
                'exchange_comment_input_to_requisites'
            ).format(
                pair['to_requisites_comment']
            )

        bot.delete_message(
            chat_id=call.message.chat.id,
            message_id=data['a3_mid']
        )

        bot.send_message(
            chat_id=call.message.chat.id,
            text=exchange_text,
            reply_markup=MenuKeyboard.reply_exchange_cancel(user)
        )
    # Даём возможность ввести сумму обмена
    bot.set_state(call.from_user.id, ExchageState.A5)

@bot.message_handler(is_chat=False, state=ExchageState.A5, is_cancel_action=False)
def state_a5(message):
    """ Ввод суммы обмена
    """
    user_id = message.from_user.id
    user = db.get_user(user_id)
    message_length = len(message.text)
    lang = user['language_code']

    if message_length > 256 or message_length < 6:
        # Если указана сумма меньше или больше
        # допустимой суммы, выводим ошибку.
        bot.send_message(
            message.chat.id,
            text=translate(lang, 'error_data_not_valid')
        )
        return

    with bot.retrieve_data(user_id) as data:
        data['requisites'] = json.dumps(message.text)
        data['input_amount'] = 'from'
        pair = json.loads(data['pair'])

        exchange_text = translate(
            lang,
            'exchange_input_from_amount'
        ).format(
            pair['from_name'],
            pair['to_name'],
            pair['min_from_amount'],
            pair['max_from_amount']
        )
        string_input_asset_name = translate(lang, 'inline_input_asset_name').format(pair['to_name'])

        try:
            bot.send_message(
                chat_id=message.chat.id,
                text=exchange_text,
                reply_markup=MenuKeyboard.smart({
                    string_input_asset_name: {
                        'callback_data': (callback_data_input_amount + str(data['input_amount']))
                    }
                })
            )
        except Exception as e:
            print(e)


    # Даём возможность получить котировки обмена,
    # после вводы суммы обмена
    bot.set_state(message.from_user.id, ExchageState.A6)


@bot.callback_query_handler(
    is_chat=False,
    func=lambda call: call.data.startswith(callback_data_input_amount),
    state=ExchageState.A6
)
def state_a5(call):
    """ Переключает ввод суммы from/to
        активах
    """
    user_id = call.from_user.id
    user = db.get_user(user_id)
    lang = user['language_code']

    with bot.retrieve_data(user_id) as data:
        calldata = call.data.replace(callback_data_input_amount, "")
        pair = json.loads(data['pair'])

        direction_dict = {'from': 'to', 'to': 'from'}
        direction = direction_dict.get(calldata)
        data['input_amount'] = direction

        string_input_text = 'exchange_input_from_amount'
        string_input_asset_name = 'inline_input_asset_name'

        from_name = pair['from_name']
        to_name = pair['to_name']

        if direction == 'to':
            string_input_text = 'exchange_input_to_amount'

            pair1 = calculate_amount(pair['min_from_amount'], pair)
            pair2 = calculate_amount(pair['max_from_amount'], pair)

            data['pair1'] = json.dumps(pair1, indent=4, sort_keys=True, default=str)
            data['pair2'] = json.dumps(pair2, indent=4, sort_keys=True, default=str)

            pair['min_from_amount'] = pair1['to_amount']
            pair['max_from_amount'] = pair2['to_amount']

            data['min_from_amount'] = pair1['to_amount']
            data['max_from_amount'] = pair2['to_amount']

            from_name = pair['to_name']
            to_name = pair['from_name']

        string_input_asset_name = translate(
            lang,
            string_input_asset_name
        ).format(
            to_name
        )

        exchange_text = translate(
            lang,
            string_input_text
        ).format(
            from_name,
            to_name,
            pair['min_from_amount'],
            pair['max_from_amount']
        )

        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=exchange_text,
                reply_markup=MenuKeyboard.smart({
                    string_input_asset_name: {
                        'callback_data': (callback_data_input_amount + str(direction))
                    }
                })
            )
        except Exception as e:
            print(e)


@bot.message_handler(is_chat=False, is_amount=False, state=ExchageState.A6, is_cancel_action=False)
def error_state_a6(message):
    """ Если во время ввода суммы обмена
        пользователь ввёл некорректные данные,
        выдаём ему ошибку
    """
    user = db.get_user(message.from_user.id)
    bot.send_message(
        message.chat.id,
        text=translate(user['language_code'], 'error_data_not_valid')
    )

@bot.message_handler(is_chat=False, is_amount=True, state=ExchageState.A6, is_cancel_action=False)
def state_a6(message):
    """ Показывает котировки
    """
    user_id = message.from_user.id
    user = db.get_user(user_id)
    amount = float(message.text)

    with bot.retrieve_data(user_id) as data:
        pair = json.loads(data['pair'])
        from_bank = json.loads(data['from_bank'])
        to_bank = json.loads(data['to_bank'])
        requisites = json.loads(data['requisites'])
        min_amount = pair['min_from_amount']
        max_amount = pair['max_from_amount']

        if data['input_amount'] == 'to':
            min_amount = float(data['min_from_amount'])
            max_amount = float(data['max_from_amount'])

        if amount > max_amount or amount < min_amount:
            # Если указана сумма меньше или больше
            # допустимой суммы, выводим ошибку.
            bot.send_message(
                message.chat.id,
                text=translate(user['language_code'], 'error_data_not_valid')
            )
            return

        exchange_info = calculate_amount(amount, pair, data['input_amount'])

        data['to_amount'] = exchange_info['to_amount']
        data['from_amount'] = exchange_info['from_amount']
        data['exchange_rate'] = exchange_info['exchange_rate']
        data['orig_calculated_amount'] = exchange_info['orig_calculated_amount']
        data['orig_finally_exchange_rate'] = exchange_info['orig_finally_exchange_rate']
        data['spread'] = pair['spread']
        data['to_bank_requisites'] = requisites

        # Выводим котировки
        exchange_message = translate(
            user['language_code'],
            'exchange_issuing_quotes'
        ).format(**{
            'to_amount':          exchange_info['to_amount'],
            'to_name':            pair['to_name'],
            'from_bank_name':     from_bank['name'],
            'from_amount':        exchange_info['from_amount'],
            'from_name':          pair['from_name'],
            'exchange_rate':      exchange_info['exchange_rate'],
            'to_bank_name':       to_bank['name'],
            'to_bank_requisites': requisites,
            'rate_from_name':     exchange_info['rate_from_name'],
            'rate_from_amount':   exchange_info['rate_from_amount'],
            'rate_to_name':       exchange_info['rate_to_name'],
            'rate_to_amount':     exchange_info['rate_to_amount'],
        })

        introduction_deal = bot.send_message(
            chat_id=message.chat.id,
            text=translate(user['language_code'], 'exchange_deal_introduction'),
            reply_markup=MenuKeyboard.remove_reply()
        )

        bot.send_message(
            message.chat.id,
            text=str(exchange_message),
            reply_markup=MenuKeyboard.exchange_accept_or_decline(user)
        )

        data['introduction_deal_mid'] = introduction_deal.message_id

    bot.set_state(message.from_user.id, ExchageState.A7)

def get_restriction(key_string, user_id, expires_at, set=False):
    key_string = key_string.format(user_id)
    data = cache.get(key_string)

    if data is None:
        return False
    return True

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_exchange_accept), state=ExchageState.A7)
def exchange_accept(call):
    """ Создание обмена в базе данных
    """
    user_id = call.from_user.id
    user = db.get_user(user_id)
    lang = user['language_code']
    config = db.get_config()
    lock = Restriction.action(
        cache_waiting_create_new_deal,
        user['id'],
        config['limit_deals_per'],
        config['time_limit_deals']
    )

    if user['is_banned'] == 1:
        bot.answer_callback_query(
            call.id,
            translate(lang, 'user_is_banned'),
            show_alert=True
        )
        return

    if lock and user['role'] not in ['manager', 'admin']:
        bot.answer_callback_query(
            call.id,
            translate(lang, 'exceed_limit_deal'),
            show_alert=True
        )
        return

    with bot.retrieve_data(user_id) as data:
        pair = json.loads(data['pair'])
        to_bank = json.loads(data['to_bank'])
        from_bank = json.loads(data['from_bank'])
        deal_status = 'new'
        payment_account_id = 0
        requisites = None

        if pair.get('auto_requisites'):
            requisites = get_payment_account(pair, from_bank['id'])

        if requisites != {}:
            payment_account_id = requisites['account_id']
            deal_status = 'process'

        try:
            deal = {
                "manager_id":               0,
                "user_id":                  user['id'],
                "from_name":                pair['from_name'],
                "from_amount":              data['from_amount'],
                "from_bank_name":           from_bank['name'],
                "from_bank_id":             from_bank['id'],
                "from_payment_account_id":  payment_account_id,
                "to_name":                  pair['to_name'],
                "to_amount":                data['to_amount'],
                "to_bank_name":             to_bank['name'],
                "requisites":               data['to_bank_requisites'],
                "exchange_rate":            data['exchange_rate'],
                "orig_exchange_rate":       data['orig_finally_exchange_rate'],
                "orig_to_amount":           data['orig_calculated_amount'],
                "spread":                   data['spread'],
                "calculated_amount":        1,
                "status":                   deal_status,
            }

            # Создаю сделку в базе
            order_id = db.create_deal(deal)

            # cache.set(is_lock_string, user_id)
            # cache.expire(is_lock_string, (config['time_limit_deals'] * 60)) # 15 min

            kb = None
            exchange_text = translate(
                user['language_code'],
                'exchange_deal_created'
            ).format(**{
                "id":             order_id,
                "to_amount":      data['to_amount'],
                "to_name":        pair['to_name'],
                "to_bank_name":   to_bank['name'],
                "from_amount":    data['from_amount'],
                "from_name":      pair['from_name'],
                "from_bank_name": from_bank['name'],
                "requisites":     data['to_bank_requisites'],
            })

            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=data['introduction_deal_mid'],
            )

            if pair.get('auto_requisites') and requisites != {}:
                deal = db.get_deal(order_id)
                exchange_text, kb = get_requisites_text(user, deal, payment_account_id)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=exchange_text,
                reply_markup=kb
            )
        except Exception as e:
            print(e)

        if pair.get('auto_requisites') and requisites != {}:
            # КОСТЫЛЬ: отменяем дальнейшие действия
            return False

        try:
            # Отправляем уведомление о сделке
            #
            deal = db.get_deal(order_id)
            bot.send_message(
                config['notifications_deal_chat_id'],
                get_admin_deal_text(user, deal),
                reply_markup=MenuKeyboard.notification_deal(user, order_id)
            )
        except Exception as e:
            print(e)

    # bot.delete_state(call.from_user.id)


#======================================================#
#=================ПОДТВЕРЖДЕНИЕ ОПЛЛАТЫ================#
#======================================================#


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_accept_deal_accept))
def accept_paid_deal(call):
    """ Пользователь подтверждает,
        что отправил деньги по
        указанными реквизитам
    """
    deal_id = call.data.replace(callback_data_accept_deal_accept, "")
    user = db.get_user(call.from_user.id)
    deal = db.get_deal(deal_id)

    if (
        deal['user_id'] != user['id'] or
        deal['status'] != 'process'
    ):
        bot.answer_callback_query(
            call.id,
            translate(user['language_code'], 'deal_not_available'),
            show_alert=True
        )
        return

    bot.set_state(call.from_user.id, UserDeal.requisites)

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

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=call.message.text,
        reply_markup=''
    )
    bot.send_message(
        chat_id=call.message.chat.id,
        text=translate(user['language_code'], 'user_deal_accept_confirmation_or_message'),
        reply_markup=MenuKeyboard.accept_or_decline(
            user,
            cl_accept=callback_data_accept_deal_paid+str(deal['id']),
            key_string_accept='inline_deal_user_deal_paid_',
            cl_decline='bot.back_to_main_menu',
            key_string_decline='inline_back_to_main_menu',
        )
    )

@bot.message_handler(is_chat=False, state=UserDeal.requisites, content_types=['audio', 'animation', 'sticker', 'video_note', 'voice', 'contact', 'location', 'venue', 'dice', 'invoice', 'successful_payment'])
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
            translate(user['language_code'], 'deal_file_not_supported'),
            reply_markup=MenuKeyboard.accept_or_decline(
                user,
                cl_accept=callback_data_accept_deal_paid+str(deal['id']),
                key_string_accept='inline_deal_user_deal_paid_',
                cl_decline='bot.back_to_main_menu',
                key_string_decline='inline_back_to_main_menu',
            )
        )

@bot.message_handler(is_chat=False, state=UserDeal.requisites, content_types=['text', 'photo', 'video', 'document'])
def set_message(message):
    """ Получаем доп информацию от пользователя по сделке
        (перед подтверждением оплаты)

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
                    cl_accept=callback_data_accept_deal_paid+str(deal['id']),
                    key_string_accept='inline_deal_user_deal_paid_',
                    cl_decline='bot.back_to_main_menu',
                    key_string_decline='inline_back_to_main_menu',
                )
            )
            data['message_id'] = new_message.message_id
        except Exception as e:
            print(e)


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_accept_deal_paid), state=UserDeal.requisites)
def bot_to_main_menu(call):
    """ Подтверждаем, что сделка оплачена
    """
    config = db.get_config()

    if config['technical_break'] == 1:
        bot.answer_callback_query(
            call.id,
            translate(user['language_code'], 'technical_break'),
            show_alert=True
        )
        return

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
                    'user_deal_change_status_paid'
                ).format(
                    deal['id']
                )
            )

            # key_string_back_to = translate(user['language_code'], 'inline_back_to_main_menu')
            # bot.send_message(
            #     chat_id=call.message.chat.id,
            #     text=translate(
            #         user['language_code'],
            #         'user_deal_change_status_paid'
            #     ),
            #     reply_markup=MenuKeyboard.smart({
            #         key_string_back_to: {'callback_data': 'bot.back_to_main_menu'}
            #     })
            # )

            if data.get('content_type') is not None:
                db.create_message(
                    user_id=user['id'],
                    dialog_id=dialog['id'],
                    text=data['message'],
                    attach=data['attach'],
                    content_type=data['content_type'],
                )

            db.update_deal(deal['id'], {'status': 'paid'})
        except Exception as e:
            print(e)

        if config['notifications_deal_chat_id'] is not False:
            try:
                kb = MenuKeyboard.notification_deal(user, deal['id'])
                m = bot.send_message(
                    chat_id=config['notifications_deal_chat_id'],
                    text=translate(
                        user['language_code'],
                        'user_deal_change_status_paid_notification'
                    ).format(**{
                        "id": deal['id'],
                        "from_name": deal['from_name'],
                        "from_bank_name": deal['from_bank_name'],
                        "from_amount": deal['from_amount'],
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
