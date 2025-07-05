# ALP Looping Bot: USDC x KOII (Arbitrum)

This Python bot automates an ALP looping strategy using:
- ✅ USDC (DeFi token)
- 🌐 KOII (DePIN token)
- 🧠 Radiant Capital Lending
- 🔄 Uniswap V3 for token swaps

## Features
- ALP Looping: deposit, borrow, swap
- DEX integration via Uniswap V3
- KOII token swap from borrowed USDT
- Basic LTV monitoring
- No external alerts (Telegram-free)
- Easy customization and extension

## Requirements
- Python 3.9+
- Web3.py
- dotenv
- Arbitrum RPC URL

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file based on `.env.example`.

3. Place ABI files in `abi/` folder.

4. Run the bot:
```bash
python alp_looping_bot.py
```

## To Do
- Add KOII staking logic
- Add real-time LTV risk logic
- Add optional database/logging
