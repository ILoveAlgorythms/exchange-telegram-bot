from keyboards.inline.menu import AdminKeyboard, MenuKeyboard
from telebot.formatting import escape_markdown
from bot_locale.translate import _
from loader import db

def get_admin_deal_text(user, deal):
    """ Возвращает текст сделки
        для администратора

        :user: объект пользователь
        :deal: объект сделка
    """
    deal_status = _(user['language_code'], 'dict_deal_status')
    deal_status_text = _(user['language_code'], 'dict_deal_status_text')
    user_deal = db.get_user(deal['user_id'], name_id="id")
    manager_text = _(user['language_code'], 'manager_not_exist')
    from_requisites = deal['from_requisites']

    if deal['manager_id'] != 0:
        manager_deal = db.get_user(deal['manager_id'], name_id="id")
        manager_text = _(
            user['language_code'],
            'user_data'
        ).format(**{
            'username': escape_markdown(manager_deal['username']),
            'telegram_id': manager_deal['telegram_id'],
        })

    if deal.get('from_payment_account_id') > 0:
        account = db.get_payment_accoumt(deal['from_payment_account_id'])
        from_requisites = f"{account.get('account', '-')} ({account.get('account_info', '-')})"

    return _(
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
        "from_requisites":    from_requisites,
        "from_exchange_rate": deal['exchange_rate'],
        "orig_exchange_rate": deal['orig_exchange_rate'],
        "to_amount":          deal['to_amount'],
        "orig_to_amount":     deal['to_amount'],
        "to_name":            deal['to_name'],
        "to_bank_name":       deal['to_bank_name'],
        "spread":             deal['spread'],
        "profit":             deal['profit'],
        "profit_asset":       escape_markdown(deal['profit_asset']),
        "requisites":         escape_markdown(deal['requisites']),
        "status_emoji":       deal_status[deal['status']],
        "status_text":        deal_status_text[deal['status']].lower(),
        "datetime":           deal['created_at'],
        "update_datetime":    deal['updated_at'] or _(user['language_code'], 'string_updated_at_none'),
    })

def get_requisites_text(user, deal, requisites):
    """ Возвращает текст выдачи реквизитов
        для пользователя и объект клавиатуры

        :user: объект пользователь
        :deal: объект сделка
    """
    deal_status = _(user['language_code'], 'dict_deal_status')
    deal_status_text = _(user['language_code'], 'dict_deal_status_text')
    user_deal = db.get_user(deal['user_id'], name_id="id")
    lang = user_deal['language_code']

    string_paid = _(lang, 'inline_deal_user_deal_paid_')
    string_new_exchange = _(lang, 'inline_create_new_exchange')
    string_back_menu = _(lang, 'inline_back_to_main_menu')

    kb = MenuKeyboard.smart({
        string_paid: {
            'callback_data':  'bot.deal_change_status_accept_'+str(deal['id'])
        },
        string_new_exchange: {
            'callback_data':  'bot.set.new_exchange'
        },
        string_back_menu: {
            'callback_data':  'inline_back_to_main_menu'
        }
    })

    if deal.get('from_payment_account_id') > 0:
        account = db.get_payment_accoumt(deal['from_payment_account_id'])
        requisites = f"{account.get('account', '-')} ({account.get('account_info', '-')})"


    return _(
        user_deal['language_code'],
        'user_deal_send_requisites_message'
    ).format(**{
        "id":              deal['id'],
        "from_name":       deal['from_name'],
        "from_amount":     deal['from_amount'],
        "from_bank_name":  deal['from_bank_name'],
        "to_name":         deal['to_name'],
        "to_amount":       deal['to_amount'],
        "to_bank_name":    deal['to_bank_name'],
        "requisites":      requisites
    }), kb


def get_user_deal_text(user, deal):
    deal_status = _(user['language_code'], 'dict_deal_status')
    deal_status_text = _(user['language_code'], 'dict_deal_status_text')

    if deal.get('from_payment_account_id') > 0:
        account = db.get_payment_accoumt(deal['from_payment_account_id'])
        deal['from_requisites'] = f"{account.get('account', '-')} ({account.get('account_info', '-')})"

    deal_text = _(
        user['language_code'],
        'my_exchange_deal_info'
    ).format(**{
        "id":                 deal['id'],
        "from_amount":        deal['from_amount'],
        "from_name":          deal['from_name'],
        "from_bank_name":     deal['from_bank_name'],
        "from_exchange_rate": deal['exchange_rate'],
        "from_requisites":    escape_markdown(deal['from_requisites']),
        "to_amount":          deal['to_amount'],
        "to_name":            deal['to_name'],
        "to_bank_name":       deal['to_bank_name'],
        "requisites":         escape_markdown(deal['requisites']),
        "status_emoji":       deal_status[deal['status']],
        "status_text":        deal_status_text[deal['status']].lower(),
        "datetime":           deal['created_at'],
        "update_datetime":    deal['updated_at'] or _(user['language_code'], 'string_updated_at_none'),
    })

    return deal_text, MenuKeyboard.deal(user, deal)
