from valon_ai.strategy import StrategyEngine
from valon_ai.mt5_integration import MT5Client


class TradingBot:
    """Fetch candles from MT5 and run the strategy engine."""

    def __init__(self, symbol="XAUUSD", timeframe="M5"):
        self.symbol = symbol
        self.timeframe = timeframe
        self.mt5 = MT5Client()
        self.mt5.connect()

    def fetch_candles(self, count=100):
        return self.mt5.get_candles(symbol=self.symbol, timeframe=self.timeframe, count=count)

    def analyze_and_trade(self):
        candles = self.fetch_candles()
        strategy = StrategyEngine(candles)
        signals = strategy.generate_signals()

        if signals:
            last_signal = signals[-1]
            direction = last_signal["type"]

            if direction == "BUY":
                print("\U0001f535 BUY signal detected → executing long entry...")
                # self.mt5.buy(symbol=self.symbol, volume=0.1)
            elif direction == "SELL":
                print("\U0001f534 SELL signal detected → executing short entry...")
                # self.mt5.sell(symbol=self.symbol, volume=0.1)
        else:
            print("\U0001f7e1 No valid trade signal found.")

    def shutdown(self):
        self.mt5.shutdown()
