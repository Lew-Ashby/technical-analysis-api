"""Comprehensive asset registry for crypto tokens and stocks."""
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


class AssetType(str, Enum):
    CRYPTO = "crypto"
    STOCK = "stock"


class CryptoCategory(str, Enum):
    LAYER_1 = "Layer 1"
    LAYER_2 = "Layer 2"
    DEFI = "DeFi"
    MEME = "Meme"
    GAMING = "Gaming/Metaverse"
    AI = "AI"
    EXCHANGE = "Exchange Token"
    STABLECOIN = "Stablecoin"
    PRIVACY = "Privacy"
    ORACLE = "Oracle"
    STORAGE = "Storage"
    NFT = "NFT/Collectibles"
    INFRASTRUCTURE = "Infrastructure"
    RWA = "Real World Assets"


class StockCategory(str, Enum):
    TECH = "Technology"
    FINANCE = "Finance"
    HEALTHCARE = "Healthcare"
    CONSUMER = "Consumer"
    ENERGY = "Energy"
    INDUSTRIAL = "Industrial"
    COMMUNICATION = "Communication"
    MATERIALS = "Materials"
    UTILITIES = "Utilities"
    REAL_ESTATE = "Real Estate"
    ETF = "ETF"
    INDEX = "Index"


@dataclass
class Asset:
    """Represents a tradeable asset."""
    symbol: str
    name: str
    asset_type: AssetType
    category: str
    coingecko_id: Optional[str] = None  # For crypto
    description: Optional[str] = None
    logo_url: Optional[str] = None
    mcap_rank: Optional[int] = None  # Market cap rank (lower = higher mcap)


# ============================================================================
# COMPREHENSIVE CRYPTO REGISTRY
# ============================================================================

