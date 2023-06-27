from loader import bot, db
from states.states import EditPair, CreatePair
from bot_locale.translate import _
from keyboards.inline.menu import AdminKeyboard, MenuKeyboard
from telebot.formatting import escape_markdown

import json

callback_data_admin_params = 'admin.params'
callback_data_admin_pairs = 'admin.params_pairs'
callback_data_admin_view_pair = 'admin.params_pair_view_'
callback_data_admin_edit_pair = 'admin.params_pair_edit_'
callback_data_admin_create_pair = 'admin.params_pair_create'
callback_data_admin_create_pair_accept = 'admin.params_pair_accept_create'

callback_data_admin_delete_pair = 'admin.params_pair_delete_'
callback_data_admin_pair_accept_delete = 'admin.params_pair_accept_delete_'

params = {
    'from_name':             'inline_admin_pair_edit_from_name',
    'from_country_code':     'inline_admin_pair_edit_from_country_code',
    'from_type':             'inline_admin_pair_edit_from_type',
    'min_from_amount':       'inline_admin_pair_edit_min_from_amount',
    'max_from_amount':       'inline_admin_pair_edit_max_from_amount',
    'to_name':               'inline_admin_pair_edit_to_name',
    'to_country_code':       'inline_admin_pair_edit_to_country_code',
    'to_type':               'inline_admin_pair_edit_from_type',
    'to_requisites_comment': 'inline_admin_pair_edit_to_requisites_comment',
    'spread':                'inline_admin_pair_edit_spread',
    'auto_requisites':       'inline_admin_pair_edit_price_handler',
    'handler_inverted':      'inline_admin_pair_edit_handler_inverted',
    'from_handler_name':     'inline_admin_pair_edit_from_handler_name',
    'to_handler_name':       'inline_admin_pair_edit_to_handler_name',
    'handler_inverted':      'inline_admin_pair_edit_handler_inverted',
}

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data == callback_data_admin_pairs, role=['admin'])
def admin_banks_list(call):
    """ Отображает список валютных пар
    """
    user = db.get_user(call.from_user.id)
    pairs = db.get_pairs(data=[0, 1])

    bot.delete_state(call.from_user.id)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=_(user['language_code'], 'admin_page_pairs'),
        reply_markup=AdminKeyboard.pairs(
            user,
            pairs,
            callback_data_admin_view_pair,
            back_menu_data=callback_data_admin_params,
            key_string_back_to='inline_back_to'
        )
    )


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_delete_pair), role=['admin'])
def admin_delete_pair(call):
    """ Предупреждение об удалении пары
    """
    user = db.get_user(call.from_user.id)
    pair_id = call.data.replace(callback_data_admin_delete_pair ,"")
    pair = db.get_pair(pair_id, name_id="id")

    edit_pair_text = _(
        user['language_code'],
        'admin_data_pair_delete'
    ).format(**pair)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=edit_pair_text,
        reply_markup=MenuKeyboard.accept_or_decline(
            user,
            cl_accept=callback_data_admin_pair_accept_delete+str(pair['id']),
            key_string_accept='inline_accept_delete',
            cl_decline=callback_data_admin_pairs,
            key_string_decline='inline_back_to',
        )
    )


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_pair_accept_delete), role=['admin'])
def admin_delete_pair_accept(call):
    """ Удаление пары
    """

    user = db.get_user(call.from_user.id)
    pair_id = call.data.replace(callback_data_admin_pair_accept_delete ,"")
    pair = db.get_pair(pair_id, name_id="id")

    db.delete_object(
        table="pairs",
        name_id="id",
        value=pair['id']
    )

    edit_pair_text = _(
        user['language_code'],
        'admin_data_pair_delete_success'
    ).format(**pair)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=edit_pair_text,
        reply_markup=MenuKeyboard.back_to(
            user,
            data=callback_data_admin_pairs,
            key_string='inline_back_to',
        )
    )


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_view_pair), role=['admin'])
def admin_preview_pair(call):
    """ Отображает содержимое и кнопки управления валютной парой
    """
    user = db.get_user(call.from_user.id)
    pair_id = call.data.replace(callback_data_admin_view_pair ,"")
    pair = db.get_pair(pair_id, name_id="id")
    pair['is_active'] = bool(pair['is_active'])

    edit_pair_text = _(
        user['language_code'],
        'admin_data_pair_view'
    ).format(**pair)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=edit_pair_text,
        reply_markup=AdminKeyboard.edit_pair(user, pair, params)
    )

    # Для кнопки "Назад" из редактирования страны
    bot.delete_state(call.from_user.id)

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_edit_pair), role=['admin'])
def admin_edit_pair(call):
    """ Редактирование пары
    """
    user = db.get_user(call.from_user.id)
    pair_param = call.data.replace(callback_data_admin_edit_pair, "").split("|")
    parameter = pair_param[0]
    pair_id = pair_param[1]
    pair = db.get_pair(pair_id, name_id="id")

    if parameter == 'status':
        bot.answer_callback_query(
            call.id,
            'Success!'
        )

        status = 1 if pair['is_active'] == 0 else 0
        pair['is_active'] = status

        db.update_pair(pair_id=pair['id'], args={'is_active': status})

        edit_pair_text = _(
            user['language_code'],
            'admin_data_pair_view'
        ).format(**pair)

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=edit_pair_text,
            reply_markup=AdminKeyboard.edit_pair(user, pair, params)
        )
        return

    if parameter == 'verification_account':
        bot.answer_callback_query(
            call.id,
            'Success!'
        )

        verification_account = 1 if pair['verification_account'] == 0 else 0
        pair['verification_account'] = verification_account

        db.update_pair(pair_id=pair['id'], args={'verification_account': verification_account})

        edit_pair_text = _(
            user['language_code'],
            'admin_data_pair_view'
        ).format(**pair)

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=edit_pair_text,
            reply_markup=AdminKeyboard.edit_pair(user, pair, params)
        )
        return

    if parameter == 'auto_requisites':
        bot.answer_callback_query(
            call.id,
            'Success!'
        )

        auto_requisites = 1 if pair['auto_requisites'] == 0 else 0
        pair['auto_requisites'] = auto_requisites

        db.update_pair(pair_id=pair['id'], args={'auto_requisites': auto_requisites})

        edit_pair_text = _(
            user['language_code'],
            'admin_data_pair_view'
        ).format(**pair)

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=edit_pair_text,
            reply_markup=AdminKeyboard.edit_pair(user, pair, params)
        )
        return


    bot.set_state(call.from_user.id, EditPair.A1)

    with bot.retrieve_data(call.from_user.id) as data:
        data['message_id'] = call.message.message_id
        data['pair_id'] = pair['id']
        data['parameter'] = parameter

    edit_country_text = _(
        user['language_code'],
        'edit_pair_parameter'
    ).format(
        _(user['language_code'], params[parameter])
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=edit_country_text,
        reply_markup=MenuKeyboard.back_to(user, key_string='inline_back_to', data=callback_data_admin_view_pair+str(pair['id']))
    )

    if parameter == 'price_handler':
        bot.send_message(
            chat_id=call.message.chat.id,
            text='`cryptoexchage` или `binance`'
        )

    if parameter in ['from_country_code', 'to_country_code']:
        countries = db.get_countries()
        country_text = "*Отправьте код страны в ответ:*\n"

        for country in countries:
            banks = db.get_banks(args={'country_code': country['slug']})
            banks_text = '' if len(banks) > 0 else 'Нет банков\n'
            for bank in banks:
                banks_text += f"— {bank['name']}\n"


            country_text += f"\n{country['name']} — `{country['slug']}`\n"
            country_text += banks_text

        bot.send_message(
            chat_id=call.message.chat.id,
            text=country_text
        )

