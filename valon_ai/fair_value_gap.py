"""Fair value gap detection utilities."""

from typing import List, Sequence, Dict, Any


class FVGDetector:
    """Detect fair value gaps in a sequence of OHLC candles."""

    def __init__(self, candles: Sequence[Dict[str, Any]] | None = None) -> None:
        """Store optional candle data for later processing."""
        self.candles = list(candles) if candles is not None else []

    def find(
        self, candles: Sequence[Dict[str, Any]] | None = None
    ) -> List[Dict[str, Any]]:
        """Return a list of detected fair value gaps.

        Each candle in ``candles`` must provide ``high`` and ``low`` values.
        A simple 3-candle pattern is used:
        - ``bullish`` gap when ``candles[i-2]['high'] < candles[i]['low']``.
        - ``bearish`` gap when ``candles[i-2]['low'] > candles[i]['high']``.

        The returned gaps include the indices of the candles that form the
        pattern and the price range of the gap.
        """
        if candles is None:
            candles = self.candles

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
    def detect_fvgs(
        self, candles: Sequence[Dict[str, Any]] | None = None
    ) -> List[Dict[str, Any]]:
        """Alias to :meth:`find` for older interfaces."""
        return self.find(candles)


# Backwards compatibility
FairValueGapFinder = FVGDetector
