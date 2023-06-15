from loader import bot, db
from states.states import EditCountry, CreateCountry
from bot_locale.translate import translate
from keyboards.inline.menu import AdminKeyboard, MenuKeyboard
from telebot.formatting import escape_markdown
import json

callback_data_admin_params = 'admin.params'
callback_data_admin_countries = 'admin.params_countries'
callback_data_admin_view_country = 'admin.params_country_view_'
callback_data_admin_edit_country = 'admin.params_country_edit_'
callback_data_admin_create_country = 'admin.params_country_create'
callback_data_admin_create_country_accept = 'admin.params_country_create_accept'

callback_data_admin_delete_country = 'admin.params_country_delete_'
callback_data_admin_country_accept_delete = 'admin.params_country_accept_delete_'

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data == callback_data_admin_countries, is_admin=True)
def admin_countries_list(call):
    """ Отображает список стран
    """
    user = db.get_user(call.from_user.id)
    countries = db.get_countries()

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=translate(user['language_code'], 'admin_page_countries'),
        reply_markup=AdminKeyboard.countries(
            user,
            countries,
            callback_data_admin_view_country,
            back_menu_data=callback_data_admin_params,
            is_create=True
        )
    )


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_view_country), is_admin=True)
def admin_preview_country(call):
    """ Отображает содержимое и кнопки управления страны
    """
    user = db.get_user(call.from_user.id)
    counrty_id = call.data.replace(callback_data_admin_view_country ,"")
    country = db.get_country(counrty_id, name_id="id")

    if country is None:
        return

    edit_page_text = translate(
        user['language_code'],
        'admin_country_edit_home'
    ).format(
        country['name'],
        country['slug']
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=(edit_page_text),
        reply_markup=AdminKeyboard.page_country(user, country)
    )

    # Для кнопки "Назад" из редактирования страны
    bot.delete_state(call.from_user.id)

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_edit_country), is_admin=True)
def admin_edit_country(call):
    """ Редактирование страны
    """
    user = db.get_user(call.from_user.id)
    country_param = call.data.replace(callback_data_admin_edit_country, "").split("_")
    parameter = country_param[0]
    country_id = country_param[1]
    country = db.get_country(country_id, name_id="id")

    bot.set_state(call.from_user.id, EditCountry.A1)

    with bot.retrieve_data(call.from_user.id) as data:
        data['message_id'] = call.message.message_id
        data['country_id'] = country['id']
        data['parameter'] = parameter

    key_lang_string = {
        'name': 'admin_page_edit_country_name',
        'slug': 'admin_page_edit_country_code',
    }

    edit_page_text = translate(
        user['language_code'],
        key_lang_string[parameter]
    ).format(
        country['name']
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=edit_page_text,
        reply_markup=MenuKeyboard.back_to(user, key_string='inline_back_to', data=callback_data_admin_view_country+str(country['id']))
    )


@bot.message_handler(is_chat=False, state=EditCountry.A1, is_admin=True)
def edit_country_param(message):
    user = db.get_user(message.from_user.id)

    with bot.retrieve_data(message.from_user.id) as data:
        # Обрезаем
        param_value = message.text[0:4000]
        try:
            # Обновляем
            db.update_country(country_id=data['country_id'], args={data['parameter']: param_value})

            # Получаем актуальные данные и возвращаем в админку
            country = db.get_country(data['country_id'], name_id="id")
            edit_page_text = translate(
                user['language_code'],
                'admin_country_edit_home'
            ).format(
                country['name'],
                country['slug']
            )
        except Exception as e:
            print(e)

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
            text=edit_page_text,
            reply_markup=AdminKeyboard.page_country(user, country)
        )

        bot.delete_state(message.from_user.id)


###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_delete_country), is_admin=True)
def admin_delete_country(call):
    """ Предупреждение об удалении страны
    """
    user = db.get_user(call.from_user.id)
    сountry_id = call.data.replace(callback_data_admin_delete_country ,"")
    country = db.get_country(сountry_id, name_id="id")

    delete_country_text = translate(
        user['language_code'],
        'admin_data_country_delete'
    ).format(**country)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=delete_country_text,
        reply_markup=MenuKeyboard.accept_or_decline(
            user,
            cl_accept=callback_data_admin_country_accept_delete+str(country['id']),
            key_string_accept='inline_accept_delete',
            cl_decline=callback_data_admin_countries,
            key_string_decline='inline_back_to',
        )
    )


@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_country_accept_delete), is_admin=True)
def admin_delete_country_accept(call):
    """ Удаление страны (категории)
    """

    user = db.get_user(call.from_user.id)
    сountry_id = call.data.replace(callback_data_admin_country_accept_delete ,"")
    country = db.get_country(сountry_id, name_id="id")

    db.delete_object(
        table="countries",
        name_id="id",
        value=country['id']
    )

    success_delete_country_text = translate(
        user['language_code'],
        'admin_data_country_delete_success'
    ).format(**country)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=success_delete_country_text,
        reply_markup=MenuKeyboard.back_to(
            user,
            data=callback_data_admin_countries,
            key_string='inline_back_to',
        )
    )

###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data == callback_data_admin_create_country, is_admin=True)
def admin_create_country(call):
    """ Создание страны
    """
    user = db.get_user(call.from_user.id)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=translate(user['language_code'], 'admin_create_country_name'),
        reply_markup=MenuKeyboard.back_to(user, key_string='inline_back_to', data=callback_data_admin_countries)
    )

    bot.set_state(call.from_user.id, CreateCountry.A1)

    with bot.retrieve_data(call.from_user.id) as data:
        data['user'] = json.dumps(
            user,
            indent=4,
            sort_keys=True,
            default=str
        )


@bot.message_handler(is_chat=False, state=CreateCountry.A1, is_admin=True)
def admin_create_country_a1(message):

    with bot.retrieve_data(message.from_user.id) as data:
        try:
            user = json.loads(data['user'])
            data['country_name'] = message.text
            bot.send_message(
                chat_id=message.from_user.id,
                text=translate(user['language_code'], 'admin_create_country_code')
            )
        except Exception as e:
            print(e)

    bot.set_state(message.from_user.id, CreateCountry.A2)


@bot.message_handler(is_chat=False, state=CreateCountry.A2, is_admin=True)
def admin_create_country_a2(message):

    with bot.retrieve_data(message.from_user.id) as data:
        user = json.loads(data['user'])
        data['country_code'] = message.text
        bot.send_message(
            message.from_user.id,
            translate(user['language_code'], 'admin_create_country_info').format(data['country_name'], data['country_code']),
            reply_markup=MenuKeyboard.accept_or_decline(
                user,
                cl_accept=callback_data_admin_create_country_accept,
                key_string_accept='inline_create',
                cl_decline=callback_data_admin_countries,
                key_string_decline='inline_cancel',
            )
        )

    bot.set_state(message.from_user.id, CreateCountry.A3)


@bot.callback_query_handler(is_chat=False, state=CreateCountry.A3, func=lambda call: call.data == callback_data_admin_create_country_accept, is_admin=True)
def admin_create_country(call):
    """ Запись страны в базу данных
    """
    with bot.retrieve_data(call.from_user.id) as data:
        user = json.loads(data['user'])
        country_id = db.create_country(data['country_code'], data['country_name'])
        bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text=translate(user['language_code'], 'admin_create_country_success'),
            reply_markup=MenuKeyboard.back_to(
                user,
                data=(callback_data_admin_view_country+str(country_id)),
                key_string='inline_to_country'
            )
        )
