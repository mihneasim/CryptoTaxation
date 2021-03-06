import logging
from datetime import datetime as dt

from .const import Symbols
from .rates import get_rate

LOGGER = logging.getLogger(__name__)

APP_WALLETS = {} # Singleton accross app instance
PROFITS = {} # per year

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

    @staticmethod
    def getInstance(currency):
        """ Get or create singleton wallet """
        if not isinstance(currency, Symbols):
            raise TypeError("Expected enum type Symbols, got %r type %s" % (currency, type(currency)))
        if currency in APP_WALLETS:
            return APP_WALLETS[currency]
        else:
            wallet = Wallet(currency)
            APP_WALLETS[currency] = wallet
            return wallet

    @staticmethod
    def getAll():
        for key in APP_WALLETS:
            yield APP_WALLETS[key]

    def deposit(self, amount, date=None):
        date = date or dt.now()
        self.trades.append(Trade(self.currency, amount, self.currency, 1, date))

    def withdraw(self, amount, date=None, is_tax=False):
        """
        When trading, e.g. selling one for another, the withdraw
        of the wallet we are selling from starts with oldest acquisition.
        This is the FIFO rule of taxing: when selling something, you have to
        use your earliest acquisition price to compute profit.

        It's like the coin is actually physical and you start with the
        oldest ones in the stack. Profit is your sellprice vs. their initial
        price you bought them for.

        When withdrawing EUR[1], profit is 0 (we can say we buy/sell euro
        with a forever flat rate of 1 to 1).

        Fees payed to the exchanged are not counted as a sell.

        [1] Actually, let's make this configurable. Maybe you will be
        interested in taxation vs USD or a local currency.
        """
        date = date or dt.now()

        def _log_profit(amount, then):
            """ Profit for selling amount bought `then` """
            if self.currency == Symbols.EUR or is_tax:
                return
            rate = 0.0
            sell_rate = 0.0
            try:
                rate = get_rate(self.currency, Symbols.EUR, then)
            except:
                LOGGER.error("Error getting rate %s %s %s", self.currency, Symbols.EUR, then)

            try:
                sell_rate = get_rate(self.currency, Symbols.EUR, date)
            except:
                LOGGER.error("Error getting rate %s %s %s", self.currency, Symbols.EUR, date)

            profit = (sell_rate - rate) * amount
            year = date.year
            PROFITS[year] = PROFITS.setdefault(year, 0.0) + profit

            LOGGER.debug("{}: Selling {:f} {} bought on {} (rate {:.2f} EUR) for rate: {:.2f} EUR, profit: {:.2f} EUR".format(
                    date.strftime("%d-%m-%Y"), amount, self.currency.value, then.strftime("%d-%m-%Y"), rate, sell_rate, profit))

        while amount > 0:
            if len(self.trades):
                if (self.trades[0].amount > amount):
                    self.trades[0].amount -= amount
                    _log_profit(amount, self.trades[0].date)
                    amount = 0
                else:
                    amount -= self.trades[0].amount
                    _log_profit(self.trades[0].amount, self.trades[0].date)
                    self.trades.pop(0)
            else:
                self.deposit(-amount, date)
                amount = 0

    def withdraw_for_fee(self, amount, date=None):
        return self.withdraw(amount, date, True)

    def buy(self, amount, trading_wallet, rate, date, fee=0.0):
        """ Fee is in trading_wallet currency, deducted on top """
        trade = Trade(self.currency, amount, trading_wallet.get_currency(), rate, date)
        trading_wallet.withdraw_for_fee(fee, date)
        trading_wallet.withdraw(amount * rate, date)
        self.trades.append(trade)

    def sell(self, amount, trading_wallet, rate, date, fee=0.0):
        trading_wallet.withdraw_for_fee(fee, date)
        return trading_wallet.buy(amount * rate, self, 1 / rate, date, 0.00)

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
