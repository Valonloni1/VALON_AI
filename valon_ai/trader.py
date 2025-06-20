from valon_ai.strategy import StrategyEngine

# 🔸 Disa të dhëna të simuluara për testim
mock_candles = [
    {"open": 100, "high": 110, "low": 95, "close": 108},
    {"open": 108, "high": 112, "low": 104, "close": 110},
    {"open": 110, "high": 115, "low": 109, "close": 111},
    {"open": 111, "high": 114, "low": 107, "close": 108},
    {"open": 108, "high": 109, "low": 100, "close": 102},
    {"open": 102, "high": 105, "low": 98, "close": 99},
    {"open": 99,  "high": 101, "low": 95, "close": 97},
]

# ✅ Tregti të hapura (lista bosh për simulim fillestar)
open_trades = []

# 🧠 Inicializo strategjinë
strategy = StrategyEngine(candles=mock_candles)

# 📊 Gjenero sinjale tregtie
signals = strategy.generate_signals(open_trades=open_trades)

# 📥 Printo sinjalet si të ishin tregti reale
for signal in signals:
    print("\n📌 Sinjal i ri tregtie:")
    print(f"Tipi:        {signal['type']}")
    print(f"Indeksi:     {signal['index']}")
    print(f"Çmimi:       {signal['price']}")
    print(f"Stop Loss:   {signal['stop_loss']}")
    print(f"Lot Size:    {signal['lot_size']}")
    print("🧪 [Simulim] Tregtia nuk u ekzekutua në MT5.\n")
