# !pip install yfinance  # had to run this line to install yfinance
import library as lib
import yfinance as yf
# import matplotlib.pyplot as plt
import datetime
import plotly.graph_objects as go

import plotly.io as pio
pio.renderers.default = 'svg'
# pio.renderers.default = 'browser'

#%%    

class Trade():

    def __init__(self, ticker, buy_sell, open_date, open_price):
        self.ticker = ticker
        self.buy_sell = 'BUY'
        self.open_date = open_date
        self.open_price = open_price
        self.stop_loss = 0
        self.take_profit = 0
        self.close_date = 0
        self.close_price = 0


class Strategy():
    def __init__(self, ticker, number_of_days):
        self.ticker = ticker
        self.days = []
        self.number_of_days = number_of_days
        
    def update(self, candlestick):
        if len(self.days) < self.number_of_days:
            self.days.append(candlestick)
        else:
            del self.days[0]
            self.days.append(candlestick)
            
            if self.days[-3].is_hammer(): 
                if self.price_excursion_of_these_two_days_is_comparable_in_percent(self.days[-3], self.days[-4], 50):
                    # print(f'hammer comparable, ticker = {self.ticker}, date = {self.days[-3]}')
                    if self.is_local_minimum_of_the_past_x_days(self.number_of_days - 3):
                        if self.days[-4].highest_price > self.days[-3].highest_price:
                            if self.days[-2].lowest_price > min(self.days[-3].open_price, self.days[-3].close_price):
                                if self.days[-1].highest_price > self.days[-2].highest_price:
                                    # print(f"ticker: {self.ticker}, date: {candlestick.date}, BUY")
                                    new_trade = Trade(self.ticker, 'BUY', candlestick.date, self.days[-2].highest_price)
                                    trades.append(new_trade)
    
    def price_excursion_of_these_two_days_is_comparable_in_percent(self, day1, day2, percent):
        max_price_excursion_day1 = day1.highest_price - day1.lowest_price
        max_price_excursion_day2 = day2.highest_price - day2.lowest_price
        max_price_excursion = max(max_price_excursion_day1, max_price_excursion_day2)
        if max_price_excursion_day1 / max_price_excursion * 100 > percent and max_price_excursion_day2 / max_price_excursion * 100 > percent:
            return True
        return False
    
    def is_local_minimum_of_the_past_x_days(self, number_of_days):
        reference_minimum = self.days[-3].lowest_price
        for day_idx in range(number_of_days):
            if self.days[-3 - day_idx].lowest_price < reference_minimum:
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
                candlestick = lib.Candlestick(row['Open'], row['Low'], row['High'], row['Close'], str(index.date()))
                strategy.update(candlestick)
                # date = str(index.date())
                # print(type(date))
                # print(date)
                # print(row)
                
        # for index, row in self.data.iterrows():
        #     for ticker in self.tickers:
        #         candlestick = Candlestick(row['Open'][ticker], row['Low'][ticker], row['High'][ticker], row['Close'][ticker])
        #     print(row)
        #     # print(row['Adj Close'])
        #     print(index.date())
        

        
        
#%%
# stock_tickers = ['AAPL','MSFT','TSLA','MMM','MSTR']
# stock_tickers = ['MSTR','SPY','GOOGL','NFLX','AMZN','NVDA','META']
stock_tickers = ['MSTR','SPY']
data = yf.download(stock_tickers, group_by="Ticker", start='2020-01-01')

trades = []

# data2 = {}
# index_list = []
# for index, row in data.iterrows():
#     print(row)
#     # print(row['Adj Close'])
#     print(index.date())
#     index_list.append(index.date())
             
back_tester = BackTester(1000, data)
back_tester.run()

close_price_above_open_price = True  # for debug of rectangle plot
for trade in trades:
    trade.close_date = trade.open_date + datetime.timedelta(days=10)  # for debug of rectangle plot
    if close_price_above_open_price:  # for debug of rectangle plot
        trade.close_price = trade.open_price * 1.1  # for debug of rectangle plot
        close_price_above_open_price = False  # for debug of rectangle plot
    else:  # for debug of rectangle plot
        trade.close_price = trade.open_price * 0.9  # for debug of rectangle plot
        close_price_above_open_price = False  # for debug of rectangle plot
    print(f'ticker: {trade.ticker}, date: {trade.open_date}, {trade.buy_sell}')
    plot_start_date = trade.open_date - datetime.timedelta(days=50)
    print(plot_start_date)
    plot_end_date = trade.open_date + datetime.timedelta(days=50)
    data = yf.download(trade.ticker, start=plot_start_date, end=plot_end_date)
    
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                     open=data['Open'],
                                     high=data['High'],
                                     low=data['Low'],
                                     close=data['Close'])])
    
    fig.update_layout(xaxis_rangeslider_visible=False)
    
    rectangle_color = 'Green'
    if trade.buy_sell == 'BUY':
        if trade.close_price >= trade.open_price:
            rectangle_color = 'Green'
        else:
            rectangle_color = 'Red'
    else:  # trade.buy_sell == 'SELL':
        if trade.close_price <= trade.open_price:
            rectangle_color = 'Green'
        else:
            rectangle_color = 'Red'
    fig.add_shape(type='rect', x0=trade.open_date, y0=trade.open_price, x1=trade.close_date, y1=trade.close_price, 
                  line=dict(color='RoyalBlue'), fillcolor=rectangle_color, opacity=0.2)
    
    #  boiler plate to add percentage change value on chart
    fig.add_trace(go.Scatter(
    x=[trade.open_date + (trade.close_date - trade.open_date) / 2],
    y=[trade.close_price],
    text=[f'{round((trade.close_price - trade.open_price) / trade.open_price * 100, 2)} %'],
    mode="text",))
    
    fig.update_layout(showlegend=False)

    fig.show()


