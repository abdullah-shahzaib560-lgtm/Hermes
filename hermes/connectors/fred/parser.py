import pandas as pd


def observations_to_dataframe(r: dict, series_id: str) -> pd.DataFrame:
    df = pd.DataFrame(r["observations"])
    df.drop(columns=["realtime_start", "realtime_end"], inplace=True)
    df["series_id"] = series_id
    df["unit"] = r["units"]
    df = df.set_index("date")
    df = df.sort_index(ascending=False)
    return df


__all__ = ["observations_to_dataframe"]
