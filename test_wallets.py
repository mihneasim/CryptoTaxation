from datetime import datetime as dt
import pytest

from wallets import Trade, Wallet


class TestWallets(object):

    def test_trade_init(self):
        trade = Trade('XBT', 20.02, 'EUR', 13000.01, dt(2017, 11, 1, 15, 3, 3))
        assert trade.trading_currency == 'EUR'
        assert trade.amount == pytest.approx(20.02)

    def test_wallet_init_and_deposit(self):
        eur_wallet = Wallet('EUR')
        eur_wallet.deposit(10000)
        assert eur_wallet.get_trades_count() == 1
        trade = next(eur_wallet.trades_gen())
        assert trade.amount == 10000

    def test_wallet_buy(self):
        btc_wallet = Wallet('BTC')
        eur_wallet = Wallet('EUR')
        eur_wallet.deposit(10000)
        btc_wallet.buy(0.05, eur_wallet, 10000, dt(2017, 12, 3, 12, 30))
        btc_wallet.buy(0.05, eur_wallet, 12000, dt(2017, 12, 3, 16, 20))
        assert btc_wallet.balance == pytest.approx(0.1)
        assert eur_wallet.balance == pytest.approx(8900)

    def test_wallet_sell(self):
        btc_wallet = Wallet('BTC')
        eur_wallet = Wallet('EUR')
        eur_wallet.deposit(10000)
        btc_wallet.buy(0.05, eur_wallet, 10000, dt(2017, 12, 3, 12, 30))
        btc_wallet.buy(0.05, eur_wallet, 12000, dt(2017, 12, 3, 16, 20))
        btc_wallet.sell(0.08, eur_wallet, 13000, dt(2017, 12, 3, 16, 20))
        assert btc_wallet.balance == pytest.approx(0.02)
        assert eur_wallet.balance == pytest.approx(9940)

    def test_wallet_spend_more_than_you_got(self):
        btc_wallet = Wallet('BTC')
        eur_wallet = Wallet('EUR')
        eur_wallet.deposit(1000)
        eur_wallet.deposit(1000)
        btc_wallet.buy(1, eur_wallet, 10000, dt(2017, 12, 3, 12, 30))
        assert eur_wallet.balance == pytest.approx(-8000)
        assert eur_wallet.get_trades_count() == 1
