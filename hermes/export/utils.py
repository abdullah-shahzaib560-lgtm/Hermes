import logging
import time
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def export(data: pd.DataFrame | pd.Series, filetype: str = "csv", loc: Path | str = "data/", name: str | None = None):

    if not isinstance(data, (pd.DataFrame, pd.Series)):
        raise TypeError(f"The data should be pandas DataFrame or Series, got {type(data)}")

    filetype = filetype.lower()
    if not name:
        file_name = f"{round(time.time())}.{filetype}"
    else:
        file_name = f"{name}.{filetype}"

    target_dir = Path(loc)
    target_dir.mkdir(parents=True, exist_ok=True)
    full_path = target_dir / file_name
    try:
        if filetype == "csv":
            data.to_csv(full_path, index=False)
        elif filetype == "json":
            data.to_json(full_path)
        elif filetype == "parquet":
            data.to_parquet(full_path)
        else:
            logger.error(f"The function only supports csv, json, or parquet. Got: {filetype}")
            return

        logger.info(f"Successfully exported data to {full_path}")

    except Exception as e:
        logger.error(f"Error saving file: {e}")


if __name__ == "__main__":
    data = {
        "Name": ["Alice", "Bob", "Charlie", "Diana"],
        "Age": [32, 32, 22, 43],
        "City": ["New York", "London", "Paris", "Tokyo"],
        "Salary": [70000, 85000, 95000, 80000],
    }

    df = pd.DataFrame(data)

    export(data=df, filetype="csv", name="demo")
