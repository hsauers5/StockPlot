import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import requests


class StockPlot:
    def __init__(self, ticker):
        self.ticker = ticker

    # plots a graph of our data over time
    def plot(self):
        dates = ['20160101', '20170101', '20180101', '20190101', '20200101']
        x_pos = np.arange(len(dates))

        # let's use some fancy list comprehension
        # it's fun and makes for cleaner code.
        financials = [self.get_financials(d) for d in dates]
        current_ratios = [self.get_current_ratio(f) for f in financials]
        ev_to_saless = [self.get_ev_to_sales(f) for f in financials]
        ev_to_ebits = [self.get_ev_to_ebit(f) for f in financials]

        # plot metrics

        # window 1
        plt.figure(1)
        plt.bar(x_pos, current_ratios, align='center', alpha=0.5)
        plt.xticks(x_pos, dates)

        plt.ylabel('Current Ratio')
        plt.xlabel('Date')

        # window 2
        plt.figure(2)
        plt.bar(x_pos, ev_to_saless, align='center', alpha=0.5)
        plt.xticks(x_pos, dates)

        plt.ylabel('EV/Sales')
        plt.xlabel('Date')

        # window 3
        plt.figure(3)
        plt.bar(x_pos, ev_to_ebits, align='center', alpha=0.5)
        plt.xticks(x_pos, dates)

        plt.ylabel('EV/EBIT')
        plt.xlabel('Date')

        # plot graphs
        plt.show()

    # returns a Dictionary of point-in-time financial data
    def get_financials(self, date='20200101'):
        API_KEY = 'YOUR_KEY_HERE'

        # use an f-string to build your query
        query_url = f'https://api.tenquant.io/historical?key={API_KEY}&date={date}&ticker={self.ticker}'
        financials = requests.get(query_url).json()
        return financials

    # runs calculations and returns the current ratio: current assets - current liabilities
    def get_current_ratio(self, financials):
        current_assets = financials['currentassets']
        current_liabilities = financials['currentliabilities']
        return current_assets / current_liabilities

    # returns enterprise value to sales
    def get_ev_to_sales(self, financials):
        sales = financials['revenues']
        duration = financials['duration']  # figures are from this many quarters
        cash = financials['currentassets']  # substitute current assets for cash
        debt = financials['liabilities']
        market_cap = financials['marketcap']

        annualized_sales = sales / (duration / 4)

        ev = market_cap + debt - cash
        ev_to_sales = ev / annualized_sales
        return ev_to_sales

    # returns ev to ebit, excluding unusual items
    def get_ev_to_ebit(self, financials):
        net_income = financials['netincomeavailabletocommonstockholdersbasic']
        interest = financials['interestanddebtexpense']
        taxes = financials['incometaxexpensebenefit']
        ebit = net_income + interest + taxes*(-1)  # taxes are recorded as an absolute figure: income/(loss)

        duration = financials['duration']  # figures are from this many quarters
        cash = financials['currentassets']  # substitute current assets for cash
        debt = financials['liabilities']
        market_cap = financials['marketcap']

        annualized_sales = ebit / (duration / 4)

        ev = market_cap + debt - cash
        ev_to_ebit = ev / annualized_sales

        return ev_to_ebit


if __name__ == '__main__':
    sp = StockPlot('AAPL')
    sp.plot()
