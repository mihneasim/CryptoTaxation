from .const import Symbols
from .cryptocompare import CryptoCompare

def get_rate(src, dest, date):
    if not isinstance(src, Symbols):
        raise TypeError("Expected enum type Symbols, got %r type %s" % (src, type(src)))
    if not isinstance(dest, Symbols):
        raise TypeError("Expected enum type Symbols, got %r type %s" % (dest, type(dest)))
    ts = date.timestamp()
    return get_cached_rate(src, dest, ts) or get_server_rate(src, dest, ts)

def get_cached_rate(src, dest, timestamp):
    """ Attempt to get the rate from local db, return None if not found """
    # NotImplemented
    return None

def cache_the_rate(src, dest, timestamp, value):
    # NotImplemented
    pass

def get_server_rate(src, dest, timestamp):
    """ API call to get the rate """
    rate = CryptoCompare.get_rate(src, dest, timestamp)
    cache_the_rate(src, dest, timestamp, rate)
    return rate
