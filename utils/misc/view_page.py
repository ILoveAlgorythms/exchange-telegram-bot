from loader import bot, db, ROOT_DIR
from bot_locale.translate import _
from keyboards.inline.menu import MenuKeyboard
from telebot.formatting import escape_markdown
import json

def page_send_message(chat_id, user, page, kb=None):
    """ Отпрвляет страницу
        с файлом или без
    """
    if page.get("document") != "null":
        document = json.loads(page['document'])
        file = document['file_id']

        try:
            bot.get_file(file)
        except Exception as e:
            file = open(ROOT_DIR + document['path'], 'rb')

        bot.send_document(
            chat_id=chat_id,
            document=file,
            caption=escape_markdown(page.get(
                'page_content',
                _(user['language_code'], 'page_not_found')
            )),
            reply_markup=kb
        )

        return

    bot.send_message(
        chat_id=chat_id,
        text=escape_markdown(page.get(
            'page_content',
            _(user['language_code'], 'page_not_found')
        )),
        reply_markup=kb
    )
