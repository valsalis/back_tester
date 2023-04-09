import library as lib


DATE = '2023-04-11'

def test_is_shooting_star():
    candlestick = lib.Candlestick(open_price=101, lowest_price=100, highest_price=110, close_price=104, date=DATE)
    assert candlestick.is_shooting_star() == False    
        
    candlestick = lib.Candlestick(open_price=101, lowest_price=100, highest_price=110, close_price=103, date=DATE)
    assert candlestick.is_shooting_star() == True
    assert candlestick.is_shooting_star(20) == False
    
    candlestick = lib.Candlestick(open_price=101, lowest_price=100, highest_price=110, close_price=102, date=DATE)
    assert candlestick.is_shooting_star(20) == True
       
    candlestick = lib.Candlestick(open_price=100, lowest_price=100, highest_price=110, close_price=101, date=DATE)
    assert candlestick.is_shooting_star(10) == True
    
    
def test_is_hammer():
    candlestick = lib.Candlestick(open_price=109.5, lowest_price=100, highest_price=110, close_price=105, date=DATE)
    assert candlestick.is_hammer() == False
    
    candlestick = lib.Candlestick(open_price=109.5, lowest_price=100, highest_price=110, close_price=107.5, date=DATE)
    assert candlestick.is_hammer() == True
    assert candlestick.is_hammer(20) == False
    
    candlestick = lib.Candlestick(open_price=109.5, lowest_price=100, highest_price=110, close_price=108.5, date=DATE)
    assert candlestick.is_hammer(20) == True
    
    candlestick = lib.Candlestick(open_price=109.5, lowest_price=100, highest_price=110, close_price=110, date=DATE)
    assert candlestick.is_hammer(10) == True
    