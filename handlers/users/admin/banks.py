from states.states import EditBank, CreateBank, PaymentAccount
from keyboards.inline.menu import AdminKeyboard, MenuKeyboard
from utils.misc.accounts import account_parse_from_string
from telebot.formatting import escape_markdown
from bot_locale.translate import translate
from loader import bot, db
import json

callback_data_admin_params = 'admin.params'
callback_data_admin_banks = 'admin.params_banks'
callback_data_admin_view_bank = 'admin.params_bank_view_'
callback_data_admin_edit_bank = 'admin.params_bank_edit_'
callback_data_admin_create_bank = 'admin.params_bank_create'
callback_data_admin_create_bank_accept = 'admin.params_bank_create_accept'
callback_data_admin_add_bank_acсount = 'admin.params_bank_add_bank_account_'
callback_data_admin_stats_bank_acсounts = 'admin.params_bank_stats_bank_accounts_'

callback_data_admin_delete_bank = 'admin.params_bank_delete_'
callback_data_admin_bank_accept_delete = 'admin.params_bank_accept_delete_'

def get_text_payment_accounts(bank_id):
    """ Выводит список счетов
        привязанных к банку
    """
    accounts = db.get_view("accounts_information_all_days")
    accounts_text = "\n"
    table = []

    if accounts == []:
        accounts_text = "\nнет счетов для отображения"
        return accounts_text

    for acc in accounts:
        if acc['bank_id'] != bank_id: continue

        number = acc.get('account_number')
        info = acc.get('account_info')
        total_sum = acc.get('total_sum')

        accounts_text += f"_{number}, {info}, {total_sum}_ /accdel{acc.get('account_id')}\n"

    return accounts_text

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data == callback_data_admin_banks, role=['admin', 'manager'])
def admin_banks_list(call):
    """ Отображает список банков
    """
    user = db.get_user(call.from_user.id)
    banks = db.get_banks()

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=translate(user['language_code'], 'admin_page_banks'),
        reply_markup=AdminKeyboard.banks(
            user,
            banks,
            callback_data_admin_view_bank,
            back_menu_data=callback_data_admin_params,
            is_create=True
        )
    )


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_view_bank), role=['admin', 'manager'])
def admin_preview_bank(call):
    """ Отображает содержимое и кнопки управления банком
    """
    user = db.get_user(call.from_user.id)
    bank_id = call.data.replace(callback_data_admin_view_bank ,"")
    bank = db.get_bank(bank_id, name_id="id")

    if bank is None:
        return

    edit_page_text = translate(
        user['language_code'],
        'admin_bank_edit_home'
    ).format(
        bank['name'],
        bank['country_code'],
        bank['slug'],
    )
    edit_page_text += get_text_payment_accounts(bank['id'])

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=(edit_page_text),
        reply_markup=AdminKeyboard.edit_bank(user, bank)
    )

    # Для кнопки "Назад" из редактирования страны
    bot.delete_state(call.from_user.id)

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_edit_bank), role=['admin'])
def admin_edit_bank(call):
    """ Редактирование банка
    """
    user = db.get_user(call.from_user.id)
    bank_param = call.data.replace(callback_data_admin_edit_bank, "").split("_")
    parameter = bank_param[0]
    bank_id = bank_param[1]
    bank = db.get_bank(bank_id, name_id="id")

    bot.set_state(call.from_user.id, EditBank.A1)

    if parameter == 'country': parameter = 'country_code'

    with bot.retrieve_data(call.from_user.id) as data:
        data['message_id'] = call.message.message_id
        data['bank_id'] = bank['id']
        data['parameter'] = parameter

    key_lang_string = {
        'name': 'admin_page_edit_bank_name',
        'country_code': 'admin_page_edit_bank_country',
        'slug': 'admin_page_edit_bank_slug',
    }

    edit_page_text = translate(
        user['language_code'],
        key_lang_string[parameter]
    ).format(
        bank['name']
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=edit_page_text,
        reply_markup=MenuKeyboard.back_to(user, key_string='inline_back_to', data=callback_data_admin_view_bank+str(bank['id']))
    )


