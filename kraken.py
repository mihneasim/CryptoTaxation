import csv
from datetime import datetime as dt

from const import Symbols
from wallet import Wallet

EXCHANGE_SYMBOLS = {
        'XBT': Symbols.XBT,
        'XXBT': Symbols.XBT,
        'ZEUR': Symbols.EUR,
        'XXLM': Symbols.XLM,
        'BCH': Symbols.BCH,
        'XETH': Symbols.ETH
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

def _parse_line(line):
    """ Initial text to data parsing. To be used by actual parse_line """
    date = dt.strptime(line[3], '%Y-%m-%d %H:%M:%S.%f')
    return {
            'pair': line[2],
            'rate': float(line[6]),
            'date': date,
            'amount': float(line[9])
            }

def parse_line(line):
    data = _parse_line(line)
    src, dest = pair_to_wallets(data['pair'])
    return TradesLine(src, dest, data['rate'], data['amount'], data['date'])

def parse_file_gen(csvfile):
    """ One trade at a time """
    fpointer = open(csvfile, 'rt')
    reader = csv.reader(fpointer)
    next(reader)
    for line in reader:
        yield parse_line(line)
