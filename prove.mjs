// prove.mjs
import { createPublicClient, createWalletClient, defineChain, http } from 'viem'
import { privateKeyToAccount } from 'viem/accounts'
import {
  getWithdrawals,
  getL2Output,
  buildProveWithdrawal,
  proveWithdrawal,
} from 'viem/op-stack'

// -------- env --------
const L1_RPC_URL   = "http://130.60.144.77:8549" // do not change
const L2_RPC_URL   = "http://130.60.144.77:9545" // do not change
const PORTAL       = ("0x73d2a3289621d74bb85e1d2535518ab089b95759").toLowerCase() // do not change
const DGF          = ("0xa52e6bb6174601920e2347281939cd9988514e05").toLowerCase() // do not change
const L2_TX_HASH   = "0xc8ee4405dc1b4614bb482a37a87ff5dc854a234b2fdfb8a7bd45e7bad3802ca2" // replace
const L1_PRIV_KEY = '0x' + "xxxxxx" // replace

if (!L1_RPC_URL || !L2_RPC_URL || !PORTAL || !DGF || !L2_TX_HASH || !L1_PRIV_KEY) {
  console.error('Need L1_RPC_URL, L2_RPC_URL, PORTAL, DGF, L2_WITHDRAW_TX, L1_PRIVATE_KEY')
  process.exit(1)
}

// -------- chains (ids from your rollup.json) --------
const l1 = defineChain({
  id: 8888,
  name: 'L1-local',
  nativeCurrency: { name: 'Ether', symbol: 'ETH', decimals: 18 },
  rpcUrls: { default: { http: [L1_RPC_URL] } },
})

const l2 = defineChain({
  id: 70,
  name: 'L2-local',
  nativeCurrency: { name: 'Ether', symbol: 'ETH', decimals: 18 },
  rpcUrls: { default: { http: [L2_RPC_URL] } },

  // THE IMPORTANT BIT: tell viem which L1 contracts to use for this L2
  contracts: {
    // OptimismPortal lives on L1, mapped under the L1 id
    portal: {
      [l1.id]: { address: PORTAL },
    },
    // You’re on game-based outputs (respectedGameType = 1)
    disputeGameFactory: {
      [l1.id]: { address: DGF },
    },
    // l2OutputOracle not used on your chain (0x0), so omit it
  },
})

// -------- clients --------
const l2Public = createPublicClient({ chain: l2, transport: http() })
const l1Public = createPublicClient({ chain: l1, transport: http() })

const account  = privateKeyToAccount(L1_PRIV_KEY)
const l1Wallet = createWalletClient({ chain: l1, transport: http(), account })

// -------- 1) parse withdrawal from L2 tx --------
console.log('Fetching L2 receipt:', L2_TX_HASH)
const l2Rcpt = await l2Public.getTransactionReceipt({ hash: L2_TX_HASH })
const [withdrawal] = getWithdrawals(l2Rcpt)
if (!withdrawal) {
  console.error('No withdrawals found in that L2 tx. Double-check the tx hash.')
  process.exit(1)
}
console.log('withdrawalHash  :', withdrawal.withdrawalHash)
console.log('l2BlockNumber   :', l2Rcpt.blockNumber.toString())

// -------- sanity-print the addresses viem will use --------
console.log('\nUsing addresses:')
console.log('  L1 Portal            :', PORTAL)
console.log('  L1 DisputeGameFactory:', DGF)

// -------- 2) fetch the L2 output for that block from L1 --------
const output = await getL2Output(l1Public, {
  l2BlockNumber: l2Rcpt.blockNumber,
  targetChain: l2,
})
console.log('Output info      :', {
  l2BlockNumber: output.l2BlockNumber.toString(),
  outputRoot: output.outputRoot,
})

// -------- 3) build proofs (L2) & send prove tx (L1) --------
const args = await buildProveWithdrawal(l2Public, {
  account,
  output,
  withdrawal,
})

console.log('\nSubmitting proveWithdrawal on L1…')
const txHash = await proveWithdrawal(l1Wallet, {
  ...args,
  portalAddress: PORTAL, // explicit (custom chain)
})
console.log('proveWithdrawal tx:', txHash)

// -------- 4) wait for mining --------
const mined = await l1Public.waitForTransactionReceipt({ hash: txHash })
console.log('prove status     :', mined.status) // 'success' or 'reverted'