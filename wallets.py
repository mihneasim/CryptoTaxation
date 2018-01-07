from datetime import datetime as dt

class Trade(object):
    """
    Represents aquisition done through a trade, an amount of currency
    acquired for the same price

    """

    def __init__(self, currency, amount, trading_currency, rate, date):
        self.amount = amount
        self.date = date
        self.currency = currency
        self.trading_currency = trading_currency
        self.rate = rate

class Wallet(object):
    """
    Collection of sequences representing
    the trades for the same currency

    """

    def __init__(self, currency):
        self.currency = currency
        self.trades = []

    def deposit(self, amount, date=None):
        date = date or dt.now()
        self.trades.append(Trade(self.currency, amount, self.currency, 1, date))

    def withdraw(self, amount, date=None):
        date = date or dt.now()
        self.trades[-1].amount -= amount
        # TODO implement properly

    def buy(self, amount, trading_wallet, rate, date):
        trade = Trade(self.currency, amount, trading_wallet.get_currency(), rate, date)
        trading_wallet.withdraw(amount * rate, date)
        self.trades.append(trade)

    def trades_gen(self):
        for trade in self.trades:
            yield trade

    def get_trades_count(self):
        return len(self.trades)

    def get_currency(self):
        return self.currency

    @property
    def balance(self):
        summ = 0.0
        for trade in self.trades_gen():
            summ += trade.amount
        return summ
