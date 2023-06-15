from loader import bot, db
from states.states import EditBank, CreateBank
from bot_locale.translate import translate
from keyboards.inline.menu import AdminKeyboard, MenuKeyboard
from telebot.formatting import escape_markdown
import json

callback_data_admin_params = 'admin.params'
callback_data_admin_banks = 'admin.params_banks'
callback_data_admin_view_bank = 'admin.params_bank_view_'
callback_data_admin_edit_bank = 'admin.params_bank_edit_'
callback_data_admin_create_bank = 'admin.params_bank_create'
callback_data_admin_create_bank_accept = 'admin.params_bank_create_accept'

callback_data_admin_delete_bank = 'admin.params_bank_delete_'
callback_data_admin_bank_accept_delete = 'admin.params_bank_accept_delete_'

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data == callback_data_admin_banks, is_admin=True)
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


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_view_bank), is_admin=True)
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
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=(edit_page_text),
        reply_markup=AdminKeyboard.edit_bank(user, bank)
    )

    # Для кнопки "Назад" из редактирования страны
    bot.delete_state(call.from_user.id)

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_edit_bank), is_admin=True)
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


@bot.message_handler(is_chat=False, state=EditBank.A1, is_admin=True)
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


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_delete_bank), is_admin=True)
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


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_bank_accept_delete), is_admin=True)
def admin_delete_bank_accept(call):
    """ Удаление банка
    """

    user = db.get_user(call.from_user.id)
    bank_id = call.data.replace(callback_data_admin_bank_accept_delete ,"")
    bank = db.get_bank(bank_id, name_id="id")

    db.delete_object(
        table="banks",
        name_id="id",
        value=bank['id']
    )

    success_delete_bank_text = translate(
        user['language_code'],
        'admin_data_bank_delete_success'
    ).format(**bank)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=success_delete_bank_text,
        reply_markup=MenuKeyboard.back_to(
            user,
            data=callback_data_admin_banks,
            key_string='inline_back_to',
        )
    )

# ###########################################################################
# ###########################################################################
# ###########################################################################
# ###########################################################################
# ###########################################################################
# ###########################################################################

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data == callback_data_admin_create_bank, is_admin=True)
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


@bot.message_handler(is_chat=False, state=CreateBank.A1, is_admin=True)
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


@bot.message_handler(is_chat=False, state=CreateBank.A2, is_admin=True)
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


@bot.callback_query_handler(is_chat=False, state=CreateBank.A3, func=lambda call: call.data == callback_data_admin_create_bank_accept, is_admin=True)
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