@bot.message_handler(is_chat=False, state=EditBank.A1, role=['admin'])
def edit_bank_param(message):
    user = db.get_user(message.from_user.id)

    with bot.retrieve_data(message.from_user.id) as data:
        # Обрезаем
        param_value = message.text[0:256]

        # Обновляем
        db.update_bank(bank_id=data['bank_id'], args={data['parameter']: param_value})

        # Получаем актуальные данные и возвращаем в админку
        bank = db.get_bank(data['bank_id'], name_id="id")
        edit_bank_text = translate(
            user['language_code'],
            'admin_bank_edit_home'
        ).format(
            bank['name'],
            bank['country_code'],
            bank['slug'],
        )

        try:
            bot.delete_message(
                chat_id=message.chat.id,
                message_id=data['message_id']
            )
        except Exception as e:
            pass

        bot.send_message(
            chat_id=message.chat.id,
            text=translate(user['language_code'], 'admin_data_success_edit')
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=(edit_bank_text),
            reply_markup=AdminKeyboard.edit_bank(user, bank)
        )

    bot.delete_state(message.from_user.id)


# ###########################################################################
# ###########################################################################
# ###########################################################################
# ###########################################################################
# ###########################################################################
# ###########################################################################


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_add_bank_acсount), role=['admin', 'manager'])
def admin_add_payment_account(call):
    """ Добавление новых карт
    """
    user = db.get_user(call.from_user.id)
    bank_id = call.data.replace(callback_data_admin_add_bank_acсount ,"")
    bank = db.get_bank(bank_id, name_id="id")

    add_payment_accounts_text = translate(
        user['language_code'],
        'admin_data_bank_add_accounts'
    ).format(**{'bank_name': bank['name']})

    # print(db.create_payment_account(1, 1, account_parse_from_string(stri)))

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=add_payment_accounts_text,
        reply_markup=MenuKeyboard.back_to(
            user,
            data=callback_data_admin_view_bank+str(bank['id']),
            key_string='inline_back_to',
        )
    )

    bot.set_state(call.from_user.id, PaymentAccount.create)

    with bot.retrieve_data(call.from_user.id) as data:
        data['bank'] = json.dumps(
            bank,
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


@bot.message_handler(is_chat=False, state=PaymentAccount.create, role=['admin', 'manager'])
def admin_create_payment_accoount(message):
    with bot.retrieve_data(message.from_user.id) as data:
        # print(db.create_payment_account(1, 1, account_parse_from_string(stri)))
        user = json.loads(data['user'])
        bank = json.loads(data['bank'])
        accounts, acc_error = account_parse_from_string(message.text)

        key_string = 'admin_data_bank_all_stroke'
        if acc_error != []: key_string = 'admin_data_bank_not_all_stroke'

        kb = MenuKeyboard.back_to(
            user,
            data=callback_data_admin_view_bank+str(bank['id']),
            key_string='inline_back_to',
        )

        if accounts == []:
            bot.send_message(
                chat_id=message.from_user.id,
                text=translate(user['language_code'], 'error_data_not_valid'),
                reply_markup=kb
            )
            return

        success_text = translate(user['language_code'], 'admin_data_bank_add_accounts_success')
        success_text += translate(user['language_code'], key_string)

        if acc_error != []:
            for i in acc_error: success_text += "_" + ", ".join(i) + "_\n"

        try:
            db.create_payment_account(user['id'], bank['id'], accounts)
            bot.send_message(
                chat_id=message.from_user.id,
                text=success_text,
                reply_markup=kb
            )
        except Exception as e:
            print(e)

    bot.delete_state(message.from_user.id)

@bot.message_handler(is_chat=False, func=lambda message: message.text.startswith('/accdel'), role=['manager', 'admin'])
def delete_payment_account(message):
    user = db.get_user(message.from_user.id)
    lang = user['language_code']
    acc_id = message.text.replace('/accdel', '')
    account = db.get_payment_account(acc_id)
    inline_back_to = translate(lang, 'inline_back_to')
    key_string = translate(lang, 'object_not_found')
    kb = None

    if account:
        kb = MenuKeyboard.smart({
            inline_back_to: {'callback_data': callback_data_admin_view_bank+str(account['bank_id'])}
        })
        key_string = translate(lang, 'object_deleted').format(f"_{account.get('account')}, {account.get('account_info')}, {account.get('account_limit')}_")
        db.update_payment_account(acc_id, args={'status': 'deleted'})

    bot.send_message(message.from_user.id, key_string, reply_markup=kb)

# ###########################################################################
# ###########################################################################
# ###########################################################################
# ###########################################################################
# ###########################################################################
# ###########################################################################

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_delete_bank), role=['admin'])
def admin_delete_bank(call):
    """ Предупреждение об удалении банка
    """
    user = db.get_user(call.from_user.id)
    bank_id = call.data.replace(callback_data_admin_delete_bank ,"")
    bank = db.get_bank(bank_id, name_id="id")

    delete_bank_text = translate(
        user['language_code'],
        'admin_data_bank_delete'
    ).format(**bank)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=delete_bank_text,
        reply_markup=MenuKeyboard.accept_or_decline(
            user,
            cl_accept=callback_data_admin_bank_accept_delete+str(bank['id']),
            key_string_accept='inline_accept_delete',
            cl_decline=callback_data_admin_banks,
            key_string_decline='inline_back_to',
        )
    )


