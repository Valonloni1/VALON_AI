class RiskManager:
    def __init__(self, account_balance=10000, risk_per_trade=0.01):
        """
        :param account_balance: total account capital
        :param risk_per_trade: percentage to risk per trade (e.g. 0.01 = 1%)
        """
        self.account_balance = account_balance
        self.risk_per_trade = risk_per_trade

    def calculate_lot_size(self, entry_price, stop_loss_price, pip_value=10):
        """
        Calculate lot size based on risk and stop loss distance.
        :param entry_price: trade entry price
        :param stop_loss_price: stop loss price
        :param pip_value: pip value for the symbol (e.g. 10 for XAUUSD)
        :return: lot size (float)
        """
        risk_amount = self.account_balance * self.risk_per_trade
        stop_loss_pips = abs(entry_price - stop_loss_price)
        if stop_loss_pips == 0:
            return 0
        lot_size = risk_amount / (stop_loss_pips * pip_value)
        return round(lot_size, 2)

    def is_trade_allowed(self, open_trades, max_trades=3):
        """
        Check if new trade can be opened.
        :param open_trades: current open trades
        :param max_trades: allowed number of simultaneous trades
        :return: True/False
        """
        return len(open_trades) < max_trades
