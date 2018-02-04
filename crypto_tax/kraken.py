import csv
from datetime import datetime as dt

from .const import Symbols
from .wallet import Wallet

EXCHANGE_SYMBOLS = {
        'XBT': Symbols.XBT,
        'XXBT': Symbols.XBT,
        'ZEUR': Symbols.EUR,
        'EUR': Symbols.EUR,
        'XXLM': Symbols.XLM,
        'BCH': Symbols.BCH,
        'XETH': Symbols.ETH,
        'XXRP': Symbols.XRP
        }

class TradesLine(object):
    """
    A representation of a line inside the trades CSV file
    """

    def __init__(self, src, dest, rate, amount, date, sell_or_buy, fee):
        self.src = src
        self.dest = dest
        self.rate = rate
        self.amount = amount
        self.date = date
        self.type = sell_or_buy
        self.fee = fee

def pair_to_wallets(pair):
    dest, src = pair[:int(len(pair) / 2)], pair[int(len(pair) / 2):]
    return Wallet.getInstance(EXCHANGE_SYMBOLS[src]), Wallet.getInstance(EXCHANGE_SYMBOLS[dest])

def parse_line(line):
    """ Parses a CSV sheet line into a TradesLine object """
    date = dt.strptime(line[3], '%Y-%m-%d %H:%M:%S.%f')
    pair = line[2]
    rate = float(line[6])
    amount = float(line[9])
    sell_or_buy = line[4]
    src, dest = pair_to_wallets(pair)
    fee = float(line[8])

    return TradesLine(src, dest, rate, amount, date, sell_or_buy, fee)

def parse_file_gen(csvfile):
    """ Returns one trade at a time """
    fpointer = open(csvfile, 'rt')
    reader = csv.reader(fpointer)
    next(reader)
    for line in reader:
        yield parse_line(line)

def process_file(csv_file):
   """ The main entry point - the financial execution of the sheet """
   trades_gen = parse_file_gen(csv_file)
   for trade in trades_gen:
      if trade.type == 'sell':
       trade.dest.sell(trade.amount, trade.src, trade.rate, trade.date, trade.fee)
      else:
       trade.dest.buy(trade.amount, trade.src, trade.rate, trade.date, trade.fee)
