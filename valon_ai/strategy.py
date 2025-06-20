from valon_ai.smc import StructureAnalyzer
from valon_ai.order_block import OrderBlockDetector
from valon_ai.break_of_structure import BOSDetector
from valon_ai.fair_value_gap import FVGDetector

class StrategyEngine:
    def __init__(self, candles):
        self.candles = candles
        self.smc = StructureAnalyzer(candles)
        self.ob = OrderBlockDetector(candles)
        self.bos = BOSDetector(candles)
        self.fvg = FVGDetector(candles)

    def generate_signals(self):
        signals = []

        bos_events = self.bos.detect_bos()
        bullish_obs = self.ob.detect_bullish_ob()
        bearish_obs = self.ob.detect_bearish_ob()
        fvgs = self.fvg.detect_fvgs()

        for bos in bos_events:
            bos_index = bos["index"]
            bos_type = bos["type"]

            matching_ob = None
            matching_fvg = None

            if bos_type == "bullish":
                matching_ob = [
                    ob for ob in bullish_obs if ob["index"] == bos_index - 1
                ]
                matching_fvg = [
                    fvg
                    for fvg in fvgs
                    if fvg["type"] == "bullish" and fvg["index"] == bos_index
                ]
            elif bos_type == "bearish":
                matching_ob = [
                    ob for ob in bearish_obs if ob["index"] == bos_index - 1
                ]
                matching_fvg = [
                    fvg
                    for fvg in fvgs
                    if fvg["type"] == "bearish" and fvg["index"] == bos_index
                ]

            if matching_ob and matching_fvg:
                signals.append({
                    "type": bos_type.upper(),
                    "index": bos_index,
                    "price": bos["price"]
                })

        return signals