@bot.message_handler(is_chat=False, state=EditPair.A1, role=['admin'])
def edit_pair_param(message):
    user = db.get_user(message.from_user.id)

    with bot.retrieve_data(message.from_user.id) as data:
        # Обрезаем
        param_value = message.text[0:4000]

        try:
            if data['parameter'] in ['spread', 'min_from_amount', 'max_from_amount']:
                param_value = float(param_value)
        except Exception as e:
            param_value = 0

        if (
            data['parameter'] == 'type' and
            param_value not in ['crypto', 'fiat']
        ):
            param_value = 'fiat'

        try:
            # Обновляем
            db.update_pair(pair_id=data['pair_id'], args={data['parameter']: param_value})

        except Exception as e:
            print(e)

        # Получаем актуальные данные и возвращаем в админку
        pair = db.get_pair(data['pair_id'], name_id="id")
        edit_pair_text = _(
            user['language_code'],
            'admin_data_pair_view'
        ).format(**pair)

        try:
            bot.delete_message(
                chat_id=message.chat.id,
                message_id=data['message_id']
            )
        except Exception as e:
            pass

        bot.send_message(
            chat_id=message.chat.id,
            text=_(user['language_code'], 'admin_data_success_edit')
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=edit_pair_text,
            reply_markup=AdminKeyboard.edit_pair(user, pair, params)
        )

        bot.delete_state(message.from_user.id)


###         ###         ###         ###         ###
###############         ###############         ###
###         ###############         ###############
###         ###         ###         ###         ###

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data == callback_data_admin_create_pair, role=['admin'])
def admin_create_pair(call):
    """ Создание пары
    """
    user_id = call.from_user.id
    user = db.get_user(user_id)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=_(user['language_code'], 'create_pair_input_from_name'),
        reply_markup=MenuKeyboard.back_to(user, key_string='inline_back_to', data=callback_data_admin_pairs)
    )

    bot.set_state(user_id, CreatePair.A1)

    with bot.retrieve_data(user_id) as data:
        data['user'] = json.dumps(
            user,
            indent=4,
            sort_keys=True,
            default=str
        )


@bot.message_handler(is_chat=False, state=CreatePair.A1, role=['admin'])
def create_pair_a1(message):
    """ Сохранение отдаваемого актива
        и ввод получаемого
    """
    user_id = message.from_user.id
    with bot.retrieve_data(message.from_user.id) as data:
        user = json.loads(data['user'])
        data['from_name'] = message.text
        bot.send_message(
            user_id,
            text=_(user['language_code'], 'create_pair_input_to_name')
        )

    bot.set_state(user_id, CreatePair.A2)

