import errno
import multiprocessing
import time
from contextlib import redirect_stdout
from datetime import datetime, timedelta
from socket import error as SocketError

from binance_f import RequestClient
from binance_f.base.printobject import *


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = "\033[35m"
    BOLD = '\033[1m'
    END = '\033[0m'
    UNDERLINE = "\033[4m"
    BackgroundLightYellow = "\033[103m"
    BackgroundLightRed = "\033[101m"
    BackgroundLightGray = "\033[47m"


binance_api: str = 'PMboj6WZwCdSSLEL0RvvSiWuaTkYMzFXgabNwisbzNhGuogw0wK68aRGEg1KlepZ'
secret_key: str = 'HVerz1NkXi2PWW4D4PY7gm498tHYwzx6Kd636UXSwwHonL3YDmUhCHCULD5KR2qR'


def get_price(bin_api: str, bin_key: str, symbol: str) -> float:
    result = None
    request_client = RequestClient(api_key=bin_api, secret_key=bin_key)
    try:
        result = request_client.get_mark_price(symbol=symbol)
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise
        pass
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
    exeptions: [str] = ['WAVEBUSD', '1000LUNCUSDT', 'ETHUSDT_220930', 'BTCUSDT_220930']
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
    print(f"Setting up initial prices for all available crypto!!{color.BOLD}{color.YELLOW} LET'S GO {color.END}")
    cryptocurrency_list = []
    for symbol in symbols:
        # print("Actual symbol:", symbol)
        cryptocurrency_list.append({symbol: get_price(bin_api, bin_key, symbol)})
    print(f"Available cryptocurrencies: {len(cryptocurrency_list)}")
    return cryptocurrency_list


def set_difference(dividend: float, divider: float) -> float:
    pass


# def one_minute_period(bin_api: str, bin_key: str, initial_prices: [{str: float}], symbols: [str]):
#     # first_usage: 1-true, 0-false define if array should be firstly filled or updated
#     multi_changes_storage: [{str: float}] = []
#     first_usage: int = 1
#     while True:
#         messages_to_print: [str] = []
#         tmp_changes_storage: [{str: float}] = []
#         print(f'{color.BLUE}{color.BOLD}-------------1min method start-------------{color.END}')
#         messages_to_print.append(f'{color.MAGENTA}{color.BOLD}--------------------ONE MINUTE PERIOD RESULTS--------------------{color.END}')
#         for symbol, dictt in zip(symbols, initial_prices):
#             current_price: float = get_price(bin_api, bin_key, symbol)
#             for elem in dictt:
#                 if current_price == 0:
#                     print(f"1min {symbol} current price is {current_price}, trying to set new current_price")
#                     current_price = get_price(bin_api, bin_key, symbol)
#                     # difference = 0
#                     # current_price = dictt[elem]
#                     difference: float = round((1 - (dictt[elem] / current_price)) * 100, 3)
#                     print(f'New current_price: {current_price}, new difference: {difference}')
#                 else:
#                     difference: float = round((1 - (dictt[elem] / current_price)) * 100, 3)
#                 if abs(difference) > 20:
#                     print(f'\n{color.RED}{color.BOLD}1min WRONG DIFFERENCE {symbol}{color.END}, actual values: previous_value:{dictt[elem]} current_price:{current_price}, '
#                           f'setting up new current_price')
#                     current_price = get_price(bin_api, bin_key, symbol)
#                     difference: float = round((1 - (dictt[elem] / current_price)) * 100, 3)
#                     print(f'New current_price: {current_price}, new difference: {difference}')
#                 if abs(difference) > 0.45:
#                     if difference > 0.8:
#                         messages_to_print.append(f"{color.RED}{color.BackgroundLightYellow}!!!BIG CANDLE!!!{color.END} {color.CYAN}{color.BOLD}"
#                                                  f"{color.UNDERLINE}{symbol}{color.END} -> old value:"
#                                                  f" {dictt[elem]}, new value: {current_price} difference:{color.GREEN}{color.BOLD} {difference}(%){color.END}")
#                     elif difference < -0.8:
#                         messages_to_print.append(
#                             f"{color.RED}{color.BackgroundLightYellow}!!!BIG CANDLE!!!{color.END} {color.CYAN}{color.BOLD}{color.UNDERLINE}{symbol}{color.END} -> old value:"
#                             f" {dictt[elem]}, new value: {current_price}, difference:{color.RED}{color.BOLD} {difference}(%){color.END}")
#                     else:
#                         messages_to_print.append(f"[{symbol}]-> old value: {dictt[elem]}, new value: {current_price}, difference: {difference}(%)")
#                     if first_usage == 1:
#                         # print("Adding element to changes_storage:", symbol)
#                         multi_changes_storage.append({symbol: dictt[elem]})
#                     else:
#                         for i in range(len(multi_changes_storage)):
#                             if symbol in multi_changes_storage[i]:
#                                 difference: float = round((1 - (multi_changes_storage[i].get(symbol) / current_price)) * 100, 3)
#                                 if difference > 0:
#                                     messages_to_print.append(
#                                         f"{color.GREEN}{color.BackgroundLightRed}{color.BOLD}>>>>>DOUBLE signal{color.END} in a row for {color.CYAN}{color.BOLD}{color.UNDERLINE}{symbol}{color.END} "
#                                         f"make your move now, difference:{color.GREEN}{color.BOLD} {difference}(%){color.END}!!!")
#                                 else:
#                                     messages_to_print.append(
#                                         f"{color.GREEN}{color.BackgroundLightRed}{color.BOLD}>>>>>DOUBLE signal{color.END} in a row for {color.CYAN}{color.BOLD}{color.UNDERLINE}{symbol}{color.END} "
#                                         f"make your move now, difference:{color.RED}{color.BOLD} {difference}(%){color.END}!!!")
#                         tmp_changes_storage.append({symbol: dictt[elem]})
#                 dictt[elem] = current_price
#         if first_usage != 1:
#             multi_changes_storage.clear()
#             multi_changes_storage = tmp_changes_storage
#         first_usage = 0
#         # messages_to_print.append(f"New changes_storage: {multi_changes_storage}")
#         for line in messages_to_print:
#             print(line)


