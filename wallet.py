from eth_account import Account
from web3 import Web3, HTTPProvider
from secrets import token_bytes
from coincurve import PublicKey
from sha3 import keccak_256
import re


infura_endpoint = 'https://mainnet.infura.io/v3/972b4b8a084b434bba97948637e946be'
alchemy_endpoint = 'https://eth-mainnet.g.alchemy.com/v2/csmoa4n5DwucntIE0vZtb5NtOiJLC_ez'

INFURA_LIMIT = 100000
ALCHEMY_LIMIT = int(300000000000 / 19)




def generateAccount(mode='mnemonic'):
    if mode == 'fast':
        p_key = keccak_256(token_bytes(32)).digest()
        public_key = PublicKey.from_valid_secret(p_key).format(compressed=False)[1:]
        addr = keccak_256(public_key).digest()[-20:]

        private_key = p_key.hex()
        address = '0x' + addr.hex()

    elif mode == 'mnemonic':
        Account.enable_unaudited_hdwallet_features()
        acct, mnemonic = Account.create_with_mnemonic()
        address = acct.address#.lower()

        private_key = acct.key.hex()

        return private_key, address, mnemonic

    else:
        acct = Account.create()
        address = acct.address#.lower()

        private_key = acct.key.hex()

    return private_key, address, None

def generatePrivateKey():
    acct = Account.create()
    #address = acct.address#.lower()

    private_key = acct.key.hex()

    return str(private_key)

def generatePublicKeyFromPrivate(private_key):
    acct = Account.from_key(private_key)
    address = acct.address#.lower()

    return address

def checkBalanceETH(connection, address, coin='ether'):
    #safe_address = connection.to_checksum_address(address)
    #print("Safe: " + str(safe_address))
    wei_balance = connection.eth.get_balance(address)

    try:
        balance = connection.fromWei(wei_balance, coin)
    except:
        try:
            balance = connection.from_wei(wei_balance, coin)
        except:
            return None

    return balance

def check_vanity(pattern, public_key, regex=False):
    if regex:
        if pattern in public_key:
            return True
        else:
            return False
    else:
        if pattern == public_key:
            return True
        else:
            return False

    return None