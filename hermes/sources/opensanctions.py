import logging
import os
import time
from datetime import timedelta

import httpx
import pandas as pd
import pycountry
from dotenv import load_dotenv

from hermes.core.cache import RawCache

load_dotenv()

logger = logging.getLogger(__name__)
Api = os.getenv("OPEN_SANCTIONS_API")


def iso3_to_iso2(iso3_code):
    try:
        return pycountry.countries.get(alpha_3=iso3_code.upper()).alpha_2
    except AttributeError:
        return "Not Found"


class OpenSanction:
    def __init__(self, api_key: str, cache: RawCache | None = None):
        self._url = "https://api.opensanctions.org"
        self._cache = cache or RawCache()
        self._api = api_key

    def _fetch(
        self,
        country: str,
        facets: str,
        changed_since,
        topics: str,
        dataset: str = "default",
        limit: int = 0,
        retries: int = 3,
        timeout: float = 30.0,
    ) -> pd.DataFrame:

        country_iso3 = iso3_to_iso2(iso3_code=country)
        if not dataset:
            raise ValueError("The dataset parameter is empty")
        url = f"{self._url}/search/{dataset}"

        params = {"countries": country_iso3, "limit": limit}

        if facets:
            params["facets"] = facets
        if topics:
            params["topics"] = topics
        if changed_since:
            params["changed_since"] = changed_since

        empty = pd.DataFrame(columns=["date", "indicator_id", "country", "value", "source"])

        r = None
        for attempt in range(retries):
            try:
                resp = httpx.get(url=url, params=params, timeout=timeout, follow_redirects=True)
                resp.raise_for_status()
                r = resp.content
                r = r.decode()
                break
            except httpx.ReadTimeout:
                if attempt == retries - 1:
                    raise
                time.sleep(2**attempt)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    logger.warning(f"404: country={country}")
                    return empty
                logger.error(f"HTTP error: {e.response.status_code}")
                raise
        logger.debug(f"OpenSanctions response length: {len(r)}")
        return empty

    def fetch(
        self,
        country: str,
        facets: str,
        changed_since,
        topics: str,
        dataset: str = "default",
        limit: int = 0,
        retries: int = 3,
        timeout: float = 30.0,
        force: bool = False,
    ) -> pd.DataFrame:
        cache_params = {"country": country, "dataset": dataset, "limit": limit}

        return self._cache.get_or_fetch(
            source="imf",
            params=cache_params,
            fetch_fn=lambda: self._fetch(
                country=country,
                facets=facets,
                changed_since=changed_since,
                topics=topics,
                dataset=dataset,
                timeout=timeout,
                retries=retries,
            ),
            force=force,
            ttl=timedelta(days=7),
        )


if __name__ == "__main__":
    Os = OpenSanction(api_key=Api)
    data = Os._fetch(country="USA", facets="", changed_since=None, topics="")
    print(data)
