import time
from binance_f import RequestClient
from binance_f.base.printobject import *
from contextlib import redirect_stdout
import threading
from colorama import init
from termcolor import colored

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
    print("Setting up initial prices for all available crypto!!", "\033[1m", "LET'S GO", "\033[0m")
    cryptocurrency_list = []
    for symbol in symbols:
        # print("Actual symbol:", symbol)
        cryptocurrency_list.append({symbol: get_price(bin_api, bin_key, symbol)})
    print(f"Available cryptocurrencies: {len(cryptocurrency_list)}")
    return cryptocurrency_list


def one_minute_period(bin_api: str, bin_key: str, cryptocurrencies_prices: [{str: float}], symbols: [str], changes_storage: [{str: float}], first_usage: int) -> [{str: float}]:
    # first_usage: 1-true, 0-false definie if array should be firstly filled or updated
    tmp_changes_storage: [{str: float}] = []
    print(colored('--------------------Looking for a significant differences--------------------', 'magenta', attrs=['bold']))
    for symbol, dictt in zip(symbols, cryptocurrencies_prices):
        current_price: float = get_price(bin_api, bin_key, symbol)
        for elem in dictt:
            difference: float = round((1 - (dictt[elem] / current_price)) * 100, 3)
            if abs(difference) > 0.4:
                if abs(difference) > 0.8:
                    print(colored("!!!BIG CANDLE!!!",  'red', 'on_yellow'),  colored(symbol, 'yellow', attrs=['bold']), f"-> old value: {dictt[elem]}, "
                                                                                                                        f"new value: {current_price}, "
                                                                                                                        f"difference: {difference}(%)")
                else:
                    print(f"[{symbol}]-> old value: {dictt[elem]}, new value: {current_price}, difference: {difference}(%)")
                if first_usage == 1:
                    # print("Adding element to changes_storage:", symbol)
                    changes_storage.append({symbol: dictt[elem]})
                else:
                    for i in range(len(changes_storage)):
                        if symbol in changes_storage[i]:
                            difference: float = round((1 - (changes_storage[i].get(symbol) / current_price)) * 100, 3)
                            print(colored(">>>>>DOUBLE signal",  'green', 'on_red'), "in a row for", colored(symbol, 'red', attrs=['bold']), f"""make your move now!!!
>>>>>The difference from 2 last trades for [{symbol}] -> [old_v: {changes_storage[i].get(symbol)}->new_v: {current_price}], difference: {difference}(%)""")
                    tmp_changes_storage.append({symbol: dictt[elem]})
            dictt[elem] = current_price
    if first_usage != 1:
        changes_storage.clear()
        changes_storage = tmp_changes_storage
    # print(f"New changes_storage: {changes_storage}")
    return changes_storage


def five_minutes_period(bin_api: str, bin_key: str, cryptocurrencies_prices: [{str: float}], symbols: [str]):
    # threading.Timer(240.0, five_minutes_period).start()
    time.sleep(240)
    print(colored("""\n----------------------------------------
              FIVE MINUTES PERIOD
----------------------------------------""", 'green', attrs=['bold']))
    for symbol, dictt in zip(symbols, cryptocurrencies_prices):
        current_price: float = get_price(bin_api, bin_key, symbol)
        for elem in dictt:
            difference: float = round((1 - (dictt[elem] / current_price)) * 100, 3)
            if abs(difference) > 0.6:
                print(colored(symbol, 'green', attrs=['bold']), f"-> old value: {dictt[elem]}, new value: {current_price}, difference: {difference}(%)")


symbols = get_symbols_list(binance_api, secret_key)
initial_prices: [{str: float}] = create_first_array(binance_api, secret_key, symbols)
changes_signals: [{str: float}] = []


one_minute_period(binance_api, secret_key, initial_prices, symbols, changes_signals, 1)
while True:
    changes_signals = one_minute_period(binance_api, secret_key, initial_prices, symbols, changes_signals, 0)
    # print("How Changes_signal looks like in loop:", changes_signals)
