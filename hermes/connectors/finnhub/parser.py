import pandas as pd


def candles_to_dataframe(all_candles: list) -> pd.DataFrame:
    if not all_candles:
        return pd.DataFrame()

    df = pd.DataFrame(
        all_candles,
        columns=["open_time", "open", "high", "low", "close", "volume"],
    )

    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)

    df = df.drop_duplicates(subset=["open_time"], keep="first")
    df = df.sort_values("open_time").reset_index(drop=True)

    return df


__all__ = ["candles_to_dataframe"]
