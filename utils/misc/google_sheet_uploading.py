from loader import bot, db, ROOT_DIR, me
import gspread
import json

# for test
def uploading(table_id="1zjxECztH9Kxl5lx8lwJVQHg_YI-okJ0bmrTcPgymRrY"):
    """ Выгружает сделки в гугл таблицу

        debug версия
    """
    gsh_filepath = ROOT_DIR + '/data/client.json'

    gc = gspread.service_account(filename=gsh_filepath)
    sheet = gc.open_by_key(table_id)
    worksheet = sheet.get_worksheet(0)

    row_count = len(worksheet.get_all_values())
    first_empty_row = row_count + 1

    values_list = worksheet.col_values(1)

    # Маска для конвертации
    # строкой даты в datetime объект
    str_time = "%Y-%m-%d %H:%M:%S"
    data = []

    config  = db.get_config()

    deals = db.get_deals(
        name_id='status',
        data=['completed'],
        order_by='ASC'
    )

    if deals == []:
        return

    for deal in deals:
        if deal['manager_id'] == 0 or str(deal['id']) in values_list:
            continue

        user = db.get_user(deal['user_id'], name_id='id')
        manager = db.get_user(deal['manager_id'], name_id='id')

        if deal.get('from_payment_account_id') > 0:
            account = db.get_payment_accoumt(deal['from_payment_account_id'])
            deal['from_requisites'] = f"{account.get('account', '-')} ({account.get('account_info', '-')})"

        data = [
            deal['id'],
            f"@{manager['username']} ({manager['telegram_id']})",
            f"@{user['username']} ({user['telegram_id']})",
            f"{deal['from_name']} -> {deal['to_name']}",
            f"{deal['from_amount']} {deal['from_name']}",
            deal['from_requisites'],
            f"{deal['to_amount']} {deal['to_name']}",
            deal['requisites'],
            f"1 {deal['to_name']} = {deal['exchange_rate']} {deal['from_name']}",
            f"{deal['spread']}%",
            deal['profit'],
            deal['profit_asset'],
            str(deal['updated_at']),
            str(deal['created_at']),
        ]
        worksheet.insert_row(data, index=first_empty_row)
        # db.update_deal(deal['id'],  args={''})
        first_empty_row += 1