def five_minutes_period(bin_api: str, bin_key: str, initial_prices: [{str: float}], symbols: [str]):
    # first_usage: 1-true, 0-false define if array should be firstly filled or updated
    multi_changes_storage: [{str: float}] = []
    greens: [{}] = []
    reds: [{}] = []
    first_usage: int = 1
    while True:
        messages_to_print: [str] = []
        tmp_changes_storage: [{str: float}] = []
        print(f'{color.YELLOW}{color.BOLD}-------------5min method start--------------{color.END}')
        start_time = datetime.now().strftime("%H:%M:%S")
        time.sleep(240)
        end_time = (datetime.now() + timedelta(minutes=1)).strftime("%H:%M:%S")
        messages_to_print.append(f"""{color.GREEN}{color.BOLD}\n----------------------------------------------------------
      FIVE MINUTES PERIOD RESULTS {start_time} - {end_time}
----------------------------------------------------------{color.END}""")
        start_time_tmp = datetime.now().strftime("%H:%M:%S")
        for symbol, dictt in zip(symbols, initial_prices):
            current_price: float = get_price(bin_api, bin_key, symbol)
            for elem in dictt:
                try:
                    difference: float = round((1 - (dictt[elem] / current_price)) * 100, 3)
                except ZeroDivisionError:
                    # print(f'\n{color.RED}{color.BOLD}5min DIVIDE BY 0 {symbol}{color.END}, actual values, previous_value:{dictt[elem]} current_price:{current_price}, '
                    #       f'setting up new current_price')
                    while current_price == 0:
                        current_price = get_price(bin_api, bin_key, symbol)
                    difference: float = round((1 - (dictt[elem] / current_price)) * 100, 3)
                    print(f'New current_price: {current_price}, new difference {difference}')
                while abs(difference) > 40:
                    print(f'\n{color.RED}{color.BOLD}5min WRONG DIFFERENCE {symbol}{color.END}, actual values, previous_value:{dictt[elem]} current_price:{current_price}, '
                          f'setting up new current_price')
                    current_price = get_price(bin_api, bin_key, symbol)
                    while current_price == 0:
                        current_price = get_price(bin_api, bin_key, symbol)
                    difference: float = round((1 - (dictt[elem] / current_price)) * 100, 3)
                    # print(f'New current_price: {current_price}, new difference {difference}')
                if first_usage == 1:
                    greens.append({"symbol": symbol, "multiple": 0, 'start_value': current_price, 'final_value': current_price})
                    reds.append({"symbol": symbol, "multiple": 0, 'start_value': current_price, 'final_value': current_price})
                if difference > 0:
                    for i in range(len(greens)):
                        if symbol in greens[i]['symbol']:
                            if reds[i]['multiple'] > 0:
                                greens[i]['multiple'] = 0
                                greens[i]['start_value'] = current_price
                                greens[i]['final_value'] = current_price
                            if greens[i]['multiple'] == 0:
                                greens[i]['start_value'] = current_price
                                greens[i]['final_value'] = current_price
                                greens[i]['multiple'] += 1
                            elif current_price > greens[i]['final_value']:
                                greens[i]['final_value'] = current_price
                                greens[i]['multiple'] += 1
                            else:
                                greens[i]['multiple'] = 0
                                greens[i]['start_value'] = current_price
                                greens[i]['final_value'] = current_price
                            if greens[i]['multiple'] > 2:
                                multi_difference: float = round((1 - (greens[i]['start_value'] / greens[i]["final_value"])) * 100, 5)
                                if multi_difference > 1:
                                    messages_to_print.append(f'{color.GREEN}{color.BOLD}{greens[i]["multiple"]} green move in a row for {symbol}, starting price:'
                                                             f' {greens[i]["start_value"]}, current value: {greens[i]["final_value"]}, the difference '
                                                             f'{color.BackgroundLightGray}{multi_difference}{color.END}')
                                elif multi_difference > 0.5:
                                    messages_to_print.append(f'{color.GREEN}{color.BOLD}{greens[i]["multiple"]} green move in a row for {symbol}, starting price:'
                                                             f' {greens[i]["start_value"]}, current value: {greens[i]["final_value"]}, the difference {multi_difference}{color.END}')
                else:
                    for i in range(len(reds)):
                        if symbol in reds[i]['symbol']:
                            if greens[i]['multiple'] > 0:
                                greens[i]['multiple'] = 0
                                greens[i]['start_value'] = current_price
                                greens[i]['final_value'] = current_price
                            if reds[i]['multiple'] == 0:
                                reds[i]['start_value'] = current_price
                                reds[i]['final_value'] = current_price
                                reds[i]['multiple'] += 1
                            elif current_price < reds[i]['final_value']:
                                reds[i]['final_value'] = current_price
                                reds[i]['multiple'] += 1
                            else:
                                reds[i]['multiple'] = 0
                                reds[i]['start_value'] = current_price
                                reds[i]['final_value'] = current_price
                            if reds[i]['multiple'] > 2:
                                multi_difference: float = round((1 - (reds[i]['start_value'] / reds[i]["final_value"])) * 100, 5)
                                if abs(multi_difference) > 1:
                                    messages_to_print.append(f'{color.RED}{color.BOLD}{reds[i]["multiple"]} red move in a row for {symbol}, starting price:'
                                                             f' {reds[i]["start_value"]}, current value: {reds[i]["final_value"]}, the difference '
                                                             f'{color.BackgroundLightYellow}{multi_difference}{color.END}')
                                elif abs(multi_difference) > 0.5:
                                    messages_to_print.append(f'{color.RED}{color.BOLD}{reds[i]["multiple"]} red move in a row for {symbol}, starting price:'
                                                             f' {reds[i]["start_value"]}, current value: {reds[i]["final_value"]}, the difference {multi_difference}{color.END}')
                if abs(difference) > 0.64:  # only big changes
                    messages_to_print.append(f"[{symbol}]-> old value: {dictt[elem]}, new value: {current_price}, difference: {difference}(%)")
                    if first_usage == 1:
                        multi_changes_storage.append({symbol: dictt[elem]})
                    else:
                        for i in range(len(multi_changes_storage)):
                            if symbol in multi_changes_storage[i]:
                                difference: float = round((1 - (multi_changes_storage[i].get(symbol) / current_price)) * 100, 3)
                                if difference > 0.8:
                                    messages_to_print.append(
                                        f"{color.GREEN}{color.BackgroundLightRed}{color.BOLD}>>>>>DOUBLE signal{color.END} in a row for {color.CYAN}{color.BOLD}{color.UNDERLINE}{symbol}{color.END} "
                                        f"make your move now, difference:{color.GREEN}{color.BOLD} {difference}(%){color.END}!!!")
                                elif difference < -0.8:
                                    messages_to_print.append(
                                        f"{color.GREEN}{color.BackgroundLightRed}{color.BOLD}>>>>>DOUBLE signal{color.END} in a row for {color.CYAN}{color.BOLD}{color.UNDERLINE}{symbol}{color.END} "
                                        f"make your move now, difference:{color.RED}{color.BOLD} {difference}(%){color.END}!!!")
                        tmp_changes_storage.append({symbol: dictt[elem]})
                dictt[elem] = current_price
        if first_usage != 1:
            multi_changes_storage.clear()
            multi_changes_storage = tmp_changes_storage
        first_usage = 0
        end_time_tmp = datetime.now().strftime("%H:%M:%S")
        # messages_to_print.append(f"New changes_storage: {multi_changes_storage}")
        for line in messages_to_print:
            print(line)
        print(f'\nTime spend on filling arrays {start_time_tmp} - {end_time_tmp}')


