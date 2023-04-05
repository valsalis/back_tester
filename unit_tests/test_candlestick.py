import sys
sys.path.append('C:\git\back_tester')

import library as lib

# print(dir(vs))

# candlestick = vs.Candlestick(open_price=100, lowest_price=99, highest_price=110, close_price=105)

# print(f'is shooting star? {candlestick.is_shooting_star()}')


def test_is_shooting_star():
    prova = lib.Candlestick(open_price=100, lowest_price=99, highest_price=110, close_price=105)
    assert prova.is_shooting_star() == False