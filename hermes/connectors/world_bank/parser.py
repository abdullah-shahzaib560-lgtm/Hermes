import pandas as pd


def records_to_dataframe(records: list) -> pd.DataFrame:
    data = [
        {
            "date": record["date"],
            "indicator_id": record["indicator"]["id"],
            "indicator_name": record["indicator"]["value"],
            "country": record["countryiso3code"],
            "value": record["value"],
            "source": "World_Bank",
        }
        for record in records
    ]

    data = pd.DataFrame(data)

    data.set_index("date", inplace=True)
    data.sort_index(ascending=False, inplace=True)

    data = data.reset_index()
    return data


__all__ = ["records_to_dataframe"]
