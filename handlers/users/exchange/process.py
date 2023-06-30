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
from bot_locale.translate import _
from loader import bot, db, config, cache
from datetime import datetime, timedelta
import json

callback_data_select_pair = 'bot.set.exchage_select_pair_'
callback_data_select_from_bank = 'bot.set.exchage_select_from_bank_'
callback_data_select_to_bank = 'bot.set.exchage_select_to_bank_'
callback_data_input_amount = 'bot.set.exchage_input_amount_'
callback_data_exchange_accept = 'bot.set.exchage_accept'
cache_waiting_create_new_deal = '{0}_deal_locked_time'
callback_data_accept_agreement = 'bot.accept_agreement'

#======================================================#
#==============СОЗДАНИЕ СДЕЛКИ ПОЛЬЗОВАТЕЛЕМ===========#
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
        text=_(user['language_code'], 'bot_agreement_is_accepted'),
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
        text=_(user['language_code'], 'exchange_select_pair'),
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
            _(user['language_code'], 'technical_break'),
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
                    _(user['language_code'], 'page_not_found')
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
        text=_(user['language_code'], 'exchange_select_pair'),
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
        exchange_text = _(
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
        exchange_text = _(
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
        exchange_text = _(
            user['language_code'],
            key_string
        ).format(
            bank['name'],
            pair['to_name']
        )

        if pair['to_requisites_comment'] != '-': # пока дефис
            exchange_text += _(
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
            text=_(lang, 'error_data_not_valid')
        )
        return

    with bot.retrieve_data(user_id) as data:
        data['requisites'] = json.dumps(message.text)
        data['input_amount'] = 'from'
        pair = json.loads(data['pair'])

        exchange_text = _(
            lang,
            'exchange_input_from_amount'
        ).format(
            pair['from_name'],
            pair['to_name'],
            pair['min_from_amount'],
            pair['max_from_amount']
        )
        string_input_asset_name = _(lang, 'inline_input_asset_name').format(pair['to_name'])

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
    state=ExchageState.A6,
    is_chat=False,
    func=lambda call: call.data.startswith(callback_data_input_amount),
)
def state_a5(call):
    """ Переключает ввод суммы from/to
        в активах
    """
    user_id = call.from_user.id
    user = db.get_user(user_id)
    lang = user['language_code']

    with bot.retrieve_data(user_id) as data:
        try:
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

            string_input_asset_name = _(
                lang,
                string_input_asset_name
            ).format(
                to_name
            )

            exchange_text = _(
                lang,
                string_input_text
            ).format(
                from_name,
                to_name,
                pair['min_from_amount'],
                pair['max_from_amount']
            )


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


@bot.message_handler(state=ExchageState.A6, is_chat=False, is_cancel_action=False, is_amount=False)
def error_state_a6(message):
    """ Если во время ввода суммы обмена
        пользователь ввёл некорректную сумму,
        выдаём ему ошибку
    """
    user = db.get_user(message.from_user.id)
    bot.send_message(
        message.chat.id,
        text=_(user['language_code'], 'error_data_not_valid')
    )

@bot.message_handler(state=ExchageState.A6, is_chat=False, is_amount=True, is_cancel_action=False)
def state_a6(message):
    """ Показывает котировки
    """
    user_id = message.from_user.id
    user = db.get_user(user_id)

    amount = float(message.text) # фильтр пройден, можно не бояться за поступаемые данные, exception не бросит (но требует замены)

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
                text=_(user['language_code'], 'error_data_not_valid')
            )
            return

        exchange_info = calculate_amount(amount, pair, data['input_amount'])

        data['to_amount'] = exchange_info['to_amount']
        data['from_amount'] = exchange_info['from_amount']

        data['exchange_rate'] = exchange_info['exchange_rate']
        data['orig_finally_exchange_rate'] = exchange_info['orig_finally_exchange_rate']

        data['orig_calculated_amount'] = exchange_info['orig_calculated_amount']
        data['spread'] = pair['spread']

        data['to_bank_requisites'] = requisites

        # Выводим котировки
        exchange_message = _(
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

        if user['role'] in ['admin', 'manager']:
            #
            # Добавляем данные для админов
            #
            exchange_message += _(
                user['language_code'],
                'exchange_issuing_quotes_debug'
            ).format(**{
                #debug
                'from_name': pair['from_name'],
                'to_name': pair['to_name'],
                'orig1': exchange_info['orig_calculated_amount'],
                'orig2': exchange_info['orig_finally_exchange_rate'],
                'origsp': pair['spread'],
            })

        introduction_deal = bot.send_message(
            chat_id=message.chat.id,
            text=_(user['language_code'], 'exchange_deal_introduction'),
            reply_markup=MenuKeyboard.remove_reply()
        )

        bot.send_message(
            message.chat.id,
            text=str(exchange_message),
            reply_markup=MenuKeyboard.exchange_accept_or_decline(user)
        )

        data['introduction_deal_mid'] = introduction_deal.message_id

    bot.set_state(message.from_user.id, ExchageState.A7)


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
            _(lang, 'user_is_banned'),
            show_alert=True
        )
        return

    if lock and user['role'] not in ['manager', 'admin']:
        bot.answer_callback_query(
            call.id,
            _(lang, 'exceed_limit_deal'),
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

        try:
            # ВЫНЕСТИ ВЕРИФИКАЦИЮ В ОТДЕЛЬНЫЙ обрабтчик после доработки
            if pair['verification_account'] and user['role'] in ['user']:
                key_string_card_verification = _(lang, 'inline_card_verification')
                key_string_full_verification = _(lang,'inline_full_verification')
                verify = json.loads(user['verification_data'])

                kb = {
                    key_string_card_verification: {'callback_data': 'te'},
                    key_string_full_verification: {'callback_data': 'te'}
                }

                if user['verification'] in ['process']:
                    bot.answer_callback_query(
                        call.id,
                        _(lang, 'inline_process_verification'),
                        show_alert=True
                    )
                    return

                if (
                    user['verification'] in ['anonymous'] or
                    user['verification'] in ['card_verified'] and
                    data['to_bank_requisites'] != verify.get('card_verified')
                ):
                    if user['verification'] == 'card_verified':
                        del kb[key_string_card_verification]

                    page_verification = db.get_page(4, name_id='id')

                    from utils.misc.view_page import page_send_message

                    bot.delete_message(chat_id=call.message.chat.id,
                    message_id=call.message.message_id)

                    page_send_message(call.message.chat.id, user, page_verification)

                    bot.send_message(
                        chat_id=call.message.chat.id,
                        text=_(lang, 'verification_text'),
                        reply_markup=MenuKeyboard.smart(kb)
                    )
                    return
        except Exception as e:
            print(e)

        if pair.get('auto_requisites'):
            requisites = get_payment_account(pair, from_bank['id'])

        if type(requisites) == dict and requisites != {}:
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
                "expires":                  config['time_cancel_deal'],
                "status":                   deal_status,
            }

            # Создаю сделку в базе
            order_id = db.create_deal(deal)

            string_new_exchange = _(lang, 'inline_create_new_exchange')
            string_back_menu = _(lang, 'inline_back_to_main_menu')

            kb = MenuKeyboard.smart({
                string_new_exchange: {
                    'callback_data':  'bot.set.new_exchange'
                },
                string_back_menu: {
                    'callback_data':  'bot.back_to_main_menu'
                }
            })

            exchange_text = _(
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

        # if pair.get('auto_requisites') and requisites != {}:
        #     # КОСТЫЛЬ: отменяем дальнейшие действия
        #     return False

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
