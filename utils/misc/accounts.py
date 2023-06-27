from datetime import datetime
import re

def extract_last_use_account(dictionary):
    """ Фильтр для функции min()
        Извлекает аккаунт с самым ранним
        использованием счёта по дате.
        Отдаёт предпочтения аккаунту с NULL.
    """
    if dictionary['last_use'] is None:
        return datetime.max
    return datetime.strptime(str(dictionary['last_use']), '%Y-%m-%d %H:%M:%S')

def get_payment_account(pair: dict = {}, bank_id: int = 1) -> dict:
    """ Выбирает карту с наименьшим количеством
        дневного баланса и наименьшим числом использований

        :pair: пара
    """
    # Получаем информацию по доступным картам
    from loader import db
    card_list = db.get_view("accounts_information_per_day")

    min_sum = float('inf')
    min_uses = float('inf')
    chosen_card = {}

    # Выбираем аккаунт, который использовался раньше всех
    # или вообще не использовался (NULL) за текущие сутки (с 00:00:00)
    # min_date = min(card_list, key=extract_last_use_account)

    for card in card_list:
        if card['bank_id'] != bank_id: continue

        # Выбираем наименьшее значение (кол-во использований и суточный баланс)
        if (
            card['total_sum'] < min_sum and
            card['total_uses'] < min_uses and
            card['total_sum'] <= card['account_limit']
            # min_date['account_id'] == card['account_id']
        ):
            min_sum     = card['total_sum']
            min_uses    = card['total_uses']
            chosen_card = {
                'bank_name': card['bank_name'],
                'account_id': card['account_id'],
                'account_number': card['account_number']
            }

    return chosen_card

def account_parse_from_string(accounts, min_account_length=5, min_account_length_info=5, min_account_limit=0):
    """ Парсит счета из строки

       :account: строка с аккаунтами
    """
    accounts = accounts.split('\n')

    data = []
    errors = []

    for account in accounts:
        try:
            account = re.split(", |,", account)

            if (
                len(account[0]) < min_account_length or
                len(account[1]) < min_account_length_info or
                float(account[2]) <= min_account_limit
            ):
                errors.append(account)
                continue

            data.append({
                'account': account[0],
                'account_info': account[1],
                'account_limit': account[2],
            })
        except Exception as e:
            errors.append(account)
            print(e)

    return data, errors
