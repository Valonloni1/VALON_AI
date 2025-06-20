"""Fair value gap detection utilities."""

from typing import List, Sequence, Dict, Any


class FVGDetector:
    """Detect fair value gaps in a sequence of OHLC candles."""

    def find(self, candles: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Return a list of detected fair value gaps.

        Each candle in ``candles`` must provide ``high`` and ``low`` values.
        A simple 3-candle pattern is used:
        - ``bullish`` gap when ``candles[i-2]['high'] < candles[i]['low']``.
        - ``bearish`` gap when ``candles[i-2]['low'] > candles[i]['high']``.

        The returned gaps include the indices of the candles that form the
        pattern and the price range of the gap.
        """
        gaps: List[Dict[str, Any]] = []
        for i in range(2, len(candles)):
            first = candles[i - 2]
            third = candles[i]

            if first['high'] < third['low']:
                gaps.append({
                    "type": "bullish",
                    "start_index": i - 2,
                    "end_index": i,
                    "gap_start": first['high'],
                    "gap_end": third['low'],
                })
            elif first['low'] > third['high']:
                gaps.append({
                    "type": "bearish",
                    "start_index": i - 2,
                    "end_index": i,
                    "gap_start": third['high'],
                    "gap_end": first['low'],
                })
        return gaps


# Backwards compatibility
FairValueGapFinder = FVGDetector
