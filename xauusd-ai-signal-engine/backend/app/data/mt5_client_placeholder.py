class MT5ClientPlaceholder:
    """V2 boundary only. V1 intentionally does not connect to MT5 or brokers."""

    def fetch_market_snapshot(self) -> dict:
        raise NotImplementedError("MT5 integration is reserved for V2 and disabled in V1.")
