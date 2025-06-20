from valon_ai.risk_management import RiskManager

class StrategyEngine:
    def __init__(self, candles):
        self.candles = candles
        self.smc = StructureAnalyzer(candles)
        self.ob = OrderBlockDetector(candles)
        self.bos = BOSDetector(candles)
        self.fvg = FVGDetector(candles)
        self.risk = RiskManager()

    def generate_signals(self, open_trades=[]):
        signals = []

        bos_events = self.bos.detect_bos()
        bullish_obs = self.ob.detect_bullish_ob()
        bearish_obs = self.ob.detect_bearish_ob()
        fvgs = self.fvg.detect_fvgs()

        for bos in bos_events:
            bos_index = bos["index"]
            bos_type = bos["type"]

            matching_ob = []
            matching_fvg = []

            if bos_type == "bullish":
                matching_ob = [ob for ob in bullish_obs if ob["index"] == bos_index - 1]
                matching_fvg = [fvg for fvg in fvgs if fvg["type"] == "bullish" and fvg["index"] == bos_index]
            elif bos_type == "bearish":
                matching_ob = [ob for ob in bearish_obs if ob["index"] == bos_index - 1]
                matching_fvg = [fvg for fvg in fvgs if fvg["type"] == "bearish" and fvg["index"] == bos_index]

            # Vetëm nëse ka OB + FVG dhe lejohet tregtia nga RiskManager
            if matching_ob and matching_fvg and self.risk.is_trade_allowed(open_trades):
                entry_price = bos["price"]
                stop_loss_price = entry_price - 10 if bos_type == "bullish" else entry_price + 10
                lot_size = self.risk.calculate_lot_size(entry_price, stop_loss_price)

                signals.append({
                    "type": bos_type.upper(),
                    "index": bos_index,
                    "price": entry_price,
                    "stop_loss": stop_loss_price,
                    "lot_size": lot_size
                })

        return signals
