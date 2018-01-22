import pytest
import requests_mock

from crypto_tax.const import Symbols
from crypto_tax.cryptocompare import CryptoCompare


@requests_mock.mock()
def test_get_rate(*args):
    req = 'https://min-api.cryptocompare.com/data/pricehistorical?fsym=ETH&tsyms=BTC&ts=1514761200'
    args[0].get(req, text='{"ETH":{"BTC":0.05352}}')
    rate = CryptoCompare.get_rate(Symbols.ETH, Symbols.XBT, 1514761200.0)
    assert rate == pytest.approx(0.05352)

def test_get_rate(*args):
    rate = CryptoCompare.get_rate(Symbols.EUR, Symbols.EUR, 1514761200.0)
    assert rate == pytest.approx(1.0)
