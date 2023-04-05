import library as lib


def test_is_shooting_star():
    candlestick = lib.Candlestick(open_price=101, lowest_price=100, highest_price=110, close_price=104)
    assert candlestick.is_shooting_star() == False    
        
    candlestick = lib.Candlestick(open_price=101, lowest_price=100, highest_price=110, close_price=103)
    assert candlestick.is_shooting_star() == True
    assert candlestick.is_shooting_star(20) == False
    
    candlestick = lib.Candlestick(open_price=101, lowest_price=100, highest_price=110, close_price=102)
    assert candlestick.is_shooting_star(20) == True
       
    candlestick = lib.Candlestick(open_price=100, lowest_price=100, highest_price=110, close_price=101)
    assert candlestick.is_shooting_star(10) == True
    
    
def test_is_hammer():
    candlestick = lib.Candlestick(open_price=109.5, lowest_price=100, highest_price=110, close_price=105)
    assert candlestick.is_hammer() == False
    
    candlestick = lib.Candlestick(open_price=109.5, lowest_price=100, highest_price=110, close_price=107.5)
    assert candlestick.is_hammer() == True
    assert candlestick.is_hammer(20) == False
    
    candlestick = lib.Candlestick(open_price=109.5, lowest_price=100, highest_price=110, close_price=108.5)
    assert candlestick.is_hammer(20) == True
    
    candlestick = lib.Candlestick(open_price=109.5, lowest_price=100, highest_price=110, close_price=110)
    assert candlestick.is_hammer(10) == True
    