@bot.message_handler(is_chat=False, state=CreatePair.A2, role=['admin'])
def create_pair_a2(message):
    """ Сохранение получаемого актива
        и ввод  мин/макс суммы отдаваемого актива
    """
    user_id = message.from_user.id
    with bot.retrieve_data(message.from_user.id) as data:
        user = json.loads(data['user'])
        data['to_name'] = message.text
        bot.send_message(
            user_id,
            text=_(user['language_code'], 'create_pair_input_from_amount').format(data['from_name'] )
        )

    bot.set_state(user_id, CreatePair.A3)

@bot.message_handler(is_chat=False, state=CreatePair.A3, role=['admin'])
def create_pair_a3(message):
    """ Сохранение мин/макс суммы
        и ввод кода страны для отдаваемой пары
    """
    user_id = message.from_user.id
    with bot.retrieve_data(message.from_user.id) as data:
        min_max = message.text.split("-")
        min = 0
        max = 0

        try:
            min = int(min_max[0])
            max = int(min_max[1])
        except Exception as e:
            print(e)

        user = json.loads(data['user'])
        data['from_min_amount'] = min
        data['from_max_amount'] = max
        bot.send_message(
            user_id,
            text=_(user['language_code'], 'create_pair_input_from_country_code').format(data['from_name'])
        )

    bot.set_state(user_id, CreatePair.A4)

@bot.message_handler(is_chat=False, state=CreatePair.A4, role=['admin'])
def create_pair_a4(message):
    """ Сохранение кода страны для отдаваемой пары
        и ввод кода страны для получаемой пары
    """
    user_id = message.from_user.id
    with bot.retrieve_data(message.from_user.id) as data:
        user = json.loads(data['user'])
        data['from_country_code'] = message.text
        bot.send_message(
            user_id,
            text=_(user['language_code'], 'create_pair_input_from_country_code').format(data['to_name'])
        )

    bot.set_state(user_id, CreatePair.A5)

@bot.message_handler(is_chat=False, state=CreatePair.A5, role=['admin'])
def create_pair_a5(message):
    """ Сохранение кода страны для получаемой пары
        и ввод спреда
    """
    user_id = message.from_user.id
    with bot.retrieve_data(message.from_user.id) as data:
        user = json.loads(data['user'])
        data['to_country_code'] = message.text
        bot.send_message(
            user_id,
            text=_(user['language_code'], 'create_pair_input_spread')
        )

    bot.set_state(user_id, CreatePair.A6)

@bot.message_handler(is_chat=False, state=CreatePair.A6, role=['admin'])
def create_pair_a5(message):
    """ Сохранение спреда
        и создание пары
    """
    user_id = message.from_user.id
    with bot.retrieve_data(message.from_user.id) as data:
        user = json.loads(data['user'])

        try:
            data['spread'] = float(message.text)
        except Exception as e:
            data['spread'] = 0

        try:
            text = _(
                user['language_code'],
                'create_pair_view_info'
            ).format(**{
                "from_name": data['from_name'],
                "from_min_amount": data['from_min_amount'],
                "from_max_amount": data['from_max_amount'],
                "from_country_code": data['from_country_code'],
                "to_name": data['to_name'],
                "to_country_code": data['to_country_code'],
                "spread": data['spread'],
            })

            bot.send_message(
                user_id,
                text=text,
                reply_markup=MenuKeyboard.accept_or_decline(
                    user,
                    cl_accept=callback_data_admin_create_pair_accept,
                    key_string_accept='inline_pair_create',
                    cl_decline=callback_data_admin_pairs,
                    key_string_decline='inline_back_to',
                )
            )
        except Exception as e:
            print(e)

    bot.set_state(user_id, CreatePair.A7)

@bot.callback_query_handler(is_chat=False, state=CreatePair.A7, func=lambda call: call.data.startswith(callback_data_admin_create_pair_accept), role=['admin'])
def create_pair_a6(call):
    """ Сохранение пары
    """
    user_id = call.from_user.id
    with bot.retrieve_data(user_id) as data:
        user = json.loads(data['user'])
        try:
            pair_id = db.create_pair(
                user['id'],
                data['from_name'],
                data['from_min_amount'],
                data['from_max_amount'],
                data['from_country_code'],
                data['to_name'],
                data['to_country_code'],
                data['spread']
            )
        except Exception as e:
            print(e)
            return

        msg = _(
            user['language_code'],
            'create_pair_success'
        ).format(**{
            "from_name": data['from_name'],
            "to_name": data['to_name'],
        })

        bot.delete_message(
            user_id,
            call.message.message_id,
        )
        bot.send_message(
            user_id,
            text=msg,
            reply_markup=MenuKeyboard.back_to(user, key_string='inline_to_pair', data=callback_data_admin_view_pair+str(pair_id))

        )

    bot.delete_state(user_id)
