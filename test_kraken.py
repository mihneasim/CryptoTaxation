from datetime import datetime as dt
import pytest

from const import Symbols
from wallet import Wallet
import kraken

def test_pair_to_wallets():
    src, dest = kraken.pair_to_wallets('XXBTZEUR')
    assert src.currency == Symbols.EUR
    assert dest.currency == Symbols.XBT
    src2, dest2 = kraken.pair_to_wallets('BCHXBT')
    assert src2.currency == Symbols.XBT
    assert dest2.currency == Symbols.BCH
    assert src2 == dest

def test_csv_parsing():
    gen = kraken.parse_file_gen('few-lines.csv')
    trade = next(gen)
    assert trade.src is Wallet.getInstance(Symbols.EUR)
    assert trade.dest is Wallet.getInstance(Symbols.XBT)
    trade = next(gen)
    assert trade.date == dt(2017, 9, 18, 15, 12, 25, 122500)
    assert trade.rate == pytest.approx(0.07219)
    assert trade.amount == pytest.approx(0.69261)
    count = 2
    for trade in gen:
        count += 1
    assert count == 10
    assert trade.amount == pytest.approx(0.04568334)

def test_process_file():
    kraken.process_file('few-lines.csv')
    expected_balances = {
        Symbols.EUR: -4040.237386,
        Symbols.XBT: 0.768813,
        Symbols.ETH: 2.370460,
        Symbols.XLM: 6172.8395,
        Symbols.BCH: 0.04568334
    }
    for wallet in Wallet.getAll():
        assert wallet.balance == pytest.approx(expected_balances[wallet.currency])
