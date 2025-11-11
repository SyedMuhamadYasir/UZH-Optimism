from web3 import Web3
from eth_account import Account
import json
import time


L2_RPC = "http://130.60.144.77:9545" # do not change
w3_l2 = Web3(Web3.HTTPProvider(L2_RPC))
# Try primary token first, then a few common alternatives
opt_ether_token ="0xDeadDeAddeAddEAddeadDEaDDEAdDeaDDeAD0000"
opt_ether_token_addr = Web3.to_checksum_address(opt_ether_token)
# L2StandardBridge
BRIDGE_ADDR = Web3.to_checksum_address("0x4200000000000000000000000000000000000010")
#proxy abi
BRIDGE_ABI=json.loads(open("opt_2_eth_bridge_abi.json").read())
bridge = w3_l2.eth.contract(address=BRIDGE_ADDR, abi=BRIDGE_ABI)


#user settings
private_key= 'xxxxxx' # replace with your private key
SENDER = Account.from_key(private_key).address
# set how much to withdraw
amount_wei   = w3_l2.to_wei("0.1", "ether")  # Withdraw 0.1 UZH_OP
min_gas_l2   = 200_000 #you can keep it as is
extra_data   = b""  #you can keep it as is
print(f"Sender: {SENDER}")
balance = w3_l2.eth.get_balance(SENDER)
print(f"L2 ETH balance: {w3_l2.from_wei(balance, 'ether')} ETH ({balance} wei)")

#build transaction
nonce = w3_l2.eth.get_transaction_count(SENDER, "pending")
tx = bridge.functions.withdraw(opt_ether_token, amount_wei, min_gas_l2, extra_data).build_transaction({
    "from": SENDER,
    "value": amount_wei,
    "nonce": nonce,
    "chainId": 70,                      
})
#estimate gas
gas_est = w3_l2.eth.estimate_gas(tx)
base_fee = w3_l2.eth.get_block("latest")["baseFeePerGas"]
priority = w3_l2.to_wei("1.5", "gwei")
tx.update({
    "gas": int(gas_est * 1.2),
    "maxFeePerGas": int(base_fee * 2 + priority),
    "maxPriorityFeePerGas": priority,
})
#sign transaction
signed = w3_l2.eth.account.sign_transaction(tx, private_key)
#send transaction
tx_hash = w3_l2.eth.send_raw_transaction(signed.raw_transaction)
#wait for transaction receipt
print("L2 withdraw tx hash:", w3_l2.to_hex(tx_hash))
rcpt = w3_l2.eth.wait_for_transaction_receipt(tx_hash)
print("L2 status is " + str(rcpt.status)) #' 1 for success' | '0 for reverted'
#print the current time
print("Current time is " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ", please record this time, you may need 20-30 minutes to finalize the withdrawal on L1")