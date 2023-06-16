from loader import bot, config, db, ROOT_DIR
from telebot import custom_filters
import filters, handlers
import argparse

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(filters.main_filters.IsChat())
bot.add_custom_filter(filters.main_filters.IsAdmin())
bot.add_custom_filter(filters.main_filters.IsAmount())
bot.add_custom_filter(filters.main_filters.IsCancelAction())
bot.add_custom_filter(custom_filters.IsDigitFilter())

if __name__ == '__main__':
    # Команды для выполнения функция
    command = argparse.ArgumentParser()
    command.add_argument('-db', help='Импортирование существующей базы данных из файла ./data/data.sql') # Добавляем команду
    args = command.parse_args() # Парсим переданные аргументы

    # Импортирует базу, если требуется
    if args.db == 'import':
        print("Импортирую базу данных...")
        db.create_structure(ROOT_DIR)

    try:
        # Уведомляем о запуске
        print("Бот запущен!")

        # Запускаем
        bot.infinity_polling(
            restart_on_change=config.getboolean('DEFAULT', 'debug')
        )
    except Exception as e:
        print(e)