CRYPTO_ASSETS: Dict[str, Asset] = {
    # Layer 1 Blockchains (with market cap rankings)
    "BTC": Asset("BTC", "Bitcoin", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "bitcoin", "The original cryptocurrency", mcap_rank=1),
    "ETH": Asset("ETH", "Ethereum", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "ethereum", "Smart contract platform", mcap_rank=2),
    "SOL": Asset("SOL", "Solana", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "solana", "High-performance blockchain", mcap_rank=5),
    "ADA": Asset("ADA", "Cardano", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "cardano", "Proof-of-stake blockchain", mcap_rank=10),
    "AVAX": Asset("AVAX", "Avalanche", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "avalanche-2", "Subnets blockchain", mcap_rank=12),
    "DOT": Asset("DOT", "Polkadot", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "polkadot", "Multi-chain protocol", mcap_rank=15),
    "ATOM": Asset("ATOM", "Cosmos", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "cosmos", "Internet of blockchains", mcap_rank=25),
    "NEAR": Asset("NEAR", "NEAR Protocol", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "near", "Sharded blockchain", mcap_rank=22),
    "APT": Asset("APT", "Aptos", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "aptos", "Move-based blockchain", mcap_rank=30),
    "SUI": Asset("SUI", "Sui", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "sui", "Move-based L1", mcap_rank=20),
    "SEI": Asset("SEI", "Sei", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "sei-network", "Trading-focused L1", mcap_rank=55),
    "INJ": Asset("INJ", "Injective", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "injective-protocol", "DeFi-focused L1", mcap_rank=40),
    "TIA": Asset("TIA", "Celestia", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "celestia", "Modular data availability", mcap_rank=45),
    "ICP": Asset("ICP", "Internet Computer", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "internet-computer", "World computer", mcap_rank=24),
    "FTM": Asset("FTM", "Fantom", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "fantom", "DAG-based smart contracts", mcap_rank=60),
    "ALGO": Asset("ALGO", "Algorand", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "algorand", "Pure proof-of-stake", mcap_rank=65),
    "XTZ": Asset("XTZ", "Tezos", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "tezos", "Self-amending blockchain", mcap_rank=80),
    "HBAR": Asset("HBAR", "Hedera", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "hedera-hashgraph", "Hashgraph consensus", mcap_rank=18),
    "EGLD": Asset("EGLD", "MultiversX", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "elrond-erd-2", "Adaptive sharding", mcap_rank=75),
    "FLOW": Asset("FLOW", "Flow", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "flow", "NFT-focused blockchain", mcap_rank=85),
    "KAS": Asset("KAS", "Kaspa", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "kaspa", "BlockDAG protocol", mcap_rank=35),
    "XLM": Asset("XLM", "Stellar", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "stellar", "Financial network", mcap_rank=14),
    "XRP": Asset("XRP", "XRP", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "ripple", "Payment protocol", mcap_rank=4),
    "LTC": Asset("LTC", "Litecoin", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "litecoin", "Silver to Bitcoin's gold", mcap_rank=19),
    "BCH": Asset("BCH", "Bitcoin Cash", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "bitcoin-cash", "Bitcoin fork", mcap_rank=17),
    "ETC": Asset("ETC", "Ethereum Classic", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "ethereum-classic", "Original Ethereum chain", mcap_rank=28),
    "TRX": Asset("TRX", "TRON", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "tron", "Entertainment blockchain", mcap_rank=8),
    "VET": Asset("VET", "VeChain", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "vechain", "Supply chain blockchain", mcap_rank=42),
    "EOS": Asset("EOS", "EOS", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "eos", "Enterprise blockchain", mcap_rank=90),
    "XMR": Asset("XMR", "Monero", AssetType.CRYPTO, CryptoCategory.PRIVACY.value, "monero", "Privacy cryptocurrency", mcap_rank=32),
    "ZEC": Asset("ZEC", "Zcash", AssetType.CRYPTO, CryptoCategory.PRIVACY.value, "zcash", "Privacy coin with zk-SNARKs", mcap_rank=120),
    "DASH": Asset("DASH", "Dash", AssetType.CRYPTO, CryptoCategory.PRIVACY.value, "dash", "Digital cash", mcap_rank=130),
    "NEO": Asset("NEO", "Neo", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "neo", "Chinese Ethereum", mcap_rank=95),
    "KAVA": Asset("KAVA", "Kava", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "kava", "Cosmos DeFi hub", mcap_rank=110),
    "ROSE": Asset("ROSE", "Oasis Network", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "oasis-network", "Privacy-focused L1", mcap_rank=140),
    "MINA": Asset("MINA", "Mina Protocol", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "mina-protocol", "Lightweight blockchain", mcap_rank=100),
    "ONE": Asset("ONE", "Harmony", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "harmony", "Sharded blockchain", mcap_rank=200),
    "CELO": Asset("CELO", "Celo", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "celo", "Mobile-first blockchain", mcap_rank=150),
    "WAVES": Asset("WAVES", "Waves", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "waves", "Mass adoption blockchain", mcap_rank=180),
    "ZIL": Asset("ZIL", "Zilliqa", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "zilliqa", "Sharded blockchain", mcap_rank=190),
    "ICX": Asset("ICX", "ICON", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "icon", "Korean blockchain", mcap_rank=210),
    "QTUM": Asset("QTUM", "Qtum", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "qtum", "Bitcoin + Ethereum hybrid", mcap_rank=220),
    "ONT": Asset("ONT", "Ontology", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "ontology", "Enterprise blockchain", mcap_rank=230),
    "THETA": Asset("THETA", "Theta Network", AssetType.CRYPTO, CryptoCategory.LAYER_1.value, "theta-token", "Video streaming", mcap_rank=70),

    # Layer 2 Solutions
    "MATIC": Asset("MATIC", "Polygon", AssetType.CRYPTO, CryptoCategory.LAYER_2.value, "matic-network", "Ethereum scaling", mcap_rank=13),
    "ARB": Asset("ARB", "Arbitrum", AssetType.CRYPTO, CryptoCategory.LAYER_2.value, "arbitrum", "Optimistic rollup", mcap_rank=38),
    "OP": Asset("OP", "Optimism", AssetType.CRYPTO, CryptoCategory.LAYER_2.value, "optimism", "Optimistic rollup", mcap_rank=36),
    "IMX": Asset("IMX", "Immutable X", AssetType.CRYPTO, CryptoCategory.LAYER_2.value, "immutable-x", "NFT scaling", mcap_rank=50),
    "LRC": Asset("LRC", "Loopring", AssetType.CRYPTO, CryptoCategory.LAYER_2.value, "loopring", "zkRollup DEX", mcap_rank=160),
    "METIS": Asset("METIS", "Metis", AssetType.CRYPTO, CryptoCategory.LAYER_2.value, "metis-token", "Optimistic rollup", mcap_rank=170),
    "STRK": Asset("STRK", "Starknet", AssetType.CRYPTO, CryptoCategory.LAYER_2.value, "starknet", "zk-STARK rollup", mcap_rank=68),
    "ZK": Asset("ZK", "zkSync", AssetType.CRYPTO, CryptoCategory.LAYER_2.value, "zksync", "zkRollup", mcap_rank=115),
    "MANTA": Asset("MANTA", "Manta Network", AssetType.CRYPTO, CryptoCategory.LAYER_2.value, "manta-network", "Modular L2", mcap_rank=125),
    "BLAST": Asset("BLAST", "Blast", AssetType.CRYPTO, CryptoCategory.LAYER_2.value, "blast", "Native yield L2", mcap_rank=135),
    "ZETA": Asset("ZETA", "ZetaChain", AssetType.CRYPTO, CryptoCategory.LAYER_2.value, "zetachain", "Omnichain L1", mcap_rank=145),
    "BOBA": Asset("BOBA", "Boba Network", AssetType.CRYPTO, CryptoCategory.LAYER_2.value, "boba-network", "Hybrid compute L2", mcap_rank=300),
    "SKL": Asset("SKL", "SKALE", AssetType.CRYPTO, CryptoCategory.LAYER_2.value, "skale", "Elastic sidechains", mcap_rank=175),

    # DeFi Protocols
    "UNI": Asset("UNI", "Uniswap", AssetType.CRYPTO, CryptoCategory.DEFI.value, "uniswap", "DEX protocol", mcap_rank=23),
    "AAVE": Asset("AAVE", "Aave", AssetType.CRYPTO, CryptoCategory.DEFI.value, "aave", "Lending protocol", mcap_rank=34),
    "MKR": Asset("MKR", "Maker", AssetType.CRYPTO, CryptoCategory.DEFI.value, "maker", "DAI stablecoin issuer", mcap_rank=48),
    "CRV": Asset("CRV", "Curve", AssetType.CRYPTO, CryptoCategory.DEFI.value, "curve-dao-token", "Stablecoin DEX", mcap_rank=105),
    "LDO": Asset("LDO", "Lido DAO", AssetType.CRYPTO, CryptoCategory.DEFI.value, "lido-dao", "Liquid staking", mcap_rank=58),
    "SNX": Asset("SNX", "Synthetix", AssetType.CRYPTO, CryptoCategory.DEFI.value, "havven", "Synthetic assets", mcap_rank=155),
    "COMP": Asset("COMP", "Compound", AssetType.CRYPTO, CryptoCategory.DEFI.value, "compound-governance-token", "Lending protocol", mcap_rank=165),
    "SUSHI": Asset("SUSHI", "SushiSwap", AssetType.CRYPTO, CryptoCategory.DEFI.value, "sushi", "DEX protocol", mcap_rank=195),
    "1INCH": Asset("1INCH", "1inch", AssetType.CRYPTO, CryptoCategory.DEFI.value, "1inch", "DEX aggregator", mcap_rank=185),
    "DYDX": Asset("DYDX", "dYdX", AssetType.CRYPTO, CryptoCategory.DEFI.value, "dydx", "Perp DEX", mcap_rank=78),
    "GMX": Asset("GMX", "GMX", AssetType.CRYPTO, CryptoCategory.DEFI.value, "gmx", "Perp DEX", mcap_rank=112),
    "PENDLE": Asset("PENDLE", "Pendle", AssetType.CRYPTO, CryptoCategory.DEFI.value, "pendle", "Yield trading", mcap_rank=72),
    "JUP": Asset("JUP", "Jupiter", AssetType.CRYPTO, CryptoCategory.DEFI.value, "jupiter-exchange-solana", "Solana DEX aggregator", mcap_rank=52),
    "RAY": Asset("RAY", "Raydium", AssetType.CRYPTO, CryptoCategory.DEFI.value, "raydium", "Solana AMM", mcap_rank=88),
    "YFI": Asset("YFI", "yearn.finance", AssetType.CRYPTO, CryptoCategory.DEFI.value, "yearn-finance", "Yield aggregator", mcap_rank=240),
    "BAL": Asset("BAL", "Balancer", AssetType.CRYPTO, CryptoCategory.DEFI.value, "balancer", "Programmable liquidity", mcap_rank=250),
    "CAKE": Asset("CAKE", "PancakeSwap", AssetType.CRYPTO, CryptoCategory.DEFI.value, "pancakeswap-token", "BSC DEX", mcap_rank=108),
    "JOE": Asset("JOE", "Trader Joe", AssetType.CRYPTO, CryptoCategory.DEFI.value, "joe", "Avalanche DEX", mcap_rank=260),
    "SPELL": Asset("SPELL", "Spell Token", AssetType.CRYPTO, CryptoCategory.DEFI.value, "spell-token", "Abracadabra Money", mcap_rank=350),
    "RPL": Asset("RPL", "Rocket Pool", AssetType.CRYPTO, CryptoCategory.DEFI.value, "rocket-pool", "Decentralized staking", mcap_rank=138),
    "RUNE": Asset("RUNE", "THORChain", AssetType.CRYPTO, CryptoCategory.DEFI.value, "thorchain", "Cross-chain swaps", mcap_rank=62),
    "OSMO": Asset("OSMO", "Osmosis", AssetType.CRYPTO, CryptoCategory.DEFI.value, "osmosis", "Cosmos DEX", mcap_rank=118),
    "CVX": Asset("CVX", "Convex Finance", AssetType.CRYPTO, CryptoCategory.DEFI.value, "convex-finance", "Curve booster", mcap_rank=270),
    "FXS": Asset("FXS", "Frax Share", AssetType.CRYPTO, CryptoCategory.DEFI.value, "frax-share", "Algorithmic stablecoin", mcap_rank=280),
    "LQTY": Asset("LQTY", "Liquity", AssetType.CRYPTO, CryptoCategory.DEFI.value, "liquity", "Decentralized borrowing", mcap_rank=290),
    "RBN": Asset("RBN", "Ribbon Finance", AssetType.CRYPTO, CryptoCategory.DEFI.value, "ribbon-finance", "Structured products", mcap_rank=400),
    "PERP": Asset("PERP", "Perpetual Protocol", AssetType.CRYPTO, CryptoCategory.DEFI.value, "perpetual-protocol", "Perp DEX", mcap_rank=380),
    "BADGER": Asset("BADGER", "Badger DAO", AssetType.CRYPTO, CryptoCategory.DEFI.value, "badger-dao", "Bitcoin DeFi", mcap_rank=390),
    "MORPHO": Asset("MORPHO", "Morpho", AssetType.CRYPTO, CryptoCategory.DEFI.value, "morpho", "Lending optimizer", mcap_rank=178),
    "ENA": Asset("ENA", "Ethena", AssetType.CRYPTO, CryptoCategory.DEFI.value, "ethena", "Synthetic dollar", mcap_rank=56),
    "EIGEN": Asset("EIGEN", "EigenLayer", AssetType.CRYPTO, CryptoCategory.DEFI.value, "eigenlayer", "Restaking protocol", mcap_rank=82),

    # Exchange Tokens
    "BNB": Asset("BNB", "BNB", AssetType.CRYPTO, CryptoCategory.EXCHANGE.value, "binancecoin", "Binance exchange token", mcap_rank=3),
    "OKB": Asset("OKB", "OKB", AssetType.CRYPTO, CryptoCategory.EXCHANGE.value, "okb", "OKX exchange token", mcap_rank=26),
    "CRO": Asset("CRO", "Cronos", AssetType.CRYPTO, CryptoCategory.EXCHANGE.value, "crypto-com-chain", "Crypto.com token", mcap_rank=46),
    "KCS": Asset("KCS", "KuCoin Token", AssetType.CRYPTO, CryptoCategory.EXCHANGE.value, "kucoin-shares", "KuCoin token", mcap_rank=92),
    "GT": Asset("GT", "GateToken", AssetType.CRYPTO, CryptoCategory.EXCHANGE.value, "gatechain-token", "Gate.io token", mcap_rank=98),
    "HT": Asset("HT", "Huobi Token", AssetType.CRYPTO, CryptoCategory.EXCHANGE.value, "huobi-token", "Huobi token", mcap_rank=152),
    "LEO": Asset("LEO", "LEO Token", AssetType.CRYPTO, CryptoCategory.EXCHANGE.value, "leo-token", "Bitfinex token", mcap_rank=21),
    "MX": Asset("MX", "MX Token", AssetType.CRYPTO, CryptoCategory.EXCHANGE.value, "mx-token", "MEXC token", mcap_rank=168),

    # Oracles
    "LINK": Asset("LINK", "Chainlink", AssetType.CRYPTO, CryptoCategory.ORACLE.value, "chainlink", "Decentralized oracle", mcap_rank=11),
    "BAND": Asset("BAND", "Band Protocol", AssetType.CRYPTO, CryptoCategory.ORACLE.value, "band-protocol", "Cross-chain oracle", mcap_rank=310),
    "API3": Asset("API3", "API3", AssetType.CRYPTO, CryptoCategory.ORACLE.value, "api3", "First-party oracles", mcap_rank=255),
    "TRB": Asset("TRB", "Tellor", AssetType.CRYPTO, CryptoCategory.ORACLE.value, "tellor", "Decentralized oracle", mcap_rank=320),
    "UMA": Asset("UMA", "UMA", AssetType.CRYPTO, CryptoCategory.ORACLE.value, "uma", "Optimistic oracle", mcap_rank=330),
    "PYTH": Asset("PYTH", "Pyth Network", AssetType.CRYPTO, CryptoCategory.ORACLE.value, "pyth-network", "Solana oracle", mcap_rank=66),
    "DIA": Asset("DIA", "DIA", AssetType.CRYPTO, CryptoCategory.ORACLE.value, "dia-data", "Open-source oracle", mcap_rank=340),

    # AI & Compute
    "FET": Asset("FET", "Fetch.ai", AssetType.CRYPTO, CryptoCategory.AI.value, "fetch-ai", "AI & machine learning", mcap_rank=27),
    "AGIX": Asset("AGIX", "SingularityNET", AssetType.CRYPTO, CryptoCategory.AI.value, "singularitynet", "AI marketplace", mcap_rank=86),
    "OCEAN": Asset("OCEAN", "Ocean Protocol", AssetType.CRYPTO, CryptoCategory.AI.value, "ocean-protocol", "Data marketplace", mcap_rank=128),
    "RNDR": Asset("RNDR", "Render", AssetType.CRYPTO, CryptoCategory.AI.value, "render-token", "GPU rendering", mcap_rank=29),
    "TAO": Asset("TAO", "Bittensor", AssetType.CRYPTO, CryptoCategory.AI.value, "bittensor", "Decentralized AI", mcap_rank=31),
    "ARKM": Asset("ARKM", "Arkham", AssetType.CRYPTO, CryptoCategory.AI.value, "arkham", "Blockchain intelligence", mcap_rank=102),
    "WLD": Asset("WLD", "Worldcoin", AssetType.CRYPTO, CryptoCategory.AI.value, "worldcoin-wld", "World ID", mcap_rank=54),
    "AKT": Asset("AKT", "Akash Network", AssetType.CRYPTO, CryptoCategory.AI.value, "akash-network", "Decentralized cloud", mcap_rank=76),
    "GLM": Asset("GLM", "Golem", AssetType.CRYPTO, CryptoCategory.AI.value, "golem", "Decentralized compute", mcap_rank=182),
    "NMR": Asset("NMR", "Numeraire", AssetType.CRYPTO, CryptoCategory.AI.value, "numeraire", "Data science", mcap_rank=360),
    "PRIME": Asset("PRIME", "Echelon Prime", AssetType.CRYPTO, CryptoCategory.AI.value, "echelon-prime", "Gaming AI", mcap_rank=142),

    # Gaming & Metaverse
    "AXS": Asset("AXS", "Axie Infinity", AssetType.CRYPTO, CryptoCategory.GAMING.value, "axie-infinity", "Play-to-earn gaming", mcap_rank=96),
    "SAND": Asset("SAND", "The Sandbox", AssetType.CRYPTO, CryptoCategory.GAMING.value, "the-sandbox", "Virtual world", mcap_rank=74),
    "MANA": Asset("MANA", "Decentraland", AssetType.CRYPTO, CryptoCategory.GAMING.value, "decentraland", "Virtual reality", mcap_rank=84),
    "GALA": Asset("GALA", "Gala Games", AssetType.CRYPTO, CryptoCategory.GAMING.value, "gala", "Blockchain gaming", mcap_rank=64),
    "ENJ": Asset("ENJ", "Enjin Coin", AssetType.CRYPTO, CryptoCategory.GAMING.value, "enjincoin", "Gaming NFTs", mcap_rank=215),
    "ILV": Asset("ILV", "Illuvium", AssetType.CRYPTO, CryptoCategory.GAMING.value, "illuvium", "Open-world RPG", mcap_rank=225),
    "MAGIC": Asset("MAGIC", "Magic", AssetType.CRYPTO, CryptoCategory.GAMING.value, "magic", "Treasure ecosystem", mcap_rank=235),
    "APE": Asset("APE", "ApeCoin", AssetType.CRYPTO, CryptoCategory.GAMING.value, "apecoin", "BAYC ecosystem", mcap_rank=122),
    "YGG": Asset("YGG", "Yield Guild Games", AssetType.CRYPTO, CryptoCategory.GAMING.value, "yield-guild-games", "Gaming guild", mcap_rank=295),
    "ALICE": Asset("ALICE", "My Neighbor Alice", AssetType.CRYPTO, CryptoCategory.GAMING.value, "my-neighbor-alice", "Farming game", mcap_rank=355),
    "SUPER": Asset("SUPER", "SuperVerse", AssetType.CRYPTO, CryptoCategory.GAMING.value, "superfarm", "NFT marketplace", mcap_rank=305),
    "BEAM": Asset("BEAM", "Beam", AssetType.CRYPTO, CryptoCategory.GAMING.value, "beam-2", "Gaming subnet", mcap_rank=94),
    "RONIN": Asset("RONIN", "Ronin", AssetType.CRYPTO, CryptoCategory.GAMING.value, "ronin", "Gaming sidechain", mcap_rank=53),
    "PIXEL": Asset("PIXEL", "Pixels", AssetType.CRYPTO, CryptoCategory.GAMING.value, "pixels", "Web3 farming", mcap_rank=246),
    "PORTAL": Asset("PORTAL", "Portal", AssetType.CRYPTO, CryptoCategory.GAMING.value, "portal", "Gaming L2", mcap_rank=370),
    "PYR": Asset("PYR", "Vulcan Forged", AssetType.CRYPTO, CryptoCategory.GAMING.value, "vulcan-forged", "Gaming ecosystem", mcap_rank=365),
    "AUDIO": Asset("AUDIO", "Audius", AssetType.CRYPTO, CryptoCategory.GAMING.value, "audius", "Decentralized music", mcap_rank=315),
    "CHZ": Asset("CHZ", "Chiliz", AssetType.CRYPTO, CryptoCategory.GAMING.value, "chiliz", "Sports tokens", mcap_rank=132),

    # Meme Coins
    "DOGE": Asset("DOGE", "Dogecoin", AssetType.CRYPTO, CryptoCategory.MEME.value, "dogecoin", "Original meme coin", mcap_rank=7),
    "SHIB": Asset("SHIB", "Shiba Inu", AssetType.CRYPTO, CryptoCategory.MEME.value, "shiba-inu", "Dogecoin killer", mcap_rank=16),
    "PEPE": Asset("PEPE", "Pepe", AssetType.CRYPTO, CryptoCategory.MEME.value, "pepe", "Frog meme coin", mcap_rank=33),
    "FLOKI": Asset("FLOKI", "Floki", AssetType.CRYPTO, CryptoCategory.MEME.value, "floki", "Viking dog meme", mcap_rank=57),
    "BONK": Asset("BONK", "Bonk", AssetType.CRYPTO, CryptoCategory.MEME.value, "bonk", "Solana meme coin", mcap_rank=44),
    "WIF": Asset("WIF", "dogwifhat", AssetType.CRYPTO, CryptoCategory.MEME.value, "dogwifcoin", "Dog with hat", mcap_rank=41),
    "MEME": Asset("MEME", "Memecoin", AssetType.CRYPTO, CryptoCategory.MEME.value, "meme", "9GAG memecoin", mcap_rank=156),
    "ELON": Asset("ELON", "Dogelon Mars", AssetType.CRYPTO, CryptoCategory.MEME.value, "dogelon-mars", "Mars meme coin", mcap_rank=275),
    "BABYDOGE": Asset("BABYDOGE", "Baby Doge", AssetType.CRYPTO, CryptoCategory.MEME.value, "baby-doge-coin", "Baby Dogecoin", mcap_rank=188),
    "MYRO": Asset("MYRO", "Myro", AssetType.CRYPTO, CryptoCategory.MEME.value, "myro", "Solana meme", mcap_rank=325),
    "BRETT": Asset("BRETT", "Brett", AssetType.CRYPTO, CryptoCategory.MEME.value, "brett", "Base meme coin", mcap_rank=79),
    "MOG": Asset("MOG", "Mog Coin", AssetType.CRYPTO, CryptoCategory.MEME.value, "mog-coin", "Cat meme coin", mcap_rank=116),
    "POPCAT": Asset("POPCAT", "Popcat", AssetType.CRYPTO, CryptoCategory.MEME.value, "popcat", "Pop cat meme", mcap_rank=89),
    "COQ": Asset("COQ", "Coq Inu", AssetType.CRYPTO, CryptoCategory.MEME.value, "coq-inu", "Avalanche meme", mcap_rank=345),
    "WOJAK": Asset("WOJAK", "Wojak", AssetType.CRYPTO, CryptoCategory.MEME.value, "wojak", "Wojak meme coin", mcap_rank=420),
    "TURBO": Asset("TURBO", "Turbo", AssetType.CRYPTO, CryptoCategory.MEME.value, "turbo", "AI-generated meme", mcap_rank=162),
    "NEIRO": Asset("NEIRO", "Neiro", AssetType.CRYPTO, CryptoCategory.MEME.value, "first-neiro-on-ethereum", "Dog meme coin", mcap_rank=126),
    "SPX": Asset("SPX", "SPX6900", AssetType.CRYPTO, CryptoCategory.MEME.value, "spx6900", "SPX meme", mcap_rank=148),
    "GOAT": Asset("GOAT", "Goatseus Maximus", AssetType.CRYPTO, CryptoCategory.MEME.value, "goatseus-maximus", "AI meme coin", mcap_rank=136),
    "ACT": Asset("ACT", "Act I", AssetType.CRYPTO, CryptoCategory.MEME.value, "act-i-the-ai-prophecy", "AI prophecy meme", mcap_rank=158),

    # Storage
    "FIL": Asset("FIL", "Filecoin", AssetType.CRYPTO, CryptoCategory.STORAGE.value, "filecoin", "Decentralized storage", mcap_rank=37),
    "AR": Asset("AR", "Arweave", AssetType.CRYPTO, CryptoCategory.STORAGE.value, "arweave", "Permanent storage", mcap_rank=59),
    "STORJ": Asset("STORJ", "Storj", AssetType.CRYPTO, CryptoCategory.STORAGE.value, "storj", "Cloud storage", mcap_rank=265),
    "SC": Asset("SC", "Siacoin", AssetType.CRYPTO, CryptoCategory.STORAGE.value, "siacoin", "Decentralized storage", mcap_rank=192),
    "BTT": Asset("BTT", "BitTorrent", AssetType.CRYPTO, CryptoCategory.STORAGE.value, "bittorrent", "File sharing", mcap_rank=67),

    # Infrastructure
    "GRT": Asset("GRT", "The Graph", AssetType.CRYPTO, CryptoCategory.INFRASTRUCTURE.value, "the-graph", "Indexing protocol", mcap_rank=47),
    "ENS": Asset("ENS", "Ethereum Name Service", AssetType.CRYPTO, CryptoCategory.INFRASTRUCTURE.value, "ethereum-name-service", "Domain names", mcap_rank=114),
    "SSV": Asset("SSV", "SSV Network", AssetType.CRYPTO, CryptoCategory.INFRASTRUCTURE.value, "ssv-network", "DVT protocol", mcap_rank=198),
    "ANKR": Asset("ANKR", "Ankr", AssetType.CRYPTO, CryptoCategory.INFRASTRUCTURE.value, "ankr", "Web3 infrastructure", mcap_rank=205),
    "LPT": Asset("LPT", "Livepeer", AssetType.CRYPTO, CryptoCategory.INFRASTRUCTURE.value, "livepeer", "Video streaming", mcap_rank=124),
    "POKT": Asset("POKT", "Pocket Network", AssetType.CRYPTO, CryptoCategory.INFRASTRUCTURE.value, "pocket-network", "RPC services", mcap_rank=252),
    "QNT": Asset("QNT", "Quant", AssetType.CRYPTO, CryptoCategory.INFRASTRUCTURE.value, "quant-network", "Interoperability", mcap_rank=63),
    "HNT": Asset("HNT", "Helium", AssetType.CRYPTO, CryptoCategory.INFRASTRUCTURE.value, "helium", "IoT network", mcap_rank=77),
    "MOBILE": Asset("MOBILE", "Helium Mobile", AssetType.CRYPTO, CryptoCategory.INFRASTRUCTURE.value, "helium-mobile", "Mobile network", mcap_rank=202),
    "IOTX": Asset("IOTX", "IoTeX", AssetType.CRYPTO, CryptoCategory.INFRASTRUCTURE.value, "iotex", "IoT blockchain", mcap_rank=172),
    "STX": Asset("STX", "Stacks", AssetType.CRYPTO, CryptoCategory.INFRASTRUCTURE.value, "blockstack", "Bitcoin smart contracts", mcap_rank=39),
    "CFX": Asset("CFX", "Conflux", AssetType.CRYPTO, CryptoCategory.INFRASTRUCTURE.value, "conflux-token", "Tree-graph blockchain", mcap_rank=146),
    "COTI": Asset("COTI", "COTI", AssetType.CRYPTO, CryptoCategory.INFRASTRUCTURE.value, "coti", "Payment network", mcap_rank=218),
    "CTSI": Asset("CTSI", "Cartesi", AssetType.CRYPTO, CryptoCategory.INFRASTRUCTURE.value, "cartesi", "Linux rollups", mcap_rank=285),
    "ACH": Asset("ACH", "Alchemy Pay", AssetType.CRYPTO, CryptoCategory.INFRASTRUCTURE.value, "alchemy-pay", "Payment gateway", mcap_rank=228),
    "RLC": Asset("RLC", "iExec", AssetType.CRYPTO, CryptoCategory.INFRASTRUCTURE.value, "iexec-rlc", "Cloud computing", mcap_rank=375),

    # Real World Assets (RWA)
    "ONDO": Asset("ONDO", "Ondo Finance", AssetType.CRYPTO, CryptoCategory.RWA.value, "ondo-finance", "Tokenized treasuries", mcap_rank=51),
    "MNT": Asset("MNT", "Mantle", AssetType.CRYPTO, CryptoCategory.RWA.value, "mantle", "L2 with RWA", mcap_rank=43),
    "RSR": Asset("RSR", "Reserve Rights", AssetType.CRYPTO, CryptoCategory.RWA.value, "reserve-rights-token", "Stablecoin protocol", mcap_rank=258),
    "MPL": Asset("MPL", "Maple", AssetType.CRYPTO, CryptoCategory.RWA.value, "maple", "Institutional lending", mcap_rank=385),
    "CFG": Asset("CFG", "Centrifuge", AssetType.CRYPTO, CryptoCategory.RWA.value, "centrifuge", "Real-world assets", mcap_rank=335),
    "DUSK": Asset("DUSK", "Dusk Network", AssetType.CRYPTO, CryptoCategory.RWA.value, "dusk-network", "Financial infrastructure", mcap_rank=395),
    "RIO": Asset("RIO", "Realio", AssetType.CRYPTO, CryptoCategory.RWA.value, "realio-network", "Tokenized real estate", mcap_rank=450),

    # NFT/Collectibles
    "BLUR": Asset("BLUR", "Blur", AssetType.CRYPTO, CryptoCategory.NFT.value, "blur", "NFT marketplace", mcap_rank=104),
    "LOOKS": Asset("LOOKS", "LooksRare", AssetType.CRYPTO, CryptoCategory.NFT.value, "looksrare", "NFT marketplace", mcap_rank=410),
    "X2Y2": Asset("X2Y2", "X2Y2", AssetType.CRYPTO, CryptoCategory.NFT.value, "x2y2", "NFT marketplace", mcap_rank=430),
    "RARE": Asset("RARE", "SuperRare", AssetType.CRYPTO, CryptoCategory.NFT.value, "superrare", "Digital art", mcap_rank=405),
    "RARI": Asset("RARI", "Rarible", AssetType.CRYPTO, CryptoCategory.NFT.value, "rarible", "NFT platform", mcap_rank=415),

    # Stablecoins (for reference/comparison) - ranked by market cap
    "USDT": Asset("USDT", "Tether", AssetType.CRYPTO, CryptoCategory.STABLECOIN.value, "tether", "USD-pegged stablecoin", mcap_rank=6),
    "USDC": Asset("USDC", "USD Coin", AssetType.CRYPTO, CryptoCategory.STABLECOIN.value, "usd-coin", "Circle stablecoin", mcap_rank=9),
    "DAI": Asset("DAI", "Dai", AssetType.CRYPTO, CryptoCategory.STABLECOIN.value, "dai", "Decentralized stablecoin", mcap_rank=49),
    "FRAX": Asset("FRAX", "Frax", AssetType.CRYPTO, CryptoCategory.STABLECOIN.value, "frax", "Algorithmic stablecoin", mcap_rank=212),
    "TUSD": Asset("TUSD", "TrueUSD", AssetType.CRYPTO, CryptoCategory.STABLECOIN.value, "true-usd", "Regulated stablecoin", mcap_rank=248),
    "USDP": Asset("USDP", "Pax Dollar", AssetType.CRYPTO, CryptoCategory.STABLECOIN.value, "paxos-standard", "Paxos stablecoin", mcap_rank=282),
    "GUSD": Asset("GUSD", "Gemini Dollar", AssetType.CRYPTO, CryptoCategory.STABLECOIN.value, "gemini-dollar", "Gemini stablecoin", mcap_rank=435),
    "PYUSD": Asset("PYUSD", "PayPal USD", AssetType.CRYPTO, CryptoCategory.STABLECOIN.value, "paypal-usd", "PayPal stablecoin", mcap_rank=166),
    "FDUSD": Asset("FDUSD", "First Digital USD", AssetType.CRYPTO, CryptoCategory.STABLECOIN.value, "first-digital-usd", "First Digital stablecoin", mcap_rank=73),
    "USDE": Asset("USDE", "USDe", AssetType.CRYPTO, CryptoCategory.STABLECOIN.value, "ethena-usde", "Ethena synthetic dollar", mcap_rank=69),
}

