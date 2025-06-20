class StructureAnalyzer:
    def __init__(self, candles):
        self.candles = candles

    def detect_bos(self):
        bos_list = []
        for i in range(2, len(self.candles)):
            prev_high = self.candles[i - 2]['high']
            prev_low = self.candles[i - 2]['low']
            curr_close = self.candles[i]['close']

            if curr_close > prev_high:
                bos_list.append({"type": "bullish", "index": i, "price": curr_close})
            elif curr_close < prev_low:
                bos_list.append({"type": "bearish", "index": i, "price": curr_close})
        return bos_list

    def detect_choch(self):
        choch_list = []
        for i in range(2, len(self.candles)):
            prev = self.candles[i - 1]
            curr = self.candles[i]
            if curr['low'] < prev['low'] and curr['high'] < prev['high']:
                choch_list.append({"type": "bearish", "index": i, "price": curr['low']})
            elif curr['high'] > prev['high'] and curr['low'] > prev['low']:
                choch_list.append({"type": "bullish", "index": i, "price": curr['high']})
        return choch_list

    def detect_liquidity_sweep(self):
        sweeps = []
        for i in range(3, len(self.candles)):
            high_prev = self.candles[i - 3]['high']
            low_prev = self.candles[i - 3]['low']
            wick_high = self.candles[i]['high']
            wick_low = self.candles[i]['low']

            if wick_high > high_prev:
                sweeps.append({"type": "buy-side", "index": i, "price": wick_high})
            elif wick_low < low_prev:
                sweeps.append({"type": "sell-side", "index": i, "price": wick_low})
        return sweeps
