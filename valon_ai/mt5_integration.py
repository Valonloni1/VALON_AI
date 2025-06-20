"""MetaTrader 5 integration helpers."""

# Typically you would import MetaTrader5 package, but we keep it optional
# to avoid dependency issues in this template.
try:
    import MetaTrader5 as mt5
except ImportError:  # pragma: no cover - optional dependency
    mt5 = None

from typing import Union


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

    def get_candles(self, symbol, timeframe, count):
        """Return OHLC candle data for a symbol.

        Parameters
        ----------
        symbol : str
            Market symbol to request data for.
        timeframe : Union[str, int]
            Timeframe string like ``"M5"`` or the corresponding ``mt5``
            constant such as ``mt5.TIMEFRAME_M5``.
        count : int
            Number of candles to retrieve starting from the most recent.
        """

        if isinstance(timeframe, str):
            attr = f"TIMEFRAME_{timeframe.upper()}"
            if not hasattr(mt5, attr):
                raise ValueError(f"Unknown timeframe {timeframe}")
            timeframe = getattr(mt5, attr)

        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)

        candles = []
        for rate in rates:
            candles.append(
                {
                    "time": rate["time"],
                    "open": rate["open"],
                    "high": rate["high"],
                    "low": rate["low"],
                    "close": rate["close"],
                }
            )

        return candles
