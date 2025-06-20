"""Example script that runs all detectors on sample candle data."""

from pprint import pprint

from valon_ai.order_block import OrderBlockDetector
from valon_ai.fair_value_gap import FVGDetector
from valon_ai.break_of_structure import BOSDetector
from valon_ai.smc import SMCAnalyzer


SAMPLE_CANDLES = [
    {"open": 1.05, "high": 1.10, "low": 0.94, "close": 0.95},
    {"open": 0.95, "high": 1.15, "low": 0.92, "close": 1.12},
    {"open": 1.12, "high": 1.13, "low": 0.87, "close": 0.90},
    {"open": 0.90, "high": 0.93, "low": 0.85, "close": 0.92},
    {"open": 0.92, "high": 1.05, "low": 0.91, "close": 1.02},
    {"open": 1.02, "high": 1.20, "low": 1.01, "close": 1.15},
    {"open": 1.15, "high": 1.25, "low": 1.10, "close": 1.20},
    {"open": 1.20, "high": 1.30, "low": 1.18, "close": 0.92},
    {"open": 0.92, "high": 1.00, "low": 0.90, "close": 0.95},
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