# ###########################################################################
# ###########################################################################
# ###########################################################################
# ###########################################################################
# ###########################################################################
# ###########################################################################

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data == callback_data_admin_create_bank, role=['admin'])
def admin_create_bank(call):
    """ Создание банка
    """
    user = db.get_user(call.from_user.id)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=translate(user['language_code'], 'admin_create_bank_name'),
        reply_markup=MenuKeyboard.back_to(user, key_string='inline_back_to', data=callback_data_admin_banks)
    )

    bot.set_state(call.from_user.id, CreateBank.A1)

    with bot.retrieve_data(call.from_user.id) as data:
        data['user'] = json.dumps(
            user,
            indent=4,
            sort_keys=True,
            default=str
        )


@bot.message_handler(is_chat=False, state=CreateBank.A1, role=['admin'])
def admin_create_bank_a1(message):

    with bot.retrieve_data(message.from_user.id) as data:
        try:
            user = json.loads(data['user'])
            data['bank_name'] = message.text
            bot.send_message(
                chat_id=message.from_user.id,
                text=translate(user['language_code'], 'admin_create_bank_code')
            )
        except Exception as e:
            print(e)

    bot.set_state(message.from_user.id, CreateBank.A2)


@bot.message_handler(is_chat=False, state=CreateBank.A2, role=['admin'])
def admin_create_bank_a2(message):

    with bot.retrieve_data(message.from_user.id) as data:
        user = json.loads(data['user'])
        data['bank_code'] = message.text
        bot.send_message(
            message.from_user.id,
            translate(user['language_code'], 'admin_create_bank_info').format(data['bank_name'], data['bank_code']),
            reply_markup=MenuKeyboard.accept_or_decline(
                user,
                cl_accept=callback_data_admin_create_bank_accept,
                key_string_accept='inline_create',
                cl_decline=callback_data_admin_banks,
                key_string_decline='inline_cancel',
            )
        )

    bot.set_state(message.from_user.id, CreateBank.A3)


@bot.callback_query_handler(is_chat=False, state=CreateBank.A3, func=lambda call: call.data == callback_data_admin_create_bank_accept, role=['admin'])
def admin_create_bank(call):
    """ Запись банка в базу данных
    """
    with bot.retrieve_data(call.from_user.id) as data:
        user = json.loads(data['user'])
        bank_id = db.create_bank(data['bank_name'], data['bank_code'])
        bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text=translate(user['language_code'], 'admin_create_bank_success'),
            reply_markup=MenuKeyboard.back_to(
                user,
                data=(callback_data_admin_view_bank+str(bank_id)),
                key_string='inline_to_bank'
            )
        )
