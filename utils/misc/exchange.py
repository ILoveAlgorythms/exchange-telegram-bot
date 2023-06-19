from .data import cryptoexchange_parse_rate

def add_spread(num, spread):
    """ Стыкует спред
    """
    return (num - (num * (spread / 100)))

def calculate_amount(amount: float = 0, pair: dict = {}, mode: str = 'from'):
    """ Считает сумму обмена

        :amount: сумма
        :pair:   пара
        :mode:   главный from/to актив
    """

    _in =                              pair['from_name'] # отдаю
    _out =                             pair['to_name'] # получаю
    rate_from_name, rate_to_name =     pair['from_name'], pair['to_name']
    rate_from_amount, rate_to_amount = 1, 1
    orig_calculated_amount =           0 # получаемая сумма без спреда
    orig_finally_exchange_rate =       0 # курс обмена без спреда
    calculated_amount =                0 # получаемая сумма
    finally_exchange_rate =            0 # курс обмена

    if pair['price_handler'] == 'cryptoexchage':
        exchange_rate = cryptoexchange_parse_rate(
            pair['from_handler_name'],
            pair['to_handler_name']
        )

        _out = float(exchange_rate['out'])
        _in = float(exchange_rate['in'])

        if pair['handler_inverted'] == 1:
            _out, _in = _in, _out

        if mode == 'to':
            _out, _in = _in, _out

        if _out == 1:
            orig_calculated_amount = amount / _in
            calculated_amount = (round(
                amount / add_spread(_in, pair['spread']),
                3
            ))

            orig_finally_exchange_rate = round(_in, 3)
            finally_exchange_rate = round(add_spread(_in, pair['spread']), 3)
            rate_from_amount, rate_to_amount = finally_exchange_rate, 1

            if pair['handler_inverted'] == 1:
                rate_from_name, rate_to_name = pair['to_name'], pair['from_name']
                rate_from_amount, rate_to_amount = 1, finally_exchange_rate

        if _in == 1:
            orig_calculated_amount = amount * _out
            print(orig_calculated_amount)
            calculated_amount = (round(
                amount * add_spread(_out, pair['spread']),
                3
            ))
            finally_exchange_rate = round(add_spread(_out, pair['spread']), 3)
            orig_finally_exchange_rate = round(_out, 3)
            rate_from_amount, rate_to_amount = 1, finally_exchange_rate

            if pair['handler_inverted'] == 1:
                rate_from_name, rate_to_name = pair['from_name'], pair['to_name']
                rate_from_amount, rate_to_amount = finally_exchange_rate, 1

        if mode == 'to':
            calculated_amount, amount = amount, calculated_amount
            rate_from_amount, rate_to_amount = finally_exchange_rate, 1

    return {
        'from_amount':                    amount,
        'to_amount':                      calculated_amount,
        'rate_from_name':                 rate_from_name,
        'rate_from_amount':               rate_from_amount,
        'rate_to_name':                   rate_to_name,
        'rate_to_amount':                 rate_to_amount,
        'exchange_rate':                  finally_exchange_rate,
        'orig_calculated_amount':         orig_calculated_amount,
        'orig_finally_exchange_rate':     orig_finally_exchange_rate,
    }
