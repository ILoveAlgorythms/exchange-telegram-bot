from telebot.handler_backends import State, StatesGroup

class ExchageState(StatesGroup):
    """ Состояние бота во время
        формирования обмена.

        :A1: Выбор валютной пары;
        :A2: Выбор банка из которого будут перечислены средства;
        :A3: Выбор банка в который будут получены средства;
        :A4: Ввод номера банковской карты карты;
        :A5: Ввод суммы;
        :A6: Получение котировок;
        :A7: Создание ордера и вывод информации о нём.
    """
    A1 = State()
    A2 = State()
    A3 = State()
    A4 = State()
    A5 = State()
    A6 = State()
    A7 = State()

class EditCountry(StatesGroup):
    """ Редактирование страны
    """
    A1 = State()

class PaymentAccount(StatesGroup):
    """ Создание платёжного счтеа
    """
    create = State()

class EditBank(StatesGroup):
    """ Редактирование банка
    """
    A1 = State()

class CreateCountry(StatesGroup):
    """ Создание страны
    """
    A1 = State()
    A2 = State()
    A3 = State()

class CreateBank(StatesGroup):
    """ Создание банка
    """
    A1 = State()
    A2 = State()
    A3 = State()

class EditLimit(StatesGroup):
    """ Редактирование лимитов
    """
    A1 = State()

class EditPage(StatesGroup):
    """ Редактирование страницы
    """
    A1 = State()
    B1 = State()

class EditPair(StatesGroup):
    """ Редактирование валютной пары
    """
    A1 = State()

class CreatePair(StatesGroup):
    """ Создание валютной пары
    """
    A1 = State()
    A2 = State()
    A3 = State()
    A4 = State()
    A5 = State()
    A6 = State()
    A7 = State()

class SupportState(StatesGroup):
    """ Создание тикета в поддержку

        :A1: Выбор причины;
        :A2: Ввод сообщения;
        :A3: Отправка.
    """
    A1 = State()
    A2 = State()
    A3 = State()

class UserDeal(StatesGroup):
    """ Изменение статуса сделки у пользователя

        :requisites: Передача реквизитов;
        :dispute:    Создание претензии;
        :chat:       Открывает чат;
    """
    requisites = State()
    dispute = State()
    chat = State()

class AdminDeal(StatesGroup):
    """ Изменение статуса сделки в админке

        :requisites: Выдача реквизитов;
        :message:    Ввод сообщения;
        :chat:       Открывает чат;
    """
    requisites = State()
    message = State()
    chat = State()
    profit = State()

class AdminTicket(StatesGroup):
    """ Изменение тикета в админке

        :chat:       Открывает чат;
    """
    message = State()
    chat = State()

class AdminDealSearch(StatesGroup):
    """ Поиск сделок

        :by_id:   Поиск по ID;
        :message: Поиск по telegram id / username;
    """
    by_id = State()
    uid_or_uname = State()
