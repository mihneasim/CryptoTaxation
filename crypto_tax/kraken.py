import csv
from datetime import datetime as dt

from .const import Symbols
from .wallet import Wallet

EXCHANGE_SYMBOLS = {
        'XBT': Symbols.XBT,
        'XXBT': Symbols.XBT,
        'ZEUR': Symbols.EUR,
        'XXLM': Symbols.XLM,
        'BCH': Symbols.BCH,
        'XETH': Symbols.ETH,
        'XXRP': Symbols.XRP
        }

class TradesLine(object):
    """
    A representation of a line inside the trades CSV file
    """

    def __init__(self, src, dest, rate, amount, date):
        self.src = src
        self.dest = dest
        self.rate = rate
        self.amount = amount
        self.date = date

def pair_to_wallets(pair):
    dest, src = pair[:int(len(pair) / 2)], pair[int(len(pair) / 2):]
    return Wallet.getInstance(EXCHANGE_SYMBOLS[src]), Wallet.getInstance(EXCHANGE_SYMBOLS[dest])


def parse_line(line):
    """ Parses a CSV sheet line into a TradesLine object """
    date = dt.strptime(line[3], '%Y-%m-%d %H:%M:%S.%f')
    pair = line[2]
    rate = float(line[6])
    amount = float(line[9])

    src, dest = pair_to_wallets(pair)
    return TradesLine(src, dest, rate, amount, date)

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
       trade.dest.buy(trade.amount, trade.src, trade.rate, trade.date)
