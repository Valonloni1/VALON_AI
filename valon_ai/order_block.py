class OrderBlockDetector:
    def __init__(self, candles):
        self.candles = candles

    def detect_bullish_ob(self):
        bullish_obs = []
        for i in range(2, len(self.candles) - 1):
            curr = self.candles[i]
            next_candle = self.candles[i + 1]
            if curr['close'] < curr['open'] and next_candle['close'] > curr['high']:
                bullish_obs.append({
                    "type": "bullish",
                    "index": i,
                    "open": curr['open'],
                    "low": curr['low'],
                    "high": curr['high'],
                    "close": curr['close']
                })
        return bullish_obs

    def detect_bearish_ob(self):
        bearish_obs = []
        for i in range(2, len(self.candles) - 1):
            curr = self.candles[i]
            next_candle = self.candles[i + 1]
            if curr['close'] > curr['open'] and next_candle['close'] < curr['low']:
                bearish_obs.append({
                    "type": "bearish",
                    "index": i,
                    "open": curr['open'],
                    "low": curr['low'],
                    "high": curr['high'],
                    "close": curr['close']
                })
        return bearish_obs
