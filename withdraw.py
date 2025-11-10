from web3 import Web3
from eth_account import Account
import os
import json
from web3.exceptions import ContractLogicError

L2_RPC = "http://130.60.144.77:9545" # do not change
private_key= 'xxxxx' # replace
SENDER = Account.from_key(private_key).address

w3_l2 = Web3(Web3.HTTPProvider(L2_RPC))

# L2StandardBridge
BRIDGE_ADDR = Web3.to_checksum_address("0x4200000000000000000000000000000000000010")
#proxy abi
BRIDGE_ABI=json.loads('[{"inputs":[{"internalType":"addresspayable","name":"_otherBridge","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"l1Token","type":"address"},{"indexed":true,"internalType":"address","name":"l2Token","type":"address"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"bytes","name":"extraData","type":"bytes"}],"name":"DepositFinalized","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"localToken","type":"address"},{"indexed":true,"internalType":"address","name":"remoteToken","type":"address"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"bytes","name":"extraData","type":"bytes"}],"name":"ERC20BridgeFinalized","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"localToken","type":"address"},{"indexed":true,"internalType":"address","name":"remoteToken","type":"address"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"bytes","name":"extraData","type":"bytes"}],"name":"ERC20BridgeInitiated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"bytes","name":"extraData","type":"bytes"}],"name":"ETHBridgeFinalized","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"bytes","name":"extraData","type":"bytes"}],"name":"ETHBridgeInitiated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"l1Token","type":"address"},{"indexed":true,"internalType":"address","name":"l2Token","type":"address"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"bytes","name":"extraData","type":"bytes"}],"name":"WithdrawalInitiated","type":"event"},{"inputs":[],"name":"MESSENGER","outputs":[{"internalType":"contractCrossDomainMessenger","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"OTHER_BRIDGE","outputs":[{"internalType":"contractStandardBridge","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_localToken","type":"address"},{"internalType":"address","name":"_remoteToken","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"uint32","name":"_minGasLimit","type":"uint32"},{"internalType":"bytes","name":"_extraData","type":"bytes"}],"name":"bridgeERC20","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_localToken","type":"address"},{"internalType":"address","name":"_remoteToken","type":"address"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"uint32","name":"_minGasLimit","type":"uint32"},{"internalType":"bytes","name":"_extraData","type":"bytes"}],"name":"bridgeERC20To","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint32","name":"_minGasLimit","type":"uint32"},{"internalType":"bytes","name":"_extraData","type":"bytes"}],"name":"bridgeETH","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint32","name":"_minGasLimit","type":"uint32"},{"internalType":"bytes","name":"_extraData","type":"bytes"}],"name":"bridgeETHTo","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"deposits","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_localToken","type":"address"},{"internalType":"address","name":"_remoteToken","type":"address"},{"internalType":"address","name":"_from","type":"address"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"bytes","name":"_extraData","type":"bytes"}],"name":"finalizeBridgeERC20","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_from","type":"address"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"bytes","name":"_extraData","type":"bytes"}],"name":"finalizeBridgeETH","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_l1Token","type":"address"},{"internalType":"address","name":"_l2Token","type":"address"},{"internalType":"address","name":"_from","type":"address"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"bytes","name":"_extraData","type":"bytes"}],"name":"finalizeDeposit","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"l1TokenBridge","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"messenger","outputs":[{"internalType":"contractCrossDomainMessenger","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_l2Token","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"uint32","name":"_minGasLimit","type":"uint32"},{"internalType":"bytes","name":"_extraData","type":"bytes"}],"name":"withdraw","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_l2Token","type":"address"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"uint32","name":"_minGasLimit","type":"uint32"},{"internalType":"bytes","name":"_extraData","type":"bytes"}],"name":"withdrawTo","outputs":[],"stateMutability":"payable","type":"function"},{"stateMutability":"payable","type":"receive"}]')
bridge = w3_l2.eth.contract(address=BRIDGE_ADDR, abi=BRIDGE_ABI)

# parameters
amount_wei   = w3_l2.to_wei("1.2", "ether")  # Withdraw 1.2 UZH_OP
min_gas_l2   = 200_000
extra_data   = b""           

