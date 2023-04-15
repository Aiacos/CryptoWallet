import web3
from eth_account._utils.signing import extract_chain_id, to_standard_v
from eth_account._utils.legacy_transactions import ALLOWED_TRANSACTION_KEYS
from eth_account._utils.legacy_transactions import serializable_unsigned_transaction_from_dict


infura_endpoint = 'https://mainnet.infura.io/v3/972b4b8a084b434bba97948637e946be'
transaction = 0xb1a15807babffdcf12c5550ef0a9364b47791d95396e1db382c94eb0bd9123ae


w3 = web3.Web3(web3.HTTPProvider(infura_endpoint))
tx = w3.eth.getTransaction(transaction)
tx.hash



s = w3.eth.account._keys.Signature(vrs=(
    to_standard_v(extract_chain_id(tx.v)[1]),
    w3.toInt(tx.r),
    w3.toInt(tx.s)
))

print("signature: ", s)


tt = {k:tx[k] for k in ALLOWED_TRANSACTION_KEYS - {'chainId', 'data'}}
tt['data']=tx.input
tt['chainId']=extract_chain_id(tx.v)[0]

print("Transaction: ", tt)


ut = serializable_unsigned_transaction_from_dict(tt)

#print("Hash:: ", ut.hash())
print("Public kye: ", s.recover_public_key_from_msg_hash(ut.hash()))

check_address = s.recover_public_key_from_msg_hash(ut.hash()).to_checksum_address()
print('Check Address: ', check_address)


