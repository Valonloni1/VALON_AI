"""Example script that runs all detectors on sample candle data."""

from pprint import pprint

from valon_ai.order_block import OrderBlockDetector
from valon_ai.fair_value_gap import FVGDetector
from valon_ai.break_of_structure import BOSDetector
from valon_ai.smc import SMCAnalyzer


SAMPLE_CANDLES = [
    {
        "open": 100,
        "high": 105,
        "low": 99,
        "close": 104,
        "time": "2025-01-01",
    },
    {
        "open": 104,
        "high": 106,
        "low": 101,
        "close": 102,
        "time": "2025-01-02",
    },
    {
        "open": 102,
        "high": 107,
        "low": 100,
        "close": 106,
        "time": "2025-01-03",
    },
    {
        "open": 106,
        "high": 110,
        "low": 105,
        "close": 109,
        "time": "2025-01-04",
    },
    {
        "open": 109,
        "high": 111,
        "low": 107,
        "close": 108,
        "time": "2025-01-05",
    },
    {
        "open": 108,
        "high": 112,
        "low": 107,
        "close": 111,
        "time": "2025-01-06",
    },
]


def main() -> None:
    """Run all detectors using the sample candle data."""
    smc = SMCAnalyzer()
    ob_detector = OrderBlockDetector(SAMPLE_CANDLES)
    bos_detector = BOSDetector(SAMPLE_CANDLES)
    fvg_detector = FVGDetector()

    results = {
        "smc": smc.analyze(SAMPLE_CANDLES),
        "bullish_order_blocks": ob_detector.detect_bullish_ob(),
        "bearish_order_blocks": ob_detector.detect_bearish_ob(),
        "fvg": fvg_detector.find(SAMPLE_CANDLES),
        "bos": bos_detector.detect_bos(),
    }

    pprint(results)


if __name__ == "__main__":
    main()