# ============================================================================
# COMPREHENSIVE STOCK REGISTRY
# ============================================================================

STOCK_ASSETS: Dict[str, Asset] = {
    # Mega-cap Tech (FAANG+)
    "AAPL": Asset("AAPL", "Apple Inc.", AssetType.STOCK, StockCategory.TECH.value, description="Consumer electronics"),
    "MSFT": Asset("MSFT", "Microsoft Corporation", AssetType.STOCK, StockCategory.TECH.value, description="Software & cloud"),
    "GOOGL": Asset("GOOGL", "Alphabet Inc. (Class A)", AssetType.STOCK, StockCategory.TECH.value, description="Search & advertising"),
    "GOOG": Asset("GOOG", "Alphabet Inc. (Class C)", AssetType.STOCK, StockCategory.TECH.value, description="Search & advertising"),
    "AMZN": Asset("AMZN", "Amazon.com Inc.", AssetType.STOCK, StockCategory.TECH.value, description="E-commerce & cloud"),
    "META": Asset("META", "Meta Platforms Inc.", AssetType.STOCK, StockCategory.TECH.value, description="Social media"),
    "NVDA": Asset("NVDA", "NVIDIA Corporation", AssetType.STOCK, StockCategory.TECH.value, description="GPU & AI chips"),
    "TSLA": Asset("TSLA", "Tesla Inc.", AssetType.STOCK, StockCategory.TECH.value, description="Electric vehicles"),
    "TSM": Asset("TSM", "Taiwan Semiconductor", AssetType.STOCK, StockCategory.TECH.value, description="Chip manufacturing"),
    "AVGO": Asset("AVGO", "Broadcom Inc.", AssetType.STOCK, StockCategory.TECH.value, description="Semiconductors"),
    "ORCL": Asset("ORCL", "Oracle Corporation", AssetType.STOCK, StockCategory.TECH.value, description="Enterprise software"),
    "ADBE": Asset("ADBE", "Adobe Inc.", AssetType.STOCK, StockCategory.TECH.value, description="Creative software"),
    "CRM": Asset("CRM", "Salesforce Inc.", AssetType.STOCK, StockCategory.TECH.value, description="CRM software"),
    "CSCO": Asset("CSCO", "Cisco Systems Inc.", AssetType.STOCK, StockCategory.TECH.value, description="Networking"),
    "INTC": Asset("INTC", "Intel Corporation", AssetType.STOCK, StockCategory.TECH.value, description="Semiconductors"),
    "AMD": Asset("AMD", "Advanced Micro Devices", AssetType.STOCK, StockCategory.TECH.value, description="CPU & GPU chips"),
    "QCOM": Asset("QCOM", "Qualcomm Inc.", AssetType.STOCK, StockCategory.TECH.value, description="Mobile chips"),
    "TXN": Asset("TXN", "Texas Instruments", AssetType.STOCK, StockCategory.TECH.value, description="Semiconductors"),
    "NOW": Asset("NOW", "ServiceNow Inc.", AssetType.STOCK, StockCategory.TECH.value, description="IT workflows"),
    "IBM": Asset("IBM", "IBM Corporation", AssetType.STOCK, StockCategory.TECH.value, description="IT services"),
    "INTU": Asset("INTU", "Intuit Inc.", AssetType.STOCK, StockCategory.TECH.value, description="Financial software"),
    "SHOP": Asset("SHOP", "Shopify Inc.", AssetType.STOCK, StockCategory.TECH.value, description="E-commerce platform"),
    "SQ": Asset("SQ", "Block Inc.", AssetType.STOCK, StockCategory.TECH.value, description="Payment processing"),
    "PYPL": Asset("PYPL", "PayPal Holdings", AssetType.STOCK, StockCategory.TECH.value, description="Digital payments"),
    "UBER": Asset("UBER", "Uber Technologies", AssetType.STOCK, StockCategory.TECH.value, description="Ride-hailing"),
    "ABNB": Asset("ABNB", "Airbnb Inc.", AssetType.STOCK, StockCategory.TECH.value, description="Travel platform"),
    "SNOW": Asset("SNOW", "Snowflake Inc.", AssetType.STOCK, StockCategory.TECH.value, description="Data cloud"),
    "PLTR": Asset("PLTR", "Palantir Technologies", AssetType.STOCK, StockCategory.TECH.value, description="Data analytics"),
    "NET": Asset("NET", "Cloudflare Inc.", AssetType.STOCK, StockCategory.TECH.value, description="CDN & security"),
    "DDOG": Asset("DDOG", "Datadog Inc.", AssetType.STOCK, StockCategory.TECH.value, description="Cloud monitoring"),
    "CRWD": Asset("CRWD", "CrowdStrike Holdings", AssetType.STOCK, StockCategory.TECH.value, description="Cybersecurity"),
    "ZS": Asset("ZS", "Zscaler Inc.", AssetType.STOCK, StockCategory.TECH.value, description="Cloud security"),
    "PANW": Asset("PANW", "Palo Alto Networks", AssetType.STOCK, StockCategory.TECH.value, description="Cybersecurity"),
    "MDB": Asset("MDB", "MongoDB Inc.", AssetType.STOCK, StockCategory.TECH.value, description="Database"),
    "COIN": Asset("COIN", "Coinbase Global", AssetType.STOCK, StockCategory.TECH.value, description="Crypto exchange"),
    "MSTR": Asset("MSTR", "MicroStrategy Inc.", AssetType.STOCK, StockCategory.TECH.value, description="Bitcoin treasury"),
    "DELL": Asset("DELL", "Dell Technologies", AssetType.STOCK, StockCategory.TECH.value, description="Computer hardware"),
    "HPQ": Asset("HPQ", "HP Inc.", AssetType.STOCK, StockCategory.TECH.value, description="PCs & printers"),
    "HPE": Asset("HPE", "Hewlett Packard Enterprise", AssetType.STOCK, StockCategory.TECH.value, description="Enterprise IT"),
    "ANET": Asset("ANET", "Arista Networks", AssetType.STOCK, StockCategory.TECH.value, description="Cloud networking"),
    "MU": Asset("MU", "Micron Technology", AssetType.STOCK, StockCategory.TECH.value, description="Memory chips"),
    "MRVL": Asset("MRVL", "Marvell Technology", AssetType.STOCK, StockCategory.TECH.value, description="Semiconductors"),
    "NXPI": Asset("NXPI", "NXP Semiconductors", AssetType.STOCK, StockCategory.TECH.value, description="Auto chips"),
    "ADI": Asset("ADI", "Analog Devices", AssetType.STOCK, StockCategory.TECH.value, description="Analog semiconductors"),
    "LRCX": Asset("LRCX", "Lam Research", AssetType.STOCK, StockCategory.TECH.value, description="Chip equipment"),
    "KLAC": Asset("KLAC", "KLA Corporation", AssetType.STOCK, StockCategory.TECH.value, description="Chip equipment"),
    "AMAT": Asset("AMAT", "Applied Materials", AssetType.STOCK, StockCategory.TECH.value, description="Chip equipment"),
    "ASML": Asset("ASML", "ASML Holding", AssetType.STOCK, StockCategory.TECH.value, description="Chip lithography"),
    "ARM": Asset("ARM", "Arm Holdings", AssetType.STOCK, StockCategory.TECH.value, description="Chip IP licensing"),
    "SMCI": Asset("SMCI", "Super Micro Computer", AssetType.STOCK, StockCategory.TECH.value, description="Server systems"),
    "AI": Asset("AI", "C3.ai Inc.", AssetType.STOCK, StockCategory.TECH.value, description="Enterprise AI"),
    "PATH": Asset("PATH", "UiPath Inc.", AssetType.STOCK, StockCategory.TECH.value, description="RPA software"),
    "OKTA": Asset("OKTA", "Okta Inc.", AssetType.STOCK, StockCategory.TECH.value, description="Identity management"),
    "ZM": Asset("ZM", "Zoom Video Communications", AssetType.STOCK, StockCategory.TECH.value, description="Video conferencing"),
    "TWLO": Asset("TWLO", "Twilio Inc.", AssetType.STOCK, StockCategory.TECH.value, description="Cloud communications"),
    "SPLK": Asset("SPLK", "Splunk Inc.", AssetType.STOCK, StockCategory.TECH.value, description="Data platform"),
    "WDAY": Asset("WDAY", "Workday Inc.", AssetType.STOCK, StockCategory.TECH.value, description="HR software"),
    "TEAM": Asset("TEAM", "Atlassian Corporation", AssetType.STOCK, StockCategory.TECH.value, description="Collaboration software"),
    "DOCU": Asset("DOCU", "DocuSign Inc.", AssetType.STOCK, StockCategory.TECH.value, description="E-signatures"),
    "DBX": Asset("DBX", "Dropbox Inc.", AssetType.STOCK, StockCategory.TECH.value, description="Cloud storage"),
    "ESTC": Asset("ESTC", "Elastic N.V.", AssetType.STOCK, StockCategory.TECH.value, description="Search & analytics"),
    "U": Asset("U", "Unity Software", AssetType.STOCK, StockCategory.TECH.value, description="Game engine"),
    "RBLX": Asset("RBLX", "Roblox Corporation", AssetType.STOCK, StockCategory.TECH.value, description="Gaming platform"),
    "EA": Asset("EA", "Electronic Arts", AssetType.STOCK, StockCategory.TECH.value, description="Video games"),
    "TTWO": Asset("TTWO", "Take-Two Interactive", AssetType.STOCK, StockCategory.TECH.value, description="Video games"),
    "ATVI": Asset("ATVI", "Activision Blizzard", AssetType.STOCK, StockCategory.TECH.value, description="Video games"),

    # Finance
    "JPM": Asset("JPM", "JPMorgan Chase", AssetType.STOCK, StockCategory.FINANCE.value, description="Banking"),
    "BAC": Asset("BAC", "Bank of America", AssetType.STOCK, StockCategory.FINANCE.value, description="Banking"),
    "WFC": Asset("WFC", "Wells Fargo", AssetType.STOCK, StockCategory.FINANCE.value, description="Banking"),
    "GS": Asset("GS", "Goldman Sachs", AssetType.STOCK, StockCategory.FINANCE.value, description="Investment banking"),
    "MS": Asset("MS", "Morgan Stanley", AssetType.STOCK, StockCategory.FINANCE.value, description="Investment banking"),
    "C": Asset("C", "Citigroup Inc.", AssetType.STOCK, StockCategory.FINANCE.value, description="Banking"),
    "BLK": Asset("BLK", "BlackRock Inc.", AssetType.STOCK, StockCategory.FINANCE.value, description="Asset management"),
    "SCHW": Asset("SCHW", "Charles Schwab", AssetType.STOCK, StockCategory.FINANCE.value, description="Brokerage"),
    "AXP": Asset("AXP", "American Express", AssetType.STOCK, StockCategory.FINANCE.value, description="Credit cards"),
    "V": Asset("V", "Visa Inc.", AssetType.STOCK, StockCategory.FINANCE.value, description="Payment network"),
    "MA": Asset("MA", "Mastercard Inc.", AssetType.STOCK, StockCategory.FINANCE.value, description="Payment network"),
    "SPGI": Asset("SPGI", "S&P Global", AssetType.STOCK, StockCategory.FINANCE.value, description="Financial data"),
    "MCO": Asset("MCO", "Moody's Corporation", AssetType.STOCK, StockCategory.FINANCE.value, description="Credit ratings"),
    "CME": Asset("CME", "CME Group", AssetType.STOCK, StockCategory.FINANCE.value, description="Derivatives exchange"),
    "ICE": Asset("ICE", "Intercontinental Exchange", AssetType.STOCK, StockCategory.FINANCE.value, description="Exchanges"),
    "USB": Asset("USB", "U.S. Bancorp", AssetType.STOCK, StockCategory.FINANCE.value, description="Banking"),
    "PNC": Asset("PNC", "PNC Financial", AssetType.STOCK, StockCategory.FINANCE.value, description="Banking"),
    "TFC": Asset("TFC", "Truist Financial", AssetType.STOCK, StockCategory.FINANCE.value, description="Banking"),
    "COF": Asset("COF", "Capital One", AssetType.STOCK, StockCategory.FINANCE.value, description="Credit cards"),
    "BX": Asset("BX", "Blackstone Inc.", AssetType.STOCK, StockCategory.FINANCE.value, description="Private equity"),
    "KKR": Asset("KKR", "KKR & Co. Inc.", AssetType.STOCK, StockCategory.FINANCE.value, description="Private equity"),
    "APO": Asset("APO", "Apollo Global", AssetType.STOCK, StockCategory.FINANCE.value, description="Alternative investments"),
    "HOOD": Asset("HOOD", "Robinhood Markets", AssetType.STOCK, StockCategory.FINANCE.value, description="Trading platform"),
    "SOFI": Asset("SOFI", "SoFi Technologies", AssetType.STOCK, StockCategory.FINANCE.value, description="Fintech"),
    "AFRM": Asset("AFRM", "Affirm Holdings", AssetType.STOCK, StockCategory.FINANCE.value, description="BNPL"),
    "NU": Asset("NU", "Nu Holdings", AssetType.STOCK, StockCategory.FINANCE.value, description="Digital banking"),

    # Healthcare
    "UNH": Asset("UNH", "UnitedHealth Group", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Health insurance"),
    "JNJ": Asset("JNJ", "Johnson & Johnson", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Pharma & devices"),
    "LLY": Asset("LLY", "Eli Lilly", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Pharmaceuticals"),
    "PFE": Asset("PFE", "Pfizer Inc.", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Pharmaceuticals"),
    "MRK": Asset("MRK", "Merck & Co.", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Pharmaceuticals"),
    "ABBV": Asset("ABBV", "AbbVie Inc.", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Pharmaceuticals"),
    "TMO": Asset("TMO", "Thermo Fisher Scientific", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Lab equipment"),
    "ABT": Asset("ABT", "Abbott Laboratories", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Medical devices"),
    "DHR": Asset("DHR", "Danaher Corporation", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Life sciences"),
    "BMY": Asset("BMY", "Bristol-Myers Squibb", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Pharmaceuticals"),
    "AMGN": Asset("AMGN", "Amgen Inc.", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Biotechnology"),
    "GILD": Asset("GILD", "Gilead Sciences", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Biotechnology"),
    "VRTX": Asset("VRTX", "Vertex Pharmaceuticals", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Biotechnology"),
    "REGN": Asset("REGN", "Regeneron Pharmaceuticals", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Biotechnology"),
    "BIIB": Asset("BIIB", "Biogen Inc.", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Biotechnology"),
    "MRNA": Asset("MRNA", "Moderna Inc.", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="mRNA therapeutics"),
    "ZTS": Asset("ZTS", "Zoetis Inc.", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Animal health"),
    "MDT": Asset("MDT", "Medtronic plc", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Medical devices"),
    "SYK": Asset("SYK", "Stryker Corporation", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Medical devices"),
    "ISRG": Asset("ISRG", "Intuitive Surgical", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Surgical robotics"),
    "ELV": Asset("ELV", "Elevance Health", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Health insurance"),
    "CI": Asset("CI", "Cigna Group", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Health insurance"),
    "CVS": Asset("CVS", "CVS Health", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Healthcare retail"),
    "HUM": Asset("HUM", "Humana Inc.", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Health insurance"),
    "HCA": Asset("HCA", "HCA Healthcare", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Hospitals"),
    "IQV": Asset("IQV", "IQVIA Holdings", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Health data"),
    "BSX": Asset("BSX", "Boston Scientific", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Medical devices"),
    "EW": Asset("EW", "Edwards Lifesciences", AssetType.STOCK, StockCategory.HEALTHCARE.value, description="Heart valves"),

    # Consumer
    "PG": Asset("PG", "Procter & Gamble", AssetType.STOCK, StockCategory.CONSUMER.value, description="Consumer goods"),
    "KO": Asset("KO", "Coca-Cola Company", AssetType.STOCK, StockCategory.CONSUMER.value, description="Beverages"),
    "PEP": Asset("PEP", "PepsiCo Inc.", AssetType.STOCK, StockCategory.CONSUMER.value, description="Beverages & snacks"),
    "WMT": Asset("WMT", "Walmart Inc.", AssetType.STOCK, StockCategory.CONSUMER.value, description="Retail"),
    "COST": Asset("COST", "Costco Wholesale", AssetType.STOCK, StockCategory.CONSUMER.value, description="Wholesale retail"),
    "TGT": Asset("TGT", "Target Corporation", AssetType.STOCK, StockCategory.CONSUMER.value, description="Retail"),
    "HD": Asset("HD", "Home Depot", AssetType.STOCK, StockCategory.CONSUMER.value, description="Home improvement"),
    "LOW": Asset("LOW", "Lowe's Companies", AssetType.STOCK, StockCategory.CONSUMER.value, description="Home improvement"),
    "MCD": Asset("MCD", "McDonald's Corporation", AssetType.STOCK, StockCategory.CONSUMER.value, description="Fast food"),
    "SBUX": Asset("SBUX", "Starbucks Corporation", AssetType.STOCK, StockCategory.CONSUMER.value, description="Coffee"),
    "NKE": Asset("NKE", "Nike Inc.", AssetType.STOCK, StockCategory.CONSUMER.value, description="Athletic apparel"),
    "LULU": Asset("LULU", "Lululemon Athletica", AssetType.STOCK, StockCategory.CONSUMER.value, description="Athletic apparel"),
    "DIS": Asset("DIS", "Walt Disney Company", AssetType.STOCK, StockCategory.CONSUMER.value, description="Entertainment"),
    "NFLX": Asset("NFLX", "Netflix Inc.", AssetType.STOCK, StockCategory.CONSUMER.value, description="Streaming"),
    "CMCSA": Asset("CMCSA", "Comcast Corporation", AssetType.STOCK, StockCategory.CONSUMER.value, description="Media & telecom"),
    "PM": Asset("PM", "Philip Morris International", AssetType.STOCK, StockCategory.CONSUMER.value, description="Tobacco"),
    "MO": Asset("MO", "Altria Group", AssetType.STOCK, StockCategory.CONSUMER.value, description="Tobacco"),
    "CL": Asset("CL", "Colgate-Palmolive", AssetType.STOCK, StockCategory.CONSUMER.value, description="Consumer goods"),
    "EL": Asset("EL", "Estée Lauder", AssetType.STOCK, StockCategory.CONSUMER.value, description="Cosmetics"),
    "GM": Asset("GM", "General Motors", AssetType.STOCK, StockCategory.CONSUMER.value, description="Automobiles"),
    "F": Asset("F", "Ford Motor Company", AssetType.STOCK, StockCategory.CONSUMER.value, description="Automobiles"),
    "RIVN": Asset("RIVN", "Rivian Automotive", AssetType.STOCK, StockCategory.CONSUMER.value, description="Electric vehicles"),
    "LCID": Asset("LCID", "Lucid Group", AssetType.STOCK, StockCategory.CONSUMER.value, description="Electric vehicles"),

    # Energy
    "XOM": Asset("XOM", "Exxon Mobil", AssetType.STOCK, StockCategory.ENERGY.value, description="Oil & gas"),
    "CVX": Asset("CVX", "Chevron Corporation", AssetType.STOCK, StockCategory.ENERGY.value, description="Oil & gas"),
    "COP": Asset("COP", "ConocoPhillips", AssetType.STOCK, StockCategory.ENERGY.value, description="Oil & gas"),
    "EOG": Asset("EOG", "EOG Resources", AssetType.STOCK, StockCategory.ENERGY.value, description="Oil & gas"),
    "SLB": Asset("SLB", "Schlumberger", AssetType.STOCK, StockCategory.ENERGY.value, description="Oil services"),
    "OXY": Asset("OXY", "Occidental Petroleum", AssetType.STOCK, StockCategory.ENERGY.value, description="Oil & gas"),
    "DVN": Asset("DVN", "Devon Energy", AssetType.STOCK, StockCategory.ENERGY.value, description="Oil & gas"),
    "HES": Asset("HES", "Hess Corporation", AssetType.STOCK, StockCategory.ENERGY.value, description="Oil & gas"),
    "PSX": Asset("PSX", "Phillips 66", AssetType.STOCK, StockCategory.ENERGY.value, description="Refining"),
    "VLO": Asset("VLO", "Valero Energy", AssetType.STOCK, StockCategory.ENERGY.value, description="Refining"),
    "MPC": Asset("MPC", "Marathon Petroleum", AssetType.STOCK, StockCategory.ENERGY.value, description="Refining"),
    "NEE": Asset("NEE", "NextEra Energy", AssetType.STOCK, StockCategory.ENERGY.value, description="Renewable energy"),
    "FSLR": Asset("FSLR", "First Solar", AssetType.STOCK, StockCategory.ENERGY.value, description="Solar energy"),
    "ENPH": Asset("ENPH", "Enphase Energy", AssetType.STOCK, StockCategory.ENERGY.value, description="Solar technology"),

    # Industrial
    "CAT": Asset("CAT", "Caterpillar Inc.", AssetType.STOCK, StockCategory.INDUSTRIAL.value, description="Heavy machinery"),
    "DE": Asset("DE", "Deere & Company", AssetType.STOCK, StockCategory.INDUSTRIAL.value, description="Agricultural equipment"),
    "BA": Asset("BA", "Boeing Company", AssetType.STOCK, StockCategory.INDUSTRIAL.value, description="Aerospace"),
    "LMT": Asset("LMT", "Lockheed Martin", AssetType.STOCK, StockCategory.INDUSTRIAL.value, description="Defense"),
    "RTX": Asset("RTX", "RTX Corporation", AssetType.STOCK, StockCategory.INDUSTRIAL.value, description="Aerospace & defense"),
    "NOC": Asset("NOC", "Northrop Grumman", AssetType.STOCK, StockCategory.INDUSTRIAL.value, description="Defense"),
    "GD": Asset("GD", "General Dynamics", AssetType.STOCK, StockCategory.INDUSTRIAL.value, description="Defense"),
    "GE": Asset("GE", "GE Aerospace", AssetType.STOCK, StockCategory.INDUSTRIAL.value, description="Aerospace"),
    "HON": Asset("HON", "Honeywell International", AssetType.STOCK, StockCategory.INDUSTRIAL.value, description="Conglomerate"),
    "MMM": Asset("MMM", "3M Company", AssetType.STOCK, StockCategory.INDUSTRIAL.value, description="Diversified industrial"),
    "UPS": Asset("UPS", "United Parcel Service", AssetType.STOCK, StockCategory.INDUSTRIAL.value, description="Logistics"),
    "FDX": Asset("FDX", "FedEx Corporation", AssetType.STOCK, StockCategory.INDUSTRIAL.value, description="Logistics"),
    "UNP": Asset("UNP", "Union Pacific", AssetType.STOCK, StockCategory.INDUSTRIAL.value, description="Railroad"),
    "CSX": Asset("CSX", "CSX Corporation", AssetType.STOCK, StockCategory.INDUSTRIAL.value, description="Railroad"),
    "NSC": Asset("NSC", "Norfolk Southern", AssetType.STOCK, StockCategory.INDUSTRIAL.value, description="Railroad"),
    "WM": Asset("WM", "Waste Management", AssetType.STOCK, StockCategory.INDUSTRIAL.value, description="Waste services"),
    "EMR": Asset("EMR", "Emerson Electric", AssetType.STOCK, StockCategory.INDUSTRIAL.value, description="Industrial technology"),
    "ETN": Asset("ETN", "Eaton Corporation", AssetType.STOCK, StockCategory.INDUSTRIAL.value, description="Power management"),
    "ITW": Asset("ITW", "Illinois Tool Works", AssetType.STOCK, StockCategory.INDUSTRIAL.value, description="Industrial products"),
    "PH": Asset("PH", "Parker-Hannifin", AssetType.STOCK, StockCategory.INDUSTRIAL.value, description="Motion & control"),
    "ROK": Asset("ROK", "Rockwell Automation", AssetType.STOCK, StockCategory.INDUSTRIAL.value, description="Industrial automation"),

    # Communication
    "T": Asset("T", "AT&T Inc.", AssetType.STOCK, StockCategory.COMMUNICATION.value, description="Telecom"),
    "VZ": Asset("VZ", "Verizon Communications", AssetType.STOCK, StockCategory.COMMUNICATION.value, description="Telecom"),
    "TMUS": Asset("TMUS", "T-Mobile US", AssetType.STOCK, StockCategory.COMMUNICATION.value, description="Wireless"),
    "CHTR": Asset("CHTR", "Charter Communications", AssetType.STOCK, StockCategory.COMMUNICATION.value, description="Cable"),
    "WBD": Asset("WBD", "Warner Bros. Discovery", AssetType.STOCK, StockCategory.COMMUNICATION.value, description="Media"),
    "PARA": Asset("PARA", "Paramount Global", AssetType.STOCK, StockCategory.COMMUNICATION.value, description="Media"),
    "FOX": Asset("FOX", "Fox Corporation", AssetType.STOCK, StockCategory.COMMUNICATION.value, description="Media"),
    "FOXA": Asset("FOXA", "Fox Corporation (Class A)", AssetType.STOCK, StockCategory.COMMUNICATION.value, description="Media"),
    "SPOT": Asset("SPOT", "Spotify Technology", AssetType.STOCK, StockCategory.COMMUNICATION.value, description="Music streaming"),
    "SNAP": Asset("SNAP", "Snap Inc.", AssetType.STOCK, StockCategory.COMMUNICATION.value, description="Social media"),
    "PINS": Asset("PINS", "Pinterest Inc.", AssetType.STOCK, StockCategory.COMMUNICATION.value, description="Social media"),
    "MTCH": Asset("MTCH", "Match Group", AssetType.STOCK, StockCategory.COMMUNICATION.value, description="Dating apps"),
    "ROKU": Asset("ROKU", "Roku Inc.", AssetType.STOCK, StockCategory.COMMUNICATION.value, description="Streaming devices"),

    # Materials
    "LIN": Asset("LIN", "Linde plc", AssetType.STOCK, StockCategory.MATERIALS.value, description="Industrial gases"),
    "APD": Asset("APD", "Air Products", AssetType.STOCK, StockCategory.MATERIALS.value, description="Industrial gases"),
    "SHW": Asset("SHW", "Sherwin-Williams", AssetType.STOCK, StockCategory.MATERIALS.value, description="Paints"),
    "ECL": Asset("ECL", "Ecolab Inc.", AssetType.STOCK, StockCategory.MATERIALS.value, description="Water & hygiene"),
    "FCX": Asset("FCX", "Freeport-McMoRan", AssetType.STOCK, StockCategory.MATERIALS.value, description="Copper mining"),
    "NEM": Asset("NEM", "Newmont Corporation", AssetType.STOCK, StockCategory.MATERIALS.value, description="Gold mining"),
    "NUE": Asset("NUE", "Nucor Corporation", AssetType.STOCK, StockCategory.MATERIALS.value, description="Steel"),
    "STLD": Asset("STLD", "Steel Dynamics", AssetType.STOCK, StockCategory.MATERIALS.value, description="Steel"),
    "CLF": Asset("CLF", "Cleveland-Cliffs", AssetType.STOCK, StockCategory.MATERIALS.value, description="Iron ore & steel"),
    "AA": Asset("AA", "Alcoa Corporation", AssetType.STOCK, StockCategory.MATERIALS.value, description="Aluminum"),
    "X": Asset("X", "United States Steel", AssetType.STOCK, StockCategory.MATERIALS.value, description="Steel"),
    "RIO": Asset("RIO", "Rio Tinto", AssetType.STOCK, StockCategory.MATERIALS.value, description="Mining"),
    "BHP": Asset("BHP", "BHP Group", AssetType.STOCK, StockCategory.MATERIALS.value, description="Mining"),
    "VALE": Asset("VALE", "Vale S.A.", AssetType.STOCK, StockCategory.MATERIALS.value, description="Mining"),

    # ETFs
    "SPY": Asset("SPY", "SPDR S&P 500 ETF", AssetType.STOCK, StockCategory.ETF.value, description="S&P 500 tracker"),
    "QQQ": Asset("QQQ", "Invesco QQQ Trust", AssetType.STOCK, StockCategory.ETF.value, description="Nasdaq-100 tracker"),
    "IWM": Asset("IWM", "iShares Russell 2000 ETF", AssetType.STOCK, StockCategory.ETF.value, description="Small-cap tracker"),
    "DIA": Asset("DIA", "SPDR Dow Jones ETF", AssetType.STOCK, StockCategory.ETF.value, description="Dow 30 tracker"),
    "VTI": Asset("VTI", "Vanguard Total Stock", AssetType.STOCK, StockCategory.ETF.value, description="Total market"),
    "VOO": Asset("VOO", "Vanguard S&P 500 ETF", AssetType.STOCK, StockCategory.ETF.value, description="S&P 500 tracker"),
    "VXX": Asset("VXX", "iPath VIX Short-Term", AssetType.STOCK, StockCategory.ETF.value, description="Volatility tracker"),
    "GLD": Asset("GLD", "SPDR Gold Trust", AssetType.STOCK, StockCategory.ETF.value, description="Gold tracker"),
    "SLV": Asset("SLV", "iShares Silver Trust", AssetType.STOCK, StockCategory.ETF.value, description="Silver tracker"),
    "USO": Asset("USO", "United States Oil Fund", AssetType.STOCK, StockCategory.ETF.value, description="Oil tracker"),
    "ARKK": Asset("ARKK", "ARK Innovation ETF", AssetType.STOCK, StockCategory.ETF.value, description="Disruptive innovation"),
    "ARKW": Asset("ARKW", "ARK Next Generation Internet", AssetType.STOCK, StockCategory.ETF.value, description="Internet innovation"),
    "ARKG": Asset("ARKG", "ARK Genomic Revolution", AssetType.STOCK, StockCategory.ETF.value, description="Genomics"),
    "XLF": Asset("XLF", "Financial Select Sector SPDR", AssetType.STOCK, StockCategory.ETF.value, description="Financials sector"),
    "XLK": Asset("XLK", "Technology Select Sector SPDR", AssetType.STOCK, StockCategory.ETF.value, description="Technology sector"),
    "XLE": Asset("XLE", "Energy Select Sector SPDR", AssetType.STOCK, StockCategory.ETF.value, description="Energy sector"),
    "XLV": Asset("XLV", "Health Care Select Sector SPDR", AssetType.STOCK, StockCategory.ETF.value, description="Healthcare sector"),
    "XLI": Asset("XLI", "Industrial Select Sector SPDR", AssetType.STOCK, StockCategory.ETF.value, description="Industrials sector"),
    "XLP": Asset("XLP", "Consumer Staples Select SPDR", AssetType.STOCK, StockCategory.ETF.value, description="Consumer staples"),
    "XLY": Asset("XLY", "Consumer Discretionary SPDR", AssetType.STOCK, StockCategory.ETF.value, description="Consumer discretionary"),
    "SOXL": Asset("SOXL", "Direxion Semiconductor Bull 3x", AssetType.STOCK, StockCategory.ETF.value, description="Leveraged semis"),
    "TQQQ": Asset("TQQQ", "ProShares UltraPro QQQ", AssetType.STOCK, StockCategory.ETF.value, description="3x Nasdaq-100"),
    "SQQQ": Asset("SQQQ", "ProShares UltraPro Short QQQ", AssetType.STOCK, StockCategory.ETF.value, description="-3x Nasdaq-100"),
    "UVXY": Asset("UVXY", "ProShares Ultra VIX Short-Term", AssetType.STOCK, StockCategory.ETF.value, description="1.5x VIX"),
    "TLT": Asset("TLT", "iShares 20+ Year Treasury ETF", AssetType.STOCK, StockCategory.ETF.value, description="Long-term bonds"),
    "HYG": Asset("HYG", "iShares High Yield Corporate", AssetType.STOCK, StockCategory.ETF.value, description="High-yield bonds"),
    "IBIT": Asset("IBIT", "iShares Bitcoin Trust", AssetType.STOCK, StockCategory.ETF.value, description="Bitcoin ETF"),
    "FBTC": Asset("FBTC", "Fidelity Wise Origin Bitcoin", AssetType.STOCK, StockCategory.ETF.value, description="Bitcoin ETF"),
    "GBTC": Asset("GBTC", "Grayscale Bitcoin Trust", AssetType.STOCK, StockCategory.ETF.value, description="Bitcoin trust"),
    "ETHE": Asset("ETHE", "Grayscale Ethereum Trust", AssetType.STOCK, StockCategory.ETF.value, description="Ethereum trust"),
}


# Combined asset registry
ALL_ASSETS: Dict[str, Asset] = {**CRYPTO_ASSETS, **STOCK_ASSETS}


def search_assets(
    query: str,
    asset_type: Optional[AssetType] = None,
    category: Optional[str] = None,
    limit: int = 20,
    sort_by_mcap: bool = True
) -> List[Asset]:
    """
    Search assets by symbol or name.

    Args:
        query: Search query (symbol or name)
        asset_type: Filter by crypto or stock
        category: Filter by category
        limit: Maximum results to return
        sort_by_mcap: Sort crypto by market cap rank (default True)

    Returns:
        List of matching assets
    """
    query = query.upper().strip()
    results = []

    # Select asset pool
    if asset_type == AssetType.CRYPTO:
        pool = CRYPTO_ASSETS
    elif asset_type == AssetType.STOCK:
        pool = STOCK_ASSETS
    else:
        pool = ALL_ASSETS

    for symbol, asset in pool.items():
        # Filter by category if specified
        if category and asset.category != category:
            continue

        # Match by symbol (exact or prefix)
        if symbol.startswith(query):
            results.append((0, asset))  # Exact match priority
        # Match by name
        elif query in asset.name.upper():
            results.append((1, asset))  # Name match lower priority

    # Sort by priority, then by market cap (for crypto) or alphabetically (for stock)
    if sort_by_mcap and asset_type == AssetType.CRYPTO:
        # For crypto: sort by match priority, then by mcap_rank (lower = higher mcap)
        results.sort(key=lambda x: (x[0], x[1].mcap_rank or 9999))
    else:
        # For stocks or mixed: sort by priority then alphabetically
        results.sort(key=lambda x: (x[0], x[1].symbol))

    return [asset for _, asset in results[:limit]]


def list_assets(
    asset_type: Optional[AssetType] = None,
    category: Optional[str] = None,
    limit: int = 50,
    sort_by_mcap: bool = True
) -> List[Asset]:
    """
    List assets with optional filtering and sorting.

    Args:
        asset_type: Filter by crypto or stock
        category: Filter by category
        limit: Maximum results to return
        sort_by_mcap: Sort crypto by market cap rank (default True)

    Returns:
        List of assets
    """
    # Select asset pool
    if asset_type == AssetType.CRYPTO:
        pool = CRYPTO_ASSETS
    elif asset_type == AssetType.STOCK:
        pool = STOCK_ASSETS
    else:
        pool = ALL_ASSETS

    assets = list(pool.values())

    # Filter by category if specified
    if category:
        assets = [a for a in assets if a.category == category]

    # Sort by market cap for crypto, alphabetically for stocks
    if sort_by_mcap and asset_type == AssetType.CRYPTO:
        assets.sort(key=lambda a: a.mcap_rank or 9999)
    else:
        assets.sort(key=lambda a: a.symbol)

    return assets[:limit]


def get_asset(symbol: str, asset_type: Optional[AssetType] = None) -> Optional[Asset]:
    """Get asset by symbol."""
    symbol = symbol.upper().strip()

    if asset_type == AssetType.CRYPTO:
        return CRYPTO_ASSETS.get(symbol)
    elif asset_type == AssetType.STOCK:
        return STOCK_ASSETS.get(symbol)

    # Try crypto first, then stock
    return CRYPTO_ASSETS.get(symbol) or STOCK_ASSETS.get(symbol)


def get_all_categories(asset_type: Optional[AssetType] = None) -> List[str]:
    """Get all available categories."""
    categories = set()

    if asset_type == AssetType.CRYPTO or asset_type is None:
        categories.update(c.value for c in CryptoCategory)

    if asset_type == AssetType.STOCK or asset_type is None:
        categories.update(c.value for c in StockCategory)

    return sorted(categories)


def get_coingecko_id(symbol: str) -> Optional[str]:
    """Get CoinGecko ID for a crypto symbol."""
    asset = CRYPTO_ASSETS.get(symbol.upper())
    return asset.coingecko_id if asset else None


# Build reverse lookup for CoinGecko IDs
COINGECKO_ID_MAP: Dict[str, str] = {
    asset.coingecko_id: symbol
    for symbol, asset in CRYPTO_ASSETS.items()
    if asset.coingecko_id
}
