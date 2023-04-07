# !pip install yfinance  # had to run this line to install yfinance
import library as lib
import yfinance as yf
import matplotlib.pyplot as plt

#%%    

class Trade():

    def __init__(self, ticker, buy_sell, open_date, open_price):
        self.ticker = ticker
        self.buy_sell = 'BUY'
        self.open_date = open_date
        self.open_price = open_price
        self.stop_loss
        self.take_profit
        self.close_date
        self.close_price


class Strategy():
    def __init__(self, ticker, number_of_days):
        self.ticker = ticker
        self.days = []
        self.number_of_days = number_of_days
        
    def update(self, date, candlestick):
        if len(self.days) < self.number_of_days:
            self.days.append([date, candlestick])
        else:
            del self.days[0]
            self.days.append([date, candlestick])
            
            if self.days[-3][1].is_hammer(): 
                if self.price_excursion_of_these_two_days_is_comparable_in_percent(self.days[-3][1], self.days[-4][1], 50):
                    # print(f'hammer comparable, ticker = {self.ticker}, date = {self.days[-3][0]}')
                    if self.is_local_minimum_in_the_past_x_days(self.number_of_days - 3):
                        if self.days[-4][1].highest_price > self.days[-3][1].highest_price:
                            if self.days[-2][1].lowest_price > min(self.days[-3][1].open_price, self.days[-3][1].close_price):
                                if self.days[-1][1].highest_price > self.days[-2][1].highest_price:
                                    print(f"ticker: {self.ticker}, date: {date}, BUY")
    
    def price_excursion_of_these_two_days_is_comparable_in_percent(self, day1, day2, percent):
        max_price_excursion_day1 = day1.highest_price - day1.lowest_price
        max_price_excursion_day2 = day2.highest_price - day2.lowest_price
        max_price_excursion = max(max_price_excursion_day1, max_price_excursion_day2)
        if max_price_excursion_day1 / max_price_excursion * 100 > percent and max_price_excursion_day2 / max_price_excursion * 100 > percent:
            return True
        return False
    
    def is_local_minimum_in_the_past_x_days(self, number_of_days):
        reference_minimum = self.days[-3][1].lowest_price
        for day_idx in range(number_of_days):
            if self.days[-3 - day_idx][1].lowest_price < reference_minimum:
                return False
        return True
            
        
class BackTester():
    
    def __init__(self, initial_cash, data):
        self.cash = initial_cash
        self.deposited_cash = initial_cash
        self.data = data
        self.tickers = self.exctract_tickers()
        self.trades = []
        
    def exctract_tickers(self):
        tickers = []
        for pair in list(self.data.columns):
            ticker = pair[0]
            if ticker not in tickers:
                tickers.append(ticker)
        return tickers
    
    def add_trade(self, ticker, open_date, open_price):
        new_trade = Trade(ticker, open_date, open_price)
        self.trades.append(new_trade)
        
    def run(self):
        for ticker in self.tickers:
            strategy = Strategy(ticker, 10)
            for index, row in self.data[ticker].iterrows():
                date = index.date()
                # print(type(index.date()))
                # print(row)
                candlestick = lib.Candlestick(row['Open'], row['Low'], row['High'], row['Close'])
                strategy.update(date, candlestick)
                
        # for index, row in self.data.iterrows():
        #     for ticker in self.tickers:
        #         candlestick = Candlestick(row['Open'][ticker], row['Low'][ticker], row['High'][ticker], row['Close'][ticker])
        #     print(row)
        #     # print(row['Adj Close'])
        #     print(index.date())
        

        
        
#%%
stock_tickers = ['AAPL','MSFT','TSLA','MMM','MSTR']
stock_tickers = ['MSTR','SPY','GOOGL','NFLX','AMZN','NVDA','META']
data = yf.download(stock_tickers, group_by="Ticker", start='2020-01-01')

# data2 = {}
# index_list = []
# for index, row in data.iterrows():
#     print(row)
#     # print(row['Adj Close'])
#     print(index.date())
#     index_list.append(index.date())
             
back_tester = BackTester(1000, data)
back_tester.run()



