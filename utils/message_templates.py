from telebot.formatting import escape_markdown
from bot_locale.translate import translate
from loader import db

def get_admin_deal_text(user, deal):
    """ Возвращает текст сделки
        для администратора

        :user: объект пользователь
        :deal: объект сделка
    """
    deal_status = translate(user['language_code'], 'dict_deal_status')
    deal_status_text = translate(user['language_code'], 'dict_deal_status_text')
    user_deal = db.get_user(deal['user_id'], name_id="id")
    manager_text = "0"

    if deal['manager_id'] != 0:
        manager_deal = db.get_user(deal['manager_id'], name_id="id")
        manager_text = translate(
            user['language_code'],
            'user_data'
        ).format(**{
            'username': escape_markdown(manager_deal['username']),
            'telegram_id': manager_deal['telegram_id'],
        })

    return translate(
        user['language_code'],
        'admin_exchange_deal_info'
    ).format(**{
        "id":                 deal['id'],
        "manager":            manager_text,
        "telegram_id":        user_deal['telegram_id'],
        "username":           escape_markdown(user_deal['username']),
        "from_amount":        deal['from_amount'],
        "from_name":          deal['from_name'],
        "from_bank_name":     deal['from_bank_name'],
        "from_exchange_rate": deal['exchange_rate'],
        "orig_exchange_rate": deal['orig_exchange_rate'],
        "to_amount":          deal['to_amount'],
        "orig_to_amount":     deal['to_amount'],
        "to_name":            deal['to_name'],
        "to_bank_name":       deal['to_bank_name'],
        "spread":             deal['spread'],
        "profit":             deal['profit'],
        "requisites":         escape_markdown(deal['requisites']),
        "status_emoji":       deal_status[deal['status']],
        "status_text":        deal_status_text[deal['status']].lower(),
        "datetime":           deal['created_at'],
        "update_datetime":    deal['updated_at'],
    })
