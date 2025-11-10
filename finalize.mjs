
// finalize.mjs
import { createPublicClient, createWalletClient, defineChain, http } from 'viem'
import { privateKeyToAccount } from 'viem/accounts'
import { getWithdrawals } from 'viem/op-stack'

// Minimal OptimismPortal ABI: read finalizedWithdrawals + finalizeWithdrawalTransaction
const OptimismPortalAbi = [
    {
        type: 'function',
        name: 'finalizedWithdrawals',
        stateMutability: 'view',
        inputs: [{ name: 'withdrawalHash', type: 'bytes32' }],
        outputs: [{ type: 'bool' }],
    },
    {
        type: 'function',
        name: 'finalizeWithdrawalTransaction',
        stateMutability: 'nonpayable',
        inputs: [{
            name: '_tx',
            type: 'tuple',
            components: [
                { name: 'nonce', type: 'uint256' },
                { name: 'sender', type: 'address' },
                { name: 'target', type: 'address' },
                { name: 'value', type: 'uint256' },
                { name: 'gasLimit', type: 'uint256' },
                { name: 'data', type: 'bytes' },
            ],
        },
        // { name: '_proofSubmitter', type: 'address' }
        ],
        outputs: [],
    },
]

const L1_RPC_URL = "http://130.60.144.77:8549" //do not change
const L2_RPC_URL = "http://130.60.144.77:9545" //do not change
const PORTAL = ("0x73d2a3289621d74bb85e1d2535518ab089b95759").toLowerCase() //do not change
// const DGF = ("0xa52e6bb6174601920e2347281939cd9988514e05").toLowerCase()
const L2_WITHDRAW_TX = "0xc8ee4405dc1b4614bb482a37a87ff5dc854a234b2fdfb8a7bd45e7bad3802ca2" // replace 
const L1_PRIVATE_KEY = "0x"+ "xxxxx" // replace

if (!L1_RPC_URL || !L2_RPC_URL || !PORTAL || !L2_WITHDRAW_TX || !L1_PRIVATE_KEY) {
    console.error('Missing env. Need L1_RPC_URL, L2_RPC_URL, PORTAL, L2_WITHDRAW_TX, L1_PRIVATE_KEY')
    process.exit(1)
}

// ---- chains (your ids) ----
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
})

// ---- clients & account ----
const l2Public = createPublicClient({ chain: l2, transport: http() })
const l1Public = createPublicClient({ chain: l1, transport: http() })

const account = privateKeyToAccount(L1_PRIVATE_KEY)
const l1Wallet = createWalletClient({ chain: l1, transport: http(), account })

// ---- 1) Extract the withdrawal from your L2 tx ----
console.log('Fetching L2 receipt:', L2_WITHDRAW_TX)
const l2Receipt = await l2Public.getTransactionReceipt({ hash: L2_WITHDRAW_TX })

const withdrawals = getWithdrawals(l2Receipt)
if (!withdrawals.length) {
    console.error('No withdrawals found in that L2 tx. Double-check L2_WITHDRAW_TX.')
    process.exit(1)
}
const w = withdrawals[0]
console.log('withdrawalHash  :', w.withdrawalHash)
console.log('withdrawal:', w)

// ---- 2) Already finalized? ----
const alreadyFinalized = await l1Public.readContract({
    address: PORTAL,
    abi: OptimismPortalAbi,
    functionName: 'finalizedWithdrawals',
    args: [w.withdrawalHash],
})
console.log('finalizedWithdrawals:', alreadyFinalized)
if (alreadyFinalized) {
    console.log('Already finalized; nothing to do.')
    process.exit(0)
}

// ---- 3) Dry-run the finalize on L1 (safe simulation) ----
// method1: simulateContract
let sim
try {
    sim = await l1Public.simulateContract({
        address: PORTAL,
        abi: OptimismPortalAbi,
        functionName: 'finalizeWithdrawalTransaction',
        args: [{
            nonce: w.nonce,
            sender: w.sender,
            target: w.target,
            value: w.value,
            gasLimit: w.gasLimit,
            data: w.data,
        }],
        account,
    })
    console.log('DRY RUN: finalize would SUCCEED')
} catch (err) {
    console.error('DRY RUN: finalize would REVERT')
    console.error(err?.shortMessage || err?.message || String(err))
    console.error('Revert data:', err)
    process.exit(1)
}





// ---- 4) Send (only if you set SEND_FINALIZE=1) ----
// if (String(SEND_FINALIZE) !== '1') {
//     console.log('\nSet SEND_FINALIZE=1 to actually send the finalize tx.')
//     process.exit(0)
// }

const txHash = await l1Wallet.writeContract(sim.request)
console.log('finalize tx     :', txHash)
const rcpt = await l1Public.waitForTransactionReceipt({ hash: txHash })
console.log('finalize status :', rcpt.status) // 'success' | 'reverted'


