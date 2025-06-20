class BOSDetector:
    def __init__(self, candles):
        self.candles = candles  # List of dicts: [{"high": ..., "low": ..., "close": ..., "time": ...}, ...]

    def detect_bos(self):
        """
        Detects Break of Structure:
        - Bullish BOS: price closes above previous swing high
        - Bearish BOS: price closes below previous swing low
        Returns: list of BOS points with type and candle index
        """
        bos_events = []

        for i in range(3, len(self.candles)):
            prev_high = self.candles[i - 2]['high']
            prev_low = self.candles[i - 2]['low']
            curr_close = self.candles[i]['close']

            if curr_close > prev_high:
                bos_events.append({"type": "bullish", "index": i, "price": curr_close})
            elif curr_close < prev_low:
                bos_events.append({"type": "bearish", "index": i, "price": curr_close})

        return bos_events
