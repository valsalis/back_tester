import datetime as dt


class Candlestick():
    
    # def __init__(self, open_price: float, lowest_price: float, highest_price: float, close_price: float, date: type(datetime.date())):
    def __init__(self, open_price: float, lowest_price: float, highest_price: float, close_price: float, date: str):
        self.open_price = open_price
        self.lowest_price = lowest_price
        self.highest_price = highest_price
        self.close_price = close_price
        self.date = dt.datetime.strptime(date,'%Y-%m-%d').date()
        
    def is_hammer(self, percent: int = 30) -> bool:
        if self.close_price_is_within_x_percent_of_the_highest_price(percent) and self.open_price_is_within_x_percent_of_the_highest_price(percent):
            return True
        return False
    
    def is_shooting_star(self, percent: int = 30) -> bool:
        if self.close_price_is_within_x_percent_of_the_lowest_price(percent) and self.open_price_is_within_x_percent_of_the_lowest_price(percent):
            return True
        return False
    
    def close_price_is_within_x_percent_of_the_lowest_price(self, percent: int) -> bool:
        return (self.close_price - self.lowest_price) / (self.highest_price - self.lowest_price) <= (percent * 0.01)
    
    def open_price_is_within_x_percent_of_the_lowest_price(self, percent: int) -> bool:
        return (self.open_price - self.lowest_price) / (self.highest_price - self.lowest_price) <= (percent * 0.01)

    def close_price_is_within_x_percent_of_the_highest_price(self, percent: int) -> bool:
        return (self.highest_price - self.close_price) / (self.highest_price - self.lowest_price) <= (percent * 0.01)
    
    def open_price_is_within_x_percent_of_the_highest_price(self, percent: int) -> bool:
        return (self.highest_price - self.open_price) / (self.highest_price - self.lowest_price) <= (percent * 0.01)


# def moving_average_calculation(dataframe, period_as_number_of_days):
#     dataframe[f'simple_moving_average_{period_as_number_of_days}'] = dataframe.Close.rolling(period_as_number_of_days).mean()

