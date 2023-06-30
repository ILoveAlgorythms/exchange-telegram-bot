  levels = {
      1: 10,
      2: 5
  }

      def distribute_referral_balance(self, user: int, args: dict, name_id='telegram_id'):
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

# ЭТО ИСКЛЮЧИТЕЛЬНО ТЕСОВАЯ ФУНКЦИЯ

  # Функция для рекурсивного расчета распределения средств рефералам
  def distribute_referral_balance(user_id, amount, level=1, levels={ 1: 10, 2: 5 }):
      cursor = conn.cursor()
      # Получение информации о пользователе
      cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
      user = db.get_user(user_id, name_id="id")
      # Проверка наличия реферала для пользователя
      if user.get('refferer_id') is not None:
          referral_id = user.get('refferer_id') # ID реферала
          referral_percentage = levels[level]  # Процент для текущего уровня
          # Расчет и начисление средств рефералу
          referral_amount = round(10 * Decimal(referral_percentage) / 100, 2)
          cursor.execute('UPDATE users SET referral_balance = referral_balance + %s WHERE id = %s',
                         (referral_amount, referral_id))
          # Рекурсивный вызов функции для реферала
          if level <= len(levels):
              distribute_referral_balance(referral_id, referral_amount, level+1)

  # Пример использования функции
  distribute_referral_balance(1, 100)  # Распределение средств для пользователя с ID 1 и суммой 100
