# alp_looping_bot.py
# ALP Looping strategy using USDC and KOII on Radiant + Uniswap V3
# No Telegram, local monitoring only

from web3 import Web3
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()

# -------------------- 🔐 Configuration --------------------
PRIVATE_KEY = os.getenv("PRIVATE_KEY")  # 🔑 Set your private key in the .env file
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
RPC_URL = os.getenv("RPC_URL")

# ✅ Addresses (fill in the real ones)
USDC_ADDRESS = "0xFF970A61A04b1cA14834A43f5de4533eBDDB5CC8"  # Arbitrum USDC
USDT_ADDRESS = "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9"  # Arbitrum USDT
KOII_ADDRESS = ""  # 🔧 Enter KOII token address on Arbitrum
RADIANT_LENDING_POOL = ""  # 🔧 Enter Radiant LendingPool address
UNISWAP_ROUTER = "0xE592427A0AEce92De3Edee1F18E0157C05861564"  # Uniswap V3 Router

# ABI loading (truncated - use full ABIs in production)
ERC20_ABI = json.load(open("./abi/erc20.json"))
UNISWAP_ABI = json.load(open("./abi/uniswap_router.json"))
RADIANT_ABI = json.load(open("./abi/radiant_lending_pool.json"))

# Initialize Web3
web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)

# -------------------- ⚙️ Core Functions --------------------
def approve_token(token_address, spender, amount):
    token = web3.eth.contract(address=token_address, abi=ERC20_ABI)
    tx = token.functions.approve(spender, amount).build_transaction({
        'from': WALLET_ADDRESS,
        'nonce': web3.eth.get_transaction_count(WALLET_ADDRESS),
        'gas': 100000,
        'gasPrice': web3.to_wei('2', 'gwei')
    })
    signed = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    print(f"✅ Approved: {tx_hash.hex()}")
    web3.eth.wait_for_transaction_receipt(tx_hash)

def swap_usdt_to_koii(amount_in):
    router = web3.eth.contract(address=UNISWAP_ROUTER, abi=UNISWAP_ABI)
    deadline = int(time.time()) + 600
    path = [USDT_ADDRESS, KOII_ADDRESS]
    amount_out_min = 0  # You can add slippage handling logic here

    tx = router.functions.exactInputSingle({
        'tokenIn': USDT_ADDRESS,
        'tokenOut': KOII_ADDRESS,
        'fee': 3000,
        'recipient': WALLET_ADDRESS,
        'deadline': deadline,
        'amountIn': amount_in,
        'amountOutMinimum': amount_out_min,
        'sqrtPriceLimitX96': 0
    }).build_transaction({
        'from': WALLET_ADDRESS,
        'nonce': web3.eth.get_transaction_count(WALLET_ADDRESS),
        'gas': 200000,
        'gasPrice': web3.to_wei('2', 'gwei')
    })
    signed = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    print(f"🔄 Swapped to KOII: {tx_hash.hex()}")
    web3.eth.wait_for_transaction_receipt(tx_hash)

def monitor_ltv():
    # You can integrate LTV check logic using Radiant contract here
    print("📊 (mock) LTV is stable: 63.5%")

# -------------------- 🚀 Main Loop --------------------
def main():
    print("[ALP-KOII-BOT] Starting Looping Strategy...")

    deposit_amount = web3.to_wei(100, 'mwei')  # USDC uses 6 decimals

    # Approve USDC for Radiant
    approve_token(USDC_ADDRESS, RADIANT_LENDING_POOL, deposit_amount)
    # TODO: Add deposit logic for Radiant

    # Approve USDT for Uniswap swap
    approve_token(USDT_ADDRESS, UNISWAP_ROUTER, web3.to_wei(70, 'mwei'))
    swap_usdt_to_koii(web3.to_wei(50, 'mwei'))

    # TODO: Stake KOII if staking contract is available

    while True:
        monitor_ltv()
        time.sleep(60)

if __name__ == "__main__":
    main()
