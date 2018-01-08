from const import Symbols
from kraken import pair_to_wallets

def test_pair_to_wallets():
    src, dest = pair_to_wallets('XXBTZEUR')
    assert src.currency == Symbols.EUR
    assert dest.currency == Symbols.XBT
    src2, dest2 = pair_to_wallets('BCHXBT')
    assert src2.currency == Symbols.XBT
    assert dest2.currency == Symbols.BCH
    assert src2 == dest
