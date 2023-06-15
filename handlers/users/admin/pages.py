from loader import bot, db, ROOT_DIR
from states.states import EditPage
from bot_locale.translate import translate
from keyboards.inline.menu import AdminKeyboard, MenuKeyboard
from telebot.formatting import escape_markdown
import json
import os
from pathlib import Path
from datetime import datetime

callback_data_admin_pages = 'admin.pages'
callback_data_admin_preview_page = 'admin.pages.preview_'
callback_data_admin_edit_page = 'admin.pages.edit_'
callback_data_admin_add_document_page = 'admin.pages.add_document_page_'
callback_data_admin_delete_document_page = 'admin.pages.delete_document_page_'

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data == callback_data_admin_pages, is_admin=True)
def admin_pages_list(call):
    """ Отображает список страниц
    """
    user = db.get_user(call.from_user.id)
    pages = db.get_pages()

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=translate(user['language_code'], 'admin_page_home'),
        reply_markup=AdminKeyboard.pages(user, pages)
    )

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_preview_page), is_admin=True)
def admin_preview_page(call):
    """ Отображает содержимое и кнопки управления страницей
    """
    user = db.get_user(call.from_user.id)
    page_id = call.data.replace(callback_data_admin_preview_page , '')
    page = db.get_page(page_id, name_id='id')

    if page['document'] == 'null':
        pass

    edit_page_text = translate(
        user['language_code'],
        'admin_page_edit_home'
    ).format(
        page['page_title'],
        page['page_content']
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=edit_page_text,
        reply_markup=AdminKeyboard.page_edit(user, page)
    )

    # Для кнопки "Назад" из редактирования страницы
    bot.delete_state(call.from_user.id)

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_edit_page), is_admin=True)
def admin_edit_page(call):
    """ Редактирование страницы
    """
    user = db.get_user(call.from_user.id)
    page_id = call.data.replace(callback_data_admin_edit_page, "")
    page = db.get_page(page_id, name_id="id")

    bot.set_state(call.from_user.id, EditPage.A1)

    with bot.retrieve_data(call.from_user.id) as data:
        data['message_id'] = call.message.message_id
        data['page_id'] = page['id']

    edit_page_text = translate(
        user['language_code'],
        'admin_page_edit_tmp'
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=translate(user['language_code'], 'admin_page_edit_text').format(page['page_title']),
        reply_markup=MenuKeyboard.back_to(user, key_string='inline_back_to', data=callback_data_admin_preview_page+str(page['id']))
    )

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_delete_document_page), is_admin=True)
def admin_delete_document_page(call):
    """ Удаление документа у страницы
    """
    user = db.get_user(call.from_user.id)
    page_id = call.data.replace(callback_data_admin_delete_document_page, "")
    page = db.get_page(page_id, name_id="id")

    db.update_page(page_id=page_id, args={'document': "null"})

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=translate(user['language_code'], 'admin_page_document_deleted').format(page['page_title']),
        reply_markup=MenuKeyboard.back_to(user, key_string='inline_back_to', data=callback_data_admin_preview_page+str(page['id']))
    )

@bot.callback_query_handler(is_chat=False, func=lambda call: call.data.startswith(callback_data_admin_add_document_page), is_admin=True)
def admin_add_document_page(call):
    """ Добавление документа к странице
    """
    user = db.get_user(call.from_user.id)
    page_id = call.data.replace(callback_data_admin_add_document_page, "")
    page = db.get_page(page_id, name_id="id")

    bot.set_state(call.from_user.id, EditPage.B1)

    with bot.retrieve_data(call.from_user.id) as data:
        data['message_id'] = call.message.message_id
        data['page'] = json.dumps(
            page,
            indent=4,
            sort_keys=True,
            default=str
        )

    edit_page_text = translate(
        user['language_code'],
        'admin_page_edit_tmp'
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=translate(user['language_code'], 'admin_page_add_document').format(page['page_title']),
        reply_markup=MenuKeyboard.back_to(user, key_string='inline_back_to', data=callback_data_admin_preview_page+str(page['id']))
    )


@bot.message_handler(is_chat=False, state=EditPage.B1, content_types=['audio', 'animation', 'sticker', 'video_note', 'voice', 'contact', 'location', 'venue', 'dice', 'invoice', 'successful_payment', 'text', 'photo', 'video'])
def not_supported_message(message):
    """ Если пользователь отправил
        неподдерживаемый тип контента
        сообщаем ему об этом
    """
    user = db.get_user(message.from_user.id)
    with bot.retrieve_data(message.from_user.id) as data:
        bot.send_message(
            message.from_user.id,
            translate(user['language_code'], 'deal_file_not_supported')
        )


@bot.message_handler(is_chat=False, state=EditPage.B1, content_types=['document'])
def not_supported_message(message):
    """ Прикрепляем документ к странице

        Only для одного файла :)
    """
    user = db.get_user(message.from_user.id)
    page_id = 0

    file_data = {
        'path': '',
        'file_id': '',
    }
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_data['path'] = "/media/" + message.document.file_name
    file_data['file_id'] = message.document.file_id
    file_path = ROOT_DIR + file_data['path']

    if Path(file_path).is_file():
        os.remove(file_path)

    with open(file_path, 'wb') as document:
        document.write(downloaded_file)

    with bot.retrieve_data(message.from_user.id) as data:
        page = json.loads(data['page'])
        page_id = page['id']

        db.update_page(page_id=page_id, args={'document': json.dumps(file_data, indent=4, sort_keys=True, default=str)})

        bot.send_message(
            message.from_user.id,
            translate(
                user['language_code'],
                'admin_page_document_attached'
            ).format(
                escape_markdown(page['page_title'])
            ),
            reply_markup=MenuKeyboard.back_to(user, key_string='inline_back_to', data=callback_data_admin_preview_page+str(page['id']))
        )

    bot.delete_state(message.from_user.id)


@bot.message_handler(is_chat=False, state=EditPage.A1, is_admin=True)
def edit_page_text(message):
    user = db.get_user(message.from_user.id)

    with bot.retrieve_data(message.from_user.id) as data:
        # Обрезаем лишние символы
        new_page_text = escape_markdown(message.text[0:4000])

        # Обновляем страницу
        db.update_page(page_id=data['page_id'], args={'page_content': new_page_text})

        # Получаем актуальные данные и возвращаем в админку
        page = db.get_page(data['page_id'], name_id="id")
        edit_page_text = translate(
            user['language_code'],
            'admin_page_edit_home'
        ).format(
            page['page_title'],
            page['page_content']
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
            text=translate(user['language_code'], 'admin_page_success_edit').format(page['page_title'])
        )
        bot.send_message(
            chat_id=message.chat.id,
            text=edit_page_text,
            reply_markup=AdminKeyboard.page_edit(user, page)
        )

        bot.delete_state(message.from_user.id)
