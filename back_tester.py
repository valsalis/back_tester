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
    def __init__(self, ticker):
        self.ticker = ticker
        self.day1 = []
        self.day2 = []
        self.day3 = []
        self.day4 = []
        self.counter = 0
        
    def update(self, date, candlestick):
        self.day1 = self.day2
        self.day2 = self.day3
        self.day3 = self.day4
        self.day4 = [date, candlestick]
        
        if self.counter < 4:
            self.counter += 1
        if self.counter >= 4:
            if self.day2[1].is_hammer(): 
                print(f'hammer, ticker = {self.ticker}, date = {self.day2[0]}')
                if self.day1[1].highest_price > self.day2[1].highest_price:
                    if self.day3[1].lowest_price > min(self.day2[1].open_price, self.day2[1].close_price):
                        if self.day4[1].highest_price > self.day3[1].highest_price:
                            print(f"ticker: {self.ticker}, date: {date}, BUY")
    
        
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
            strategy = Strategy(ticker)
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
stock_tickers = ['AAPL','MSFT','TSLA','MMM']
data = yf.download(stock_tickers, group_by="Ticker", start='2021-01-01')

# data2 = {}
# index_list = []
# for index, row in data.iterrows():
#     print(row)
#     # print(row['Adj Close'])
#     print(index.date())
#     index_list.append(index.date())
             
back_tester = BackTester(1000, data)
back_tester.run()



