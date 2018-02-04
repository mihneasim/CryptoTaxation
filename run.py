import sys
import logging
from crypto_tax.wallet import APP_WALLETS, LOGGER, PROFITS

from crypto_tax.kraken import process_file

if __name__ == '__main__':
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.addHandler(logging.StreamHandler())
    process_file(sys.argv[1])
    print('Wallet balances -except direct deposits-')
    for (currency, wallet) in APP_WALLETS.items():
        print("%s %f" % (currency.name, wallet.balance))

    print('Recorded profits, per year')
    for (year, profit) in PROFITS.items():
        print("%r: %f EUR" % (year, profit))
