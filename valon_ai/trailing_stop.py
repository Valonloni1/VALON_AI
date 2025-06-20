"""Trailing stop management."""

class TrailingStop:
    """Implement trailing stop logic."""

    def __init__(self, distance):
        self.distance = distance

    def update_stop(self, current_price):
        """Update stop level based on current price."""
        # TODO: implement trailing stop logic
        return current_price - self.distance
