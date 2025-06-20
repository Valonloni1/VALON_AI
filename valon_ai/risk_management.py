"""Risk management utilities."""

class RiskManager:
    """Manage trading risk and position sizing."""

    def __init__(self, risk_per_trade=0.01):
        self.risk_per_trade = risk_per_trade

    def calculate_lot_size(self, account_balance, stop_loss_points):
        """Calculate lot size based on risk parameters."""
        # TODO: implement real calculation
        return 0
