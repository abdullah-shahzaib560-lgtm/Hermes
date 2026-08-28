import pandas as pd


def klines_to_dataframe(all_candles: list) -> pd.DataFrame:
    if not all_candles:
        return pd.DataFrame()

    df = pd.DataFrame(
        all_candles,
        columns=[
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_volume",
            "trades_count",
            "taker_buy_volume",
            "taker_buy_quote_volume",
            "ignore",
        ],
    )

    for col in [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "quote_volume",
        "taker_buy_volume",
        "taker_buy_quote_volume",
    ]:
        df[col] = df[col].astype(float)

    df["trades_count"] = df["trades_count"].astype(int)
    df = df.drop(columns=["ignore"])
    df = df.drop_duplicates(subset=["open_time"], keep="first")
    df = df.sort_values("open_time").reset_index(drop=True)

    return df


__all__ = ["klines_to_dataframe"]
