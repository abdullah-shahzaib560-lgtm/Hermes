import logging

import pandas as pd

logger = logging.getLogger(__name__)


def normalize_sdmx(data):
    _obs = data["dataSets"]["series"]["0:0:0"]["observations"]
    obs = []
    for key, value in _obs.items():
        obs.append(str(value))

    _freq = data["structures"][0]["dimensions"]["series"]

    for idx, _fr in enumerate(_freq):
        if _fr["id"].value() == "FREQUENCY":
            logger.info("frequency is found")
            freq_idx = idx

        else:
            logger.info("frequency is not found")

    freq_values = len(_freq["values"])
    if freq_values > 1:
        logger.info("There are multiple freq taking the first value")

    freq = _freq["values"][freq_idx]
    ind = data["structures"][0]["dimensions"]["series"]

    for idx, i in enumerate(ind):
        if i["id"].value() == "INDICATOR":
            logger.info("INDICATOR is found")

        else:
            logger.info("INDICATOR is not found")

    _time = data["structures"][0]["dimensions"]["observation"][0]
    time = []
    if _time["id"] != "TIME_PERIOD":
        logger.warning("The Dates are not in the places")

    for key, value in _time["values"].items():
        time.append(int(value))

    observation = pd.Series(obs)
    frequency = pd.Series(freq)
    Time = pd.Series(time)
    df = pd.concat([observation, frequency, Time], axis=1)
    df["indicator"] = f"{data}"


__all__ = ["normalize_sdmx"]
