import sys
from crypto_tax.wallet import APP_WALLETS

from crypto_tax.kraken import process_file

if __name__ == '__main__':
    process_file(sys.argv[1])
    for (currency, wallet) in APP_WALLETS.items():
        print("%f %r" % (wallet.balance, currency))
