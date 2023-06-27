import time
import schedule
from loader import bot, db
from datetime import datetime
from bot_locale.translate import translate
from utils.misc.data import cryptoexchange_parse_rate
from keyboards.inline.menu import MenuKeyboard

def exceed_time_deal():
    """ Ищет просроченные сделки на n-минут,
        закрывает их и отправляет уведомление
        пользователю о закрытии.
    """
    # Конфигурации
    config  = db.get_config()
    # Ищем сделки имеющие статус process
    # с истёкшим сроком
    deals = db.get_deals(
        name_id='status',
        data=['process'],
    )

    # Маска для конвертации
    # строкой даты в datetime объект
    str_time = "%Y-%m-%d %H:%M:%S"

    if deals == []:
        return

    for deal in deals:
        user = db.get_user(deal['user_id'], name_id="id")
        now = datetime.now()
        uat = datetime.strptime(str(deal['updated_at']), str_time)
        diff = now - uat

        pay_time = float(deal['expires']) * 60

        if diff.total_seconds() > pay_time:
            db.update_deal(
                deal['id'],
                {'status': 'declined'}
            )

            srting_back_to = _(user_deal['language_code'], 'inline_back_to_main_menu')

            msg = translate(
                user['language_code'],
                'deal_system_canceled'
            ).format(**{
                "id": deal['id']
            })
            bot.send_message(
                chat_id=user['telegram_id'],
                text=msg,
                reply_markup=MenuKeyboard.smart({
                    srting_back_to: {'callback_data': 'bot.back_to_main_menu'}
                })
            )

            print(f"[{datetime.now()}] Сделка №{deal['id']} отменена системой")

# Парсинг актуальных курсов валют из cryptoexchange.cc
schedule.every(10).minutes.do(cryptoexchange_parse_rate, from_name='SBERRUB', to_name='WISEEUR', is_update=True)

# Проверяет и отменяет просроченные сделки
schedule.every().minute.do(exceed_time_deal)

while True:
    schedule.run_pending()
    time.sleep(1)