def fifteen_minutes_period(bin_api: str, bin_key: str, initial_prices: [{str: float}], symbols: [str]):
    # first_usage: 1-true, 0-false define if array should be firstly filled or updated
    multi_changes_storage: [{str: float}] = []
    first_usage: int = 1
    while True:
        messages_to_print: [str] = []
        tmp_changes_storage: [{str: float}] = []
        print(f'{color.MAGENTA}{color.BOLD}-------------15min method start-------------{color.END}')
        start_time = datetime.now().strftime("%H:%M:%S")
        time.sleep(840)
        end_time = datetime.now().strftime("%H:%M:%S")
        messages_to_print.append(f"""{color.BLUE}{color.BOLD}\n----------------------------------------------------------
      FIFTEEN MINUTES PERIOD RESULTS {start_time} - {end_time}
----------------------------------------------------------{color.END}""")
        for symbol, dictt in zip(symbols, initial_prices):
            current_price: float = get_price(bin_api, bin_key, symbol)
            for elem in dictt:
                try:
                    difference: float = round((1 - (dictt[elem] / current_price)) * 100, 3)
                except ZeroDivisionError:
                    # print(f'\n{color.RED}{color.BOLD}15min DIVIDE BY 0 {symbol}{color.END}, actual values, previous_value:{dictt[elem]} current_price:{current_price}, '
                    #       f'setting up new current_price')
                    while current_price == 0:
                        current_price = get_price(bin_api, bin_key, symbol)
                    difference: float = round((1 - (dictt[elem] / current_price)) * 100, 3)
                    # print(f'New current_price: {current_price}, new difference {difference}')
                while abs(difference) > 40:
                    print(f'\n{color.RED}{color.BOLD}15min WRONG DIFFERENCE {symbol}{color.END}, actual values, previous_value:{dictt[elem]} current_price:{current_price}, '
                          f'setting up new current_price')
                    current_price = get_price(bin_api, bin_key, symbol)
                    while current_price == 0:
                        current_price = get_price(bin_api, bin_key, symbol)
                    difference: float = round((1 - (dictt[elem] / current_price)) * 100, 3)
                    print(f'New current_price: {current_price}, new difference {difference}')
                if abs(difference) > 0.84:
                    if difference > 0:
                        messages_to_print.append(f"[{symbol}]-> old value: {dictt[elem]}, new value: {current_price}, difference: {color.GREEN}{color.BOLD}{difference}(%"
                                                 f"){color.END}")
                    else:
                        messages_to_print.append(
                            f"[{symbol}]-> old value: {dictt[elem]}, new value: {current_price}, difference: {color.RED}{color.BOLD}{difference}(%){color.END}")
                    if first_usage == 1:
                        multi_changes_storage.append({symbol: dictt[elem]})
                    else:
                        for i in range(len(multi_changes_storage)):
                            if symbol in multi_changes_storage[i]:
                                difference: float = round((1 - (multi_changes_storage[i].get(symbol) / current_price)) * 100, 3)
                                if difference > 0.8:
                                    messages_to_print.append(
                                        f"{color.GREEN}{color.BackgroundLightRed}{color.BOLD}>>>>>DOUBLE signal{color.END} in a row for {color.CYAN}{color.BOLD}{color.UNDERLINE}{symbol}{color.END} "
                                        f"make your move now, difference:{color.GREEN}{color.BOLD} {difference}(%){color.END}!!!")
                                elif difference < -0.8:
                                    messages_to_print.append(
                                        f"{color.GREEN}{color.BackgroundLightRed}{color.BOLD}>>>>>DOUBLE signal{color.END} in a row for {color.CYAN}{color.BOLD}{color.UNDERLINE}{symbol}{color.END} "
                                        f"make your move now, difference:{color.RED}{color.BOLD} {difference}(%){color.END}!!!")
                        tmp_changes_storage.append({symbol: dictt[elem]})
                dictt[elem] = current_price
        if first_usage != 1:
            multi_changes_storage.clear()
            multi_changes_storage = tmp_changes_storage
        first_usage = 0
        # messages_to_print.append(f"New changes_storage: {multi_changes_storage}")
        for line in messages_to_print:
            print(line)


if __name__ == '__main__':
    # create initial arrays
    symbolss = get_symbols_list(binance_api, secret_key)
    init_prices: [{str: float}] = create_first_array(binance_api, secret_key, symbolss)

    # multiprocessing functions
    # p1 = multiprocessing.Process(target=one_minute_period, args=(binance_api, secret_key, init_prices, symbolss,))
    p2 = multiprocessing.Process(target=five_minutes_period, args=(binance_api, secret_key, init_prices, symbolss,))
    p3 = multiprocessing.Process(target=fifteen_minutes_period, args=(binance_api, secret_key, init_prices, symbolss,))
    # p1.start()
    p2.start()
    p3.start()
    # print("How Changes_signal looks like in loop:", changes_signals)
