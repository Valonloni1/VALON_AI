"""MetaTrader 5 integration helpers."""

# Typically you would import MetaTrader5 package, but we keep it optional
# to avoid dependency issues in this template.
try:
    import MetaTrader5 as mt5
except ImportError:  # pragma: no cover - optional dependency
    mt5 = None


class MT5Client:
    """Simple wrapper around MetaTrader 5 API."""

    def __init__(self):
        if mt5 is None:
            raise RuntimeError("MetaTrader5 package is not installed")

    def connect(self):
        """Connect to MetaTrader 5 terminal."""
        return mt5.initialize()

    def shutdown(self):
        """Shutdown connection to terminal."""
        mt5.shutdown()