nonce = w3_l2.eth.get_transaction_count(SENDER, "pending")
L2_ETH_TOKEN = Web3.to_checksum_address(os.getenv("L2_ETH_TOKEN", "0x0000000000000000000000000000000000000000"))

# --- Diagnostics / simulation before sending ---
print(f"Sender: {SENDER}")
balance = w3_l2.eth.get_balance(SENDER)
print(f"L2 ETH balance: {w3_l2.from_wei(balance, 'ether')} ETH ({balance} wei)")

code = w3_l2.eth.get_code(BRIDGE_ADDR)
# print(f"Bridge contract code length: {len(code)} bytes")

# print("Inspecting ABI entries for 'withdraw' and 'withdrawTo':")
try:
    withdraw_abis = [a for a in BRIDGE_ABI if a.get('name') == 'withdraw']
    withdraw_to_abis = [a for a in BRIDGE_ABI if a.get('name') == 'withdrawTo']
    # print(' withdraw ABI entries:', withdraw_abis)
    # print(' withdrawTo ABI entries:', withdraw_to_abis)
except Exception as e:
    print(' Failed to inspect ABI:', e)

# Try to simulate the call (eth_call) to get revert reason if any.
def try_simulate(token_addr):
    try:
        # print(f"Simulating withdraw with token {token_addr} ...")
        res = bridge.functions.withdraw(token_addr, amount_wei, min_gas_l2, extra_data).call({
            'from': SENDER,
            'value': amount_wei,
        })
        # print(' Simulation succeeded, call() returned:', res)
        return True, None
    except ContractLogicError as cle:
        # cle may contain revert reason or empty data
        # print(' ContractLogicError during simulation:', cle)
        # try to extract revert data if available
        try:
            data = cle.args[1]
            # print(' Revert data (hex):', data)
        except Exception:
            pass
        return False, cle
    except Exception as e:
        print(' Other error during simulation:', type(e), e)
        return False, e

# Try primary token first, then a few common alternatives
alt_tokens = ['0x4200000000000000000000000000000000000006', "0xDeadDeAddeAddEAddeadDEaDDEAdDeaDDeAD0000", "0x4200000000000000000000000000000000000001"]
alt_tokens = list(dict.fromkeys([Web3.to_checksum_address(t) for t in alt_tokens if Web3.is_checksum_address(t)]))

sim_ok = False
sim_errors = []
for t in alt_tokens:
    ok, err = try_simulate(t)
    if ok:
        chosen_token = t
        sim_ok = True
        break
    sim_errors.append((t, err))

if not sim_ok:
    print('\nAll simulations failed. Summary:')
    for t, err in sim_errors:
        print(f' - token {t}: {err}')
    print('\nHints:')
    print(' - Ensure the bridge contract you are calling supports ETH withdrawals via this method.')
    print(' - Check whether the bridge expects a specific predeploy L2 ETH token address (not the zero address).')
    print(' - Confirm the sender has sufficient ETH balance on L2 to cover amount + gas.')
    print(' - If the contract is a proxy, ensure the implementation is initialized on this chain.')
    raise SystemExit('Aborting send: simulation failed for all candidate token addresses')

# Build the transaction using the successfully simulated token
print(f"Using token {chosen_token} for withdraw (simulation OK). Building transaction...")

tx = bridge.functions.withdraw(chosen_token, amount_wei, min_gas_l2, extra_data).build_transaction({
    "from": SENDER,
    "value": amount_wei,
    "nonce": nonce,
    "chainId": 70,                       # OP-like chain id used in your earlier code
})


gas_est = w3_l2.eth.estimate_gas(tx)
base_fee = w3_l2.eth.get_block("latest")["baseFeePerGas"]
priority = w3_l2.to_wei("1.5", "gwei")
tx.update({
    "gas": int(gas_est * 1.2),
    "maxFeePerGas": int(base_fee * 2 + priority),
    "maxPriorityFeePerGas": priority,
})

signed = w3_l2.eth.account.sign_transaction(tx, private_key)
tx_hash = w3_l2.eth.send_raw_transaction(signed.raw_transaction)
print("L2 withdraw tx:", w3_l2.to_hex(tx_hash))


rcpt = w3_l2.eth.wait_for_transaction_receipt(tx_hash)
print("L2 status:", rcpt.status)