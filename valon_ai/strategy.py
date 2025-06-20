"""Core trading strategy assembly."""

from .smc import SMCAnalyzer
from .order_block import OrderBlockFinder
from .fair_value_gap import FairValueGapFinder
from .break_of_structure import BreakOfStructureFinder
from .risk_management import RiskManager
from .trailing_stop import TrailingStop
from .mt5_integration import MT5Client


class TradingStrategy:
    """Compose different analysis modules into a strategy."""

    def __init__(self):
        self.smc = SMCAnalyzer()
        self.ob = OrderBlockFinder()
        self.fvg = FairValueGapFinder()
        self.bos = BreakOfStructureFinder()
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
        return {
            "smc": self.smc.analyze(data),
            "order_blocks": self.ob.find(data),
            "fvg": self.fvg.find(data),
            "bos": self.bos.find(data),
        }
