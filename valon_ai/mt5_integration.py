"""MetaTrader 5 integration helpers."""

# Typically you would import MetaTrader5 package, but we keep it optional
# to avoid dependency issues in this template.
try:
    import MetaTrader5 as mt5
except ImportError:  # pragma: no cover - optional dependency
    mt5 = None

from typing import Union


class MT5Client:
    """Simple wrapper around the MetaTrader 5 API."""

    def __init__(self) -> None:
        if mt5 is None:
            raise RuntimeError("MetaTrader5 package is not installed")

        self._connected = False

    def connect(self) -> None:
        """Connect to MetaTrader 5 terminal."""
        if not mt5.initialize():
            raise RuntimeError(f"Failed to initialize MT5: {mt5.last_error()}")
        self._connected = True

    def shutdown(self) -> None:
        """Shutdown connection to the terminal."""
        if self._connected:
            mt5.shutdown()
            self._connected = False

    def get_candles(self, symbol: str, timeframe: Union[str, int], count: int):
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
        if rates is None:
            raise RuntimeError(f"Failed to fetch rates for {symbol}")

        df = pd.DataFrame(rates)
        df["time"] = pd.to_datetime(df["time"], unit="s")

        return df[["time", "open", "high", "low", "close"]].to_dict(orient="records")

    def _send_order(
        self,
        symbol: str,
        volume: float,
        order_type: int,
        price: float | None = None,
        deviation: int = 20,
    ):
        """Internal helper for ``buy`` and ``sell`` methods."""

        if price is None:
            tick = mt5.symbol_info_tick(symbol)
            if tick is None:
                raise RuntimeError(f"Could not get tick data for {symbol}")
            price = tick.ask if order_type == mt5.ORDER_TYPE_BUY else tick.bid

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": price,
            "deviation": deviation,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }

        result = mt5.order_send(request)
        # Convert namedtuple to dictionary for easier consumption
        return result._asdict() if hasattr(result, "_asdict") else result

    def buy(
        self,
        symbol: str,
        volume: float,
        price: float | None = None,
        deviation: int = 20,
    ):
        """Execute a market buy order.

        Parameters
        ----------
        symbol : str
            Trading symbol to buy.
        volume : float
            Lot size of the order.
        price : float | None, optional
            Price to execute at. If ``None`` the current ask price is used.
        deviation : int, optional
            Maximum allowed deviation in points.
        """

        return self._send_order(symbol, volume, mt5.ORDER_TYPE_BUY, price, deviation)

    def sell(
        self,
        symbol: str,
        volume: float,
        price: float | None = None,
        deviation: int = 20,
    ):
        """Execute a market sell order.

        Parameters
        ----------
        symbol : str
            Trading symbol to sell.
        volume : float
            Lot size of the order.
        price : float | None, optional
            Price to execute at. If ``None`` the current bid price is used.
        deviation : int, optional
            Maximum allowed deviation in points.
        """

        return self._send_order(symbol, volume, mt5.ORDER_TYPE_SELL, price, deviation)
