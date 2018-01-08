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

def pair_to_wallets(pair):
    dest, src = pair[:int(len(pair) / 2)], pair[int(len(pair) / 2):]
    return Wallet.getInstance(EXCHANGE_SYMBOLS[src]), Wallet.getInstance(EXCHANGE_SYMBOLS[dest])
