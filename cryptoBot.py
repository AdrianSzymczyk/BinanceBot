from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from contextlib import redirect_stdout
import threading

binance_api: str = 'PMboj6WZwCdSSLEL0RvvSiWuaTkYMzFXgabNwisbzNhGuogw0wK68aRGEg1KlepZ'
secret_key: str = 'HVerz1NkXi2PWW4D4PY7gm498tHYwzx6Kd636UXSwwHonL3YDmUhCHCULD5KR2qR'


def get_price(bin_api: str, bin_key: str, symbol: str) -> float:
    request_client = RequestClient(api_key=bin_api, secret_key=bin_key)
    result = request_client.get_mark_price(symbol=symbol)
    price_str = []
    price: float = 0
    with open('data.txt', 'w') as f:
        with redirect_stdout(f):
            PrintMix.print_data(result)

    # get only price from binance data
    with open("data.txt") as f:
        try:
            for line in f.readlines()[2]:
                if line == '\n':
                    continue
                else:
                    price_str.append(line)
            price: float = float(''.join(price_str[10:]))
        except IndexError:
            pass
    # print(price)
    return price


def get_symbols_list(bin_api: str, bin_key: str) -> [str]:
    request_client = RequestClient(api_key=bin_api, secret_key=bin_key)
    result = request_client.get_exchange_information()
    # PrintMix.print_data(result.symbols)
    # save data about symbols to file
    with open('symbols.txt', 'w') as f:
        with redirect_stdout(f):
            PrintMix.print_data(result.symbols)
    # create table and fill it with crypto symbols
    exeptions: [str] = ['WAVEBUSD']
    symbols_list: [str] = []
    with open('symbols.txt') as f:
        for line in f:
            if line.startswith('symbol:'):
                value = line[7:]
                if value.replace('\n', '') in exeptions:
                    continue
                else:
                    symbols_list.append(value.replace('\n', ''))
    # print(symbols_list)
    # print(len(symbols_list))
    return symbols_list


def create_first_array(bin_api: str, bin_key: str, symbols: [str]) -> [{str: float}]:
    print("Setting up initial prices for all available crypto!! LET'S GO")
    cryptocurrency_list = []
    for symbol in symbols:
        # print("Actual symbol:", symbol)
        cryptocurrency_list.append({symbol: get_price(bin_api, bin_key, symbol)})
    print("Available cryptocurrencies: ", len(cryptocurrency_list))
    return cryptocurrency_list


def one_minute_period(bin_api: str, bin_key: str, cryptocurrencies_prices: [{str: float}], symbols: [str]):
    print("--------------------Looking for a significant differences--------------------")
    for symbol, dictt in zip(symbols, cryptocurrencies_prices):
        current_price: float = get_price(bin_api, bin_key, symbol)
        for elem in dictt:
            difference: float = round((1 - (dictt[elem]/current_price))*100, 5)
            if abs(difference) > 0.3:
                print(symbol, "old value:", dictt[elem], "new value:", current_price, "difference:", difference, "(%)")
            dictt[elem] = current_price


def five_minutes_period(bin_api: str, bin_key: str, cryptocurrencies_prices: [{str: float}], symbols: [str]):
    threading.Timer(240.0,five_minutes_period).start()
    print("""\n----------------------------------------
    FIVE MINUTES PERIOD""")
    for symbol, dictt in zip(symbols, cryptocurrencies_prices):
        current_price: float = get_price(bin_api, bin_key, symbol)
        for elem in dictt:
            difference: float = round((1 - (dictt[elem]/current_price))*100, 5)
            if abs(difference) > 0.6:
                print(symbol, "old value:", dictt[elem], "new value:", current_price, "difference:", difference, "(%)")


symbols = get_symbols_list(binance_api, secret_key)
initial_prices: [{str: float}] = create_first_array(binance_api, secret_key, symbols)

x = 0
while x < 2:
    print("Step:", x)
    one_minute_period(binance_api, secret_key, initial_prices, symbols)
    x += 1
