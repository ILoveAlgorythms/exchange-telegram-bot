from mysql.connector import connect
from datetime import datetime
import sys
import json

class Database():
    def __init__(self, host, user, password, db):
        self.host=host
        self.user=user
        self.password=password
        self.db=db

    def create_structure(self, ROOT_DIR):
        """ Импортирование базы данных
        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            try:
                with connection.cursor(dictionary=True, buffered=True) as cursor:
                    # Открываем/читаем/закрываем файл
                    sql_file = open(ROOT_DIR + '/data/data.sql', encoding='utf-8')
                    sql_data = sql_file.read()
                    sql_file.close()

                    # Разбиваем на команды
                    sql_lines = sql_data.split(';')

                    # Добавляем команды в запрос
                    for line in sql_lines:
                        if line.rstrip() != '':
                            cursor.execute(line)

                print("Импортирую базу данных...")
                # Отправляем транзакцию
                connection.commit()
                print("База данных успешно импортирована.")

            except Warning as warn:
                print('Ошибка: %s ' % warn)
                sys.exit()

    @staticmethod
    def update_format(sql, parameters: dict, sep=", ", sql_sep=False):
        if "XXX" not in sql: sql += " XXX "

        values = f"{sep} ".join([
            f"{k} = %s" for k in parameters
        ])

        if sql_sep: sql = sql.replace(sql, "")

        if parameters == {}:
            sql = sql.replace(sql, "")
        else:
            sql = sql.replace("XXX", values)

        return sql, tuple(parameters.values())

    def get_config(self):
        """ Получаем данные о конфигурации приложения
        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            with connection.cursor(dictionary=True, buffered=True) as cursor:
                    select_config_query = f"""SELECT * FROM config"""
                    cursor.execute(select_config_query)
                    return cursor.fetchone()

    def update_config(self, args: dict):
        """ Обновляем данные о конфигурации приложения

            :args: dict словарь с конфигурациями
        """
        sql, params = self.update_format("SET", args)
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            update_config_query = f"""
             UPDATE config {sql}
            """
            with connection.cursor() as cursor:
                cursor.execute(update_config_query, params)
                connection.commit()

    def delete_object(self, table, name_id, value):
        """ Удаляем объект по name_id

        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            delete_object_query = f"""
             DELETE FROM {table} WHERE {name_id} = {value}
            """
            with connection.cursor() as cursor:
                cursor.execute(delete_object_query)
                connection.commit()

    def get_banks(self, args={}):
        """ Получает список банков по параметрам
            :slug:    int|str идентификатор банка
            :name_id: str     тип идентификатора (slug/id)
        """
        sql, params = self.update_format("WHERE", args)
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            with connection.cursor(dictionary=True, buffered=True) as cursor:
                    select_banks_query = f"""SELECT * FROM banks {sql}"""
                    cursor.execute(select_banks_query, params)
                    return cursor.fetchall()

    def get_countries(self, args, start_limit=0, end_limit=50):
        """ Получает список стран

            :slug:    int|str идентификатор/ссылка страницы
            :name_id: str тип идентификатора (slug/id)
        """
        sql, params = self.update_format("WHERE", args)
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            with connection.cursor(dictionary=True, buffered=True) as cursor:
                    select_banks_query = f"""SELECT * FROM banks {sql} LIMIT {start_limit}, {end_limit}"""
                    cursor.execute(select_banks_query, params)
                    return cursor.fetchall()

    def get_country(self, id, name_id="id"):
        """ Получает страну

            :id:      int|str идентификатор/ссылка страны
            :name_id: str тип идентификатора (id/param)
        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            with connection.cursor(dictionary=True, buffered=True) as cursor:
                    select_country_query = f"""SELECT * FROM countries WHERE {name_id} = '{id}'"""
                    cursor.execute(select_country_query)
                    return cursor.fetchone()

    def get_bank(self, id, name_id="id"):
        """ Получает данные о банке

            :id:      int|str идентификатор/ссылка банка
            :name_id: str тип идентификатора (id/param)
        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            with connection.cursor(dictionary=True, buffered=True) as cursor:
                    select_bank_query = f"""SELECT * FROM banks WHERE {name_id} = '{id}'"""
                    cursor.execute(select_bank_query)
                    return cursor.fetchone()

    def get_page(self, slug, name_id="slug"):
        """ Получает данные о странице

            :slug:    int|str идентификатор/ссылка страницы
            :name_id: str тип идентификатора (slug/id)
        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            with connection.cursor(dictionary=True, buffered=True) as cursor:
                    select_page_query = f"""SELECT * FROM pages WHERE {name_id} = '{slug}'"""
                    cursor.execute(select_page_query)
                    return cursor.fetchone()

    def update_page(self, page_id=1, name_id="id", args: dict = {}):
        """ Обновляем данные о странице

            :page_id: int  идентификатор страницы
            :name_id: str  тип идентификатора
            :args:    dict словарь с данными для обновления
        """
        sql, params = self.update_format("SET", args)
        with connect(host=self.host, user=self.user, password=self.password, database=self.db, buffered=True) as connection:
            update_page_query = f"""
             UPDATE pages {sql} WHERE {name_id} = {page_id}
            """
            with connection.cursor() as cursor:
                cursor.execute(update_page_query, params)
                connection.commit()

    def get_payment_account(self, id, name_id="id"):
        """ Получает данные о платежном аккаунте

            :slug:    int|str идентификатор/ссылка страницы
            :name_id: str тип идентификатора (slug/id)
        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            with connection.cursor(dictionary=True, buffered=True) as cursor:
                    select_pa_query = f"""SELECT * FROM payment_accounts WHERE {name_id} = '{id}'"""
                    cursor.execute(select_pa_query)
                    return cursor.fetchone()

    def update_payment_account(self, account_id=1, name_id="id", args: dict = {}):
        """ Обновляем данные о платежном аккаунте

            :account_id: int  идентификатор аккаунта
            :name_id:    str  тип идентификатора
            :args:       dict словарь с данными для обновления
        """
        sql, params = self.update_format("SET", args)
        with connect(host=self.host, user=self.user, password=self.password, database=self.db, buffered=True) as connection:
            update_pa_query = f"""
             UPDATE payment_accounts {sql} WHERE {name_id} = {account_id}
            """
            with connection.cursor() as cursor:
                cursor.execute(update_pa_query, params)
                connection.commit()


    def update_bank(self, bank_id=1, name_id="id", args: dict = {}):
        """ Обновляем данные о банке

            :page_id: int  идентификатор страницы
            :name_id: str  тип идентификатора
            :args:    dict словарь с данными для обновления
        """
        sql, params = self.update_format("SET", args)
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            update_bank_query = f"""
             UPDATE banks {sql} WHERE {name_id} = {bank_id}
            """
            with connection.cursor() as cursor:
                cursor.execute(update_bank_query, params)
                connection.commit()

    def update_country(self, country_id=1, name_id="id", args: dict = {}):
        """ Обновляем данные о стране

            :page_id: int  идентификатор страны
            :name_id: str  тип идентификатора
            :args:    dict словарь с данными для обновления
        """
        sql, params = self.update_format("SET", args)
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            update_country_query = f"""
             UPDATE countries {sql} WHERE {name_id} = {country_id}
            """
            with connection.cursor() as cursor:
                cursor.execute(update_country_query, params)
                connection.commit()

    def get_pages(self, start_limit=0, end_limit=10):
        """ Получает список всех страниц

            :start_limit: int
            :end_limit:   int
        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            with connection.cursor(dictionary=True, buffered=True) as cursor:
                    select_pages_query = f"""SELECT * FROM pages LIMIT {start_limit}, {end_limit}"""
                    cursor.execute(select_pages_query)
                    return cursor.fetchall()

    def get_countries(self, start_limit=0, end_limit=10):
        """ Получает список стран

            :start_limit: int
            :end_limit:   int
        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            with connection.cursor(dictionary=True, buffered=True) as cursor:
                    select_countries_query = f"""SELECT * FROM countries LIMIT {start_limit}, {end_limit}"""
                    cursor.execute(select_countries_query)
                    return cursor.fetchall()

    def get_pairs(self, name_id='is_active', data=[1], start_limit=0, end_limit=50):
        """ Получает список валютных пар

            :start_limit: int
            :end_limit:   int
        """
        if type(data) == list:
            data = ", ".join((f"'{i}'" for i in data))
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            with connection.cursor(dictionary=True, buffered=True) as cursor:
                    select_pairs_query = f"""SELECT * FROM pairs WHERE {name_id} IN ({data}) LIMIT {start_limit}, {end_limit}"""
                    cursor.execute(select_pairs_query)
                    return cursor.fetchall()

    def get_pair(self, id, name_id="id"):
        """ Получает данные о валютной паре

            :id:      int|str идентификатор/название
            :name_id: str     тип идентификатора (id/ticker)
        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            with connection.cursor(dictionary=True, buffered=True) as cursor:
                    select_pair_query = f"""SELECT * FROM pairs WHERE {name_id} = '{id}'"""
                    cursor.execute(select_pair_query)
                    return cursor.fetchone()

    def get_dialogs(self, data, name_id="user_id", sql='', start_limit=0, end_limit=50, order_by="DESC"):
        """ Получает список диалогов

            :data:        str|dict данные
            :name_id:     str      тип идентификатора (id)
            :start_limit: int
            :end_limit:   int
        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            if type(data) == list:
                data = ", ".join((f"'{i}'" for i in data))
            with connection.cursor(dictionary=True, buffered=True) as cursor:
                    select_dialogs_query = f"""SELECT * FROM dialogs WHERE {name_id} IN ({data}) {sql} ORDER BY id {order_by} LIMIT {start_limit}, {end_limit}"""
                    cursor.execute(select_dialogs_query)
                    return cursor.fetchall()

    def get_deals(self, data, name_id="user_id", sql='', start_limit=0, end_limit=50, order_by="DESC"):
        """ Получает список сделок пользователя

            :data:        str|dict данные
            :name_id:     str      тип идентификатора (id)
            :start_limit: int
            :end_limit:   int
        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            if type(data) == list:
                data = ", ".join((f"'{i}'" for i in data))
            with connection.cursor(dictionary=True, buffered=True) as cursor:
                    select_deals_query = f"""SELECT * FROM deals WHERE {name_id} IN ({data}) {sql} ORDER BY id {order_by} LIMIT {start_limit}, {end_limit}"""
                    cursor.execute(select_deals_query)
                    return cursor.fetchall()

    def get_accounts(self, data, name_id="bank_id", sql='', start_limit=0, end_limit=1, order_by="DESC"):
        """ Получает список аккаунтов банка

        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            if type(data) == list:
                data = ", ".join((f"'{i}'" for i in data))
            with connection.cursor(dictionary=True, buffered=True) as cursor:
                    select_accounts_query = f"""SELECT * FROM payment_accounts WHERE {name_id} IN ({data}) {sql} ORDER BY id {order_by} LIMIT {start_limit}, {end_limit}"""
                    cursor.execute(select_accounts_query)
                    return cursor.fetchall()

    def get_view(self, view_name):
        """ Получает предсавление

            :view_name: название представления
        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            with connection.cursor(dictionary=True, buffered=True) as cursor:
                    select_view_query = f"""SELECT * FROM {view_name}"""
                    cursor.execute(select_view_query)
                    return cursor.fetchall()

    def get_payment_accoumt(self, account_id):
        """ Получает счёт по ID

            :account_id:     int идентификатор счёта
        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            with connection.cursor(dictionary=True, buffered=True) as cursor:
                    select_account_query = f"""SELECT * FROM payment_accounts WHERE id = '{account_id}'"""
                    cursor.execute(select_account_query)
                    return cursor.fetchone()

    def get_deal(self, deal_id, name_id="id"):
        """ Получает сделку по ID

            :deal_id:     int идентификатор сделки
        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            with connection.cursor(dictionary=True, buffered=True) as cursor:
                    select_deal_query = f"""SELECT * FROM deals WHERE {name_id} = '{deal_id}'"""
                    cursor.execute(select_deal_query)
                    return cursor.fetchone()

    def get_dialog(self, dialog_id, name_id="id", sql=''):
        """ Получает данные о диалоге

            :dialog_id: int идентификатор
            :name_id: str тип идентификатора (id/...more...)
        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            with connection.cursor(dictionary=True, buffered=True) as cursor:
                    select_dialog_query = f"""SELECT * FROM dialogs WHERE {name_id} = '{dialog_id}' {sql}"""
                    cursor.execute(select_dialog_query)
                    return cursor.fetchone()

    def get_messages(self, args, start_limit=0, end_limit=1, filter='DESC'):
        """ Получает сообщения диалога

        """
        sql, params = self.update_format("WHERE", args)
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            with connection.cursor(dictionary=True, buffered=True) as cursor:
                    select_banks_query = f"""SELECT * FROM messages {sql} ORDER BY id {filter} LIMIT {start_limit}, {end_limit}"""
                    cursor.execute(select_banks_query, params)
                    return cursor.fetchall()

    def get_user(self, user_id, name_id="telegram_id", sql=''):
        """ Получает данные о пользователе

            :user_id: int идентификатор
            :name_id: str тип идентификатора (telegram_id/id)
        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            with connection.cursor(dictionary=True, buffered=True) as cursor:
                    select_user_query = f"""SELECT * FROM users WHERE {name_id} = '{user_id}' {sql}"""
                    cursor.execute(select_user_query)
                    return cursor.fetchone()

    def update_user(self, user: int, args: dict, name_id='telegram_id'):
        """ Обновляет данные о пользователе

            :user_id: int  идентификатор
            :name_id: str тип идентификатора (id)
            :args:    dict параметры для обновления
        """
        sql, params = self.update_format("SET", args)
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            insert_users_query = f"""
             UPDATE users {sql} WHERE {name_id} = {user}
            """
            with connection.cursor() as cursor:
                cursor.execute(insert_users_query, params)
                connection.commit()

    def update_deal(self, deal_id: int, args: dict, name_id='id'):
        """ Обновляет данные о сделке

            :deal_id: int  идентификатор
            :name_id: str тип идентификатора (id)
            :args:    dict параметры для обновления
        """
        sql, params = self.update_format("SET", args)
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            insert_deal_query = f"""
             UPDATE deals {sql} WHERE {name_id} = {deal_id}
            """
            with connection.cursor() as cursor:
                cursor.execute(insert_deal_query, params)
                connection.commit()

    def update_dialog(self, dialog_id: int, args: dict, name_id='id'):
        """ Обновляет данные о диалоге

            :dialog_id: int  идентификатор
            :name_id:   str  тип идентификатора (id)
            :args:      dict параметры для обновления
        """
        sql, params = self.update_format("SET", args)
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            insert_dialog_query = f"""
             UPDATE dialogs {sql} WHERE {name_id} = {dialog_id}
            """
            with connection.cursor() as cursor:
                cursor.execute(insert_dialog_query, params)
                connection.commit()

    def update_pair(self, pair_id: int, args: dict, name_id='id'):
        """ Обновляет данные о паре

            :pair_id: int  идентификатор
            :name_id: str тип идентификатора (id)
            :args:    dict параметры для обновления
        """
        sql, params = self.update_format("SET", args)
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            insert_pair_query = f"""
             UPDATE pairs {sql} WHERE {name_id} = {pair_id}
            """
            with connection.cursor() as cursor:
                cursor.execute(insert_pair_query, params)
                connection.commit()

    def create_user(self, user, lang='ru'):
        """ Создаёт пользователя

            :user: object message.from_user
            :lang: str код языка
        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            insert_user_query = f"""
             INSERT INTO users (telegram_id, language_code, username, created_at)
             VALUES
                 ({user.id}, "{lang}", "{user.username}", "{datetime.now()}")
            """
            with connection.cursor() as cursor:
                cursor.execute(insert_user_query)
                connection.commit()
                return cursor.fetchone()

    def create_country(self, slug, name):
        """ Создаёт страну

        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            insert_country_query = f"""
             INSERT INTO countries (slug, name, created_at)
             VALUES
                 ("{slug}", "{name}", "{datetime.now()}")
            """
            with connection.cursor() as cursor:
                cursor.execute(insert_country_query)
                connection.commit()
                return cursor.lastrowid

    def create_bank(self, name, country_code, slug='-'):
        """ Создаёт банк

        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            insert_bank_query = f"""
             INSERT INTO banks (name, country_code, slug, created_at)
             VALUES
                 ("{name}", "{country_code}", "{slug}", "{datetime.now()}")
            """
            with connection.cursor() as cursor:
                cursor.execute(insert_bank_query)
                connection.commit()
                return cursor.lastrowid

    def create_dialog(self, user_id, deal_id=0, title='Dialog', type='support', status='open'):
        """ Создаёт диалог

        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            insert_dialog_query = f"""
             INSERT INTO dialogs (user_id, deal_id, type, status, title, created_at)
             VALUES
                 ({user_id}, {deal_id}, "{type}", "{status}", "{title}", "{datetime.now()}")
            """
            with connection.cursor() as cursor:
                cursor.execute(insert_dialog_query)
                connection.commit()
                return cursor.lastrowid

    def create_message(self, user_id, dialog_id=0, text='Msg', attach={}, content_type='text'):
        """ Создаёт сообщение в диалоге

        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            insert_message_query = f"""
             INSERT INTO messages (user_id, dialog_id, text, attach, content_type, created_at)
             VALUES
                 ({user_id}, {dialog_id}, "{text}", '{json.dumps(attach)}', "{content_type}", "{datetime.now()}")
            """
            with connection.cursor() as cursor:
                cursor.execute(insert_message_query)
                connection.commit()
                return cursor.lastrowid

    def create_pair(self, user_id, from_name, from_min_amount, from_max_amount, from_country_code, to_name, to_country_code, spread):
        """ Создаёт валютную пару в админке

        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            insert_pair_query = f"""
             INSERT INTO pairs (user_id, from_name, min_from_amount, max_from_amount, from_country_code, to_name, to_country_code, spread, created_at)
             VALUES
                 ({user_id}, "{from_name}", {from_min_amount}, {from_max_amount}, "{from_country_code}", "{to_name}", "{to_country_code}", {spread}, "{datetime.now()}")
            """
            with connection.cursor() as cursor:
                cursor.execute(insert_pair_query)
                connection.commit()
                return cursor.lastrowid

    def create_payment_account(self, user_id, bank_id, rows):
        """ Создаёт платежные аккаунты для банков

            :user_id:
            :bank_id:
            :row:
        """
        data = []
        for row in rows: data.append(tuple(row.values()))

        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            insert_payment_account_query = f"""
             INSERT INTO payment_accounts (
                user_id,       bank_id,
                account,       account_info,
                account_limit, created_at)
             VALUES (
                {user_id},
                {bank_id},
                %s, %s, %s,
                "{datetime.now()}")
             ON DUPLICATE KEY UPDATE
                status = 'active',
                account = VALUES(account),
                user_id = VALUES(user_id),
                bank_id = VALUES(bank_id);
            """
            with connection.cursor() as cursor:
                # cursor.executemany(insert_payment_account_query, data)
                for row in rows:
                    cursor.execute(insert_payment_account_query, tuple(row.values()))

                connection.commit()
                return cursor.lastrowid

    def create_deal(self, deals: dict):
        """ Создаёт сделку

            :deals: dict данные о сделке
        """
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            insert_deal_query = f"""
             INSERT INTO deals
                (user_id, uid,      from_bank_name,
                from_name,          from_amount,
                from_bank_id,       from_payment_account_id,
                to_name,            to_amount,
                orig_to_amount,     to_bank_name,
                requisites,         exchange_rate,
                orig_exchange_rate, spread,
                profit,             calculated_amount,
                status,             expires,
                created_at)
             VALUES
                 ({deals['user_id']}, UPPER(SUBSTR(MD5(RAND()),1,6)), "{deals['from_bank_name']}", "{deals['from_name']}",          {deals['from_amount']}, "{deals['from_bank_id']}", {deals['from_payment_account_id']}, "{deals['to_name']}",            "{deals['to_amount']}",  "{deals['orig_to_amount']}",     "{deals['to_bank_name']}", "{deals['requisites']}",         "{deals['exchange_rate']}", "{deals['orig_exchange_rate']}", "{deals['spread']}", "{deals.get('profit', 0)}",     "{deals['calculated_amount']}",
                 "{deals['status']}", "{deals['expires']}", "{datetime.now()}")
            """
            with connection.cursor() as cursor:
                cursor.execute(insert_deal_query)
                connection.commit()
                return cursor.lastrowid

    def get_count(self, table="users", sql=''):
        """ Кол-во строк в таблице
            :table: таблица
            :q:     по каким параметрам подсчитывать строки
        """
        # sql, params = self.update_format("WHERE", q, sep=" AND", sql_sep=sql_sep)
        with connect(host=self.host, user=self.user, password=self.password, database=self.db) as connection:
            with connection.cursor() as cursor:
                    select_count_query = f"""SELECT COUNT(*) FROM {table} {sql}"""
                    cursor.execute(select_count_query)
                    return cursor.fetchone()[0]
