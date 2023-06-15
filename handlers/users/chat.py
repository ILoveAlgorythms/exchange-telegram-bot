from loader import bot, db
from states.states import ExchageState
from bot_locale.translate import translate
from keyboards.inline.menu import ChatKeyboard

callback_data_switc_notifications = 'admin.chat.notifications_switch_'

@bot.message_handler(is_chat=True, commands=['start'], is_admin=True)
def chat_home(message):
    """ Chat /start
        Отображает меню подключения уведомлений
        о новых сделках, новых обращений и тд
        к группе, в которой находится бот
    """
    user = db.get_user(message.from_user.id)
    config = db.get_config()
    chat_id = message.chat.id
    status_text = translate(user['language_code'], 'dict_notifications_status')

    bot.send_message(message.chat.id, translate(user['language_code'], 'chat_home_notifications'), reply_markup=ChatKeyboard.home(user, message.chat.id, config))

@bot.callback_query_handler(func=lambda call: call.data.startswith(callback_data_switc_notifications), is_chat=True, is_admin=True)
def chat_notifications_switcher(call):
    """ Изменение настроек уведомлений
        в группе
    """
    calldata = call.data.replace(callback_data_switc_notifications, "")
    user = db.get_user(call.from_user.id)
    config = db.get_config()

    # Подключает уведомления о новых сделках для чата
    if (
        calldata == 'deals' and
        call.message.chat.id != config['notifications_deal_chat_id']
    ):
        # Если до этого уведомления были подключены в другом чате,
        # сообщаем в нём, что уведомления были отключены
        if config['notifications_deal_chat_id'] is not None:
            try:
                bot.send_message(
                    config['notifications_deal_chat_id'],
                    translate(user['language_code'], 'chat_swith_disabled_notify_deals')
                )
                # Выходим из группы
                # bot.leave_chat(
                #     call.message.chat.id
                # )
            except Exception as e:
                pass

        # Обновляем данные
        db.update_config({
            'notifications_deal_chat_id': call.message.chat.id
        })
        # Сообщаем об успешном изменении
        bot.answer_callback_query(
            call.id,
            text=translate(user['language_code'], 'chat_swith_notify_deals'),
            show_alert=True,
        )

    # Подключает уведомления о тикетах в поддержку для чата
    if (
        calldata == 'support' and
        call.message.chat.id != config['notifications_support_chat_id']
    ):
        # Если до этого уведомления были подключены в другом чате,
        # уведомляем в нём, что уведомления были отключены
        if config['notifications_support_chat_id'] is not None:
            try:
                bot.send_message(
                    config['notifications_support_chat_id'],
                    translate(user['language_code'], 'chat_swith_disabled_notify_support')
                )
                # Выходим из группы
                # bot.leave_chat(
                #     call.message.chat.id
                # )
            except Exception as e:
                pass

        # Обновляем данные
        db.update_config({
            'notifications_support_chat_id': call.message.chat.id
        })
        # Сообщаем об успешном изменении
        bot.answer_callback_query(
            call.id,
            text=translate(user['language_code'], 'chat_swith_notify_support'),
            show_alert=True,
        )

    # Обновляем данные конфига и выводим новую информацию
    config = db.get_config()

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=call.message.text,
        reply_markup=ChatKeyboard.home(user, call.message.chat.id, config)
    )
