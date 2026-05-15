# 🐾 Coven Traders — Idle RPG Trading Game

**Agora Agents Hackathon Submission** | Canteen × Circle | May 2026

## The Pitch

Command AI disciple fleets that trade **real USDC** across a sci-fi galaxy. An idle RPG where your agents work 24/7, you coach them in plain English, and every micro-transaction is a real on-chain trade on Arc (Circle's chain).

## What Makes It Different

| Feature | Why It Wins |
|---------|-------------|
| **Idle RPG + Real Money** | Offline earnings = actual yield from agent trades |
| **Natural Language Coaching** | "Only trade ETH perps, max 2x leverage" → compiled to strategy |
| **Bring Your Own Agent** | Connect external AI agents via API, coach them, sell them on marketplace |
| **Signal Aggregator** | 6 intel sources (on-chain, social, news, technical, predictions, arb) feed in-game buffs |
| **Meshy.ai 3D** | All avatars, ships, and environments generated via AI |
| **Micro-Transaction Scale** | $0.99 boosts, $4.99 packs, $9.99 battle pass — all in USDC |

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Signal Sources │────▶│  Signal Aggregator│────▶│   Redis Pub/Sub │
│  (6 sources)    │     │  (normalizer)     │     │                 │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
┌─────────────────┐     ┌──────────────────┐              │
│   Meshy.ai 3D   │     │  Next.js Frontend │◀─────────────┘
│  (avatars/scenes)│     │  (Three.js map)   │
└─────────────────┘     └──────────────────┘
                                 │
┌─────────────────┐     ┌────────┴──────────┐     ┌─────────────────┐
│  Agent Coaching │◀────│   Orchestrator    │────▶│  Circle/Arc     │
│  (NL → strategy)│     │  (routes signals) │     │  (USDC trades)  │
└─────────────────┘     └───────────────────┘     └─────────────────┘
                                 │
                        ┌────────┴──────────┐
                        │  Agent Marketplace │
                        │  (buy/sell/rent)   │
                        └───────────────────┘
```

## Tech Stack

- **Frontend**: Next.js 14, React Three Fiber, Tailwind CSS
- **3D Assets**: Meshy.ai API (text-to-3D)
- **Blockchain**: Solidity on Arc (Circle's chain), OpenZeppelin
- **Wallet**: Circle Web3 Services (embedded wallets, gasless tx)
- **Backend**: Python (signal aggregator), TypeScript (orchestrator)
- **Real-time**: Redis Pub/Sub, WebSocket
- **Payments**: USDC, CCTP, Circle Paymaster

## Contracts

| Contract | Purpose |
|----------|---------|
| `CrusadeEscrow.sol` | Tournament entry fees + prize distribution |
| `DiscipleNFT.sol` | Agent NFTs with stats, level, 3D model URI |
| `BoostToken.sol` | ERC-1155 consumable boosts |
| `Treasury.sol` | Fee collection + staking rewards |

## Revenue Model

1. **Tournament Entry Fees** — 10% platform fee
2. **Gacha Fleet Packs** — $4.99-$49.99
3. **Boost Shop** — $0.99-$2.99 per boost
4. **Battle Pass** — $9.99/season
5. **Agent Marketplace** — 5% commission on sales/rentals
6. **Signal Subscriptions** — Premium intel feeds
7. **Cosmetics** — Skins, command center themes
8. **Staking Yield** — Treasury distributes protocol revenue

## Getting Started

```bash
cd game-frontend
npm install
npm run dev

# In another terminal
cd ../signal-aggregator
pip install -r requirements.txt
python main.py

# In another terminal
cd ../orchestrator
npm install
npm start
```

## Hackathon RFB Mapping

| RFB | Disciple Specialization | Prize |
|-----|------------------------|-------|
| 01 Perp Futures | Perp Warrior | $15,000 |
| 02 Prediction Market Trader | Oracle Seer | $12,000 |
| 03 Prediction Market Verticals | Signal Hunter | $10,000 |
| 04 Adaptive Portfolio | Treasurer | $10,000 |
| 05 Cross-Platform Arb | Arbitrageur | $10,000 |
| 06 Social Trading | Market Maker | $8,000 |

## Team

Built by **Rex Deus** and the 12 Disciples 🐾

---

*"Let the agents trade while you sleep."*
