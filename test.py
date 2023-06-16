import requests
import xml.etree.ElementTree as ET

def allocate_money(deal, cards):
    """
    Распределяет деньги по картам для новой сделки
    deal - объект сделки, содержащий информацию о цене и выбранной карте
    cards - список объектов карт, содержащих информацию об их балансах, лимитах и оборотах за текущие сутки
    """
    card_with_min_balance = None
    min_balance = float('inf')
    exhausted_cards = []
    today = datetime.now().date()

    for card in cards:
        if card.turnover_date.date() != today:  # проверяем, что оборот на карте за текущие сутки еще не был учтен, если да, то обнуляем его
            card.turnover = 0
            card.turnover_date = today
        if card.limit > deal.price and card.balance < min_balance:
            card_with_min_balance = card
            min_balance = card.balance
        else:
            exhausted_cards.append(card)

    if not card_with_min_balance:
        if exhausted_cards:
            card_with_min_balance = exhausted_cards[0]

    if card_with_min_balance:
        card_with_min_balance.balance -= deal.price
        card_with_min_balance.turnover += deal.price
        return card_with_min_balance.id

    return None  # если нет карт, которые можно использовать для оплаты сделки


def cryptoexchange_parse_rate(from_name: str, to_name: str, r: int = 2, cache_expires: int = 10) -> float:
    """ Получает файл с курсами с сайта cryptoexchange.cc
        и извлекает ставки из выбранной валютной пары.

        Если пара не найдена, возвращает словарь
        с указанными параметрами и нулевым курсом.

        :from_name:     str отдаваемый актив
        :to_name:       str получаемый актив
        :r:             int округление
        :cache_expires: int время кэшировния файла с курсами
    """
    from loader import cache, config, ROOT_DIR

    FILE_NAME = 'rates-export.xml'
    FILE_PATH = ROOT_DIR + '/data/files/'+ FILE_NAME
    RATES_XML_FILE_LINK = 'https://cryptoxchange.cc/rates-export.xml'

    STRING_CACHE = 'cryptoexchange_rates'
    CACHE_EXPIRES = cache_expires * 60
    RATES_IS_UPDATE = cache.get(STRING_CACHE)

    PAIR_RATE = {
        'from': from_name,
        'to': to_name,
        'in': 0,
        'out': 0,
    }

    if RATES_IS_UPDATE is None:
        print("ОБНООООВА")
        try:
            rates = requests.get(RATES_XML_FILE_LINK)
            with open(FILE_PATH, 'w') as x: x.write(rates.text)

            cache.set(STRING_CACHE, FILE_NAME)
            cache.expire(STRING_CACHE, CACHE_EXPIRES)
        except Exception as e:
            print(e)
            return PAIR_RATE

    tree = ET.parse(FILE_PATH)
    root = tree.getroot()

    for pair in root.findall('item'):
        rate_from_name = pair.find('from').text
        rate_to_name = pair.find('to').text
        rate_in = pair.find('in').text
        rate_out = pair.find('out').text

        if (
            from_name == rate_from_name and
            to_name == rate_to_name
        ):
            PAIR_RATE['from'] = rate_from_name
            PAIR_RATE['to'] = rate_to_name
            PAIR_RATE['in'] = round(float(rate_in), r)
            PAIR_RATE['out'] = round(float(rate_out), r)

    return PAIR_RATE

print(
    cryptoexchange_parse_rate('SBERRUB', 'USDTTRC20')
)
