import sys
import logging
from crypto_tax.wallet import APP_WALLETS, LOGGER

from crypto_tax.kraken import process_file

if __name__ == '__main__':
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.addHandler(logging.StreamHandler())
    process_file(sys.argv[1])
    for (currency, wallet) in APP_WALLETS.items():
        print("%f %r" % (wallet.balance, currency))
