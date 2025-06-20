"""Core trading strategy assembly."""

from .smc import SMCAnalyzer
from .order_block import OrderBlockDetector
from .fair_value_gap import FairValueGapFinder
from .break_of_structure import BOSDetector
from .risk_management import RiskManager
from .trailing_stop import TrailingStop
from .mt5_integration import MT5Client


class TradingStrategy:
    """Compose different analysis modules into a strategy."""

    def __init__(self):
        self.smc = SMCAnalyzer()
        # OrderBlockDetector expects candle data upon initialization. We pass an
        # empty list and update the candles when analyzing the market.
        self.ob = OrderBlockDetector([])
        self.fvg = FairValueGapFinder()
        self.bos = BOSDetector([])
        self.risk = RiskManager()
        self.trailing = TrailingStop(distance=10)
        # Connection is optional during initialization
        self.mt5 = None

    def connect(self):
        """Initialize MT5 client."""
        self.mt5 = MT5Client()
        self.mt5.connect()

    def shutdown(self):
        """Shutdown MT5 client."""
        if self.mt5:
            self.mt5.shutdown()

    def analyze_market(self, data):
        """Run all analyses on the market data."""
        # Update order block detector with the latest candle data
        self.ob.candles = data
        self.bos.candles = data
        return {
            "smc": self.smc.analyze(data),
            "bullish_order_blocks": self.ob.detect_bullish_ob(),
            "bearish_order_blocks": self.ob.detect_bearish_ob(),
            "fvg": self.fvg.find(data),
            "bos": self.bos.detect_bos(),
        }
