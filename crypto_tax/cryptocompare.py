import requests

from .const import Symbols

# Not exactly an exchange, but .. consistency
EXCHANGE_SYMBOLS = {
    'BTC': Symbols.XBT,
    'EUR': Symbols.EUR,
    'XLM': Symbols.XLM,
    'BCH': Symbols.BCH,
    'ETH': Symbols.ETH
}

# we actually need from Symbol to str
EXCHANGE_SYMBOLS_REVERSE = {}
for (key, val) in EXCHANGE_SYMBOLS.items():
    EXCHANGE_SYMBOLS_REVERSE[val] = key

class CryptoCompare(object):

    REQUEST = 'https://min-api.cryptocompare.com/data/pricehistorical?fsym={0}&tsyms={1}&ts={2}'

    @staticmethod
    def get_rate(src, dest, ts):
        """ API request """
        s_src = EXCHANGE_SYMBOLS_REVERSE[src]
        s_dest = EXCHANGE_SYMBOLS_REVERSE[dest]
        timestamp = int(ts)
        r = requests.get(CryptoCompare.REQUEST.format(s_src, s_dest, int(ts)))
        if r.status_code == 200:
            return float(r.json()[s_src][s_dest])
        else:
            raise SystemError('API response in error %r' % r.status_code)
