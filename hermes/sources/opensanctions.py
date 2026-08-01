import logging
import time
from datetime import timedelta

import httpx
import pycountry
from dotenv import load_dotenv

from hermes.core.cache import RawCache

load_dotenv()

logger = logging.getLogger(__name__)


def iso3_to_iso2(iso3_code: str) -> str:
    try:
        country = pycountry.countries.get(alpha_3=iso3_code.upper())
        return country.alpha_2 if country else "Not Found"
    except AttributeError:
        return "Not Found"


class OpenSanction:
    def __init__(self, api_key: str, cache: RawCache | None = None):
        self._base_url = "https://api.opensanctions.org"
        self._api_key = api_key
        self._headers = {"Authorization": f"ApiKey {api_key}", "Accept": "application/json"}
        self._cache = cache or RawCache()

    def _fetch(
        self,
        country: str,
        dataset: str,
        limit: int = 50,
        changed_since: str = None,
        topics: str = None,
        facets: str = None,
        retries: int = 3,
        timeout: float = 30.0,
    ) -> dict:
        """
        Fetch raw sanctions data from OpenSanctions API.
        Returns raw JSON response as dict.

        Common datasets:
        - us_ofac_sdn: US OFAC Specially Designated Nationals
        - eu_fsf: EU Financial Sanctions Files
        - uk_fcdos: UK FCDO Sanctions List
        - un_sc: UN Security Council Sanctions
        """
        if not dataset:
            raise ValueError("dataset parameter is empty")

        country_iso2 = iso3_to_iso2(country)
        if not country_iso2:
            logger.warning(f"Invalid country code: {country}")
            return {}

        url = f"{self._base_url}/search/{dataset}"

        params = {"countries": country_iso2, "limit": min(limit, 1000)}

        if changed_since:
            params["changed_since"] = changed_since
        if topics:
            params["topics"] = topics
        if facets:
            params["facets"] = facets

        logger.info(f"Fetching from: {url}")
        logger.info(f"Params: {params}")

        for attempt in range(retries):
            try:
                resp = httpx.get(url=url, params=params, headers=self._headers, timeout=timeout, follow_redirects=True)
                resp.raise_for_status()
                data = resp.json()
                logger.info(f"Fetched {data.get('total', {}).get('value', 0)} results")
                return data

            except httpx.ReadTimeout:
                if attempt == retries - 1:
                    logger.error(f"Timeout after {retries} attempts")
                    raise
                wait_time = 2**attempt
                logger.warning(f"Timeout, retrying in {wait_time}s...")
                time.sleep(wait_time)

            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    logger.error(f"Dataset '{dataset}' not found")
                    return {}
                if attempt == retries - 1:
                    raise
                wait_time = 2**attempt
                logger.warning(f"HTTP {e.response.status_code}, retrying in {wait_time}s...")
                time.sleep(wait_time)

            except Exception as e:
                if attempt == retries - 1:
                    raise
                wait_time = 2**attempt
                logger.warning(f"Error: {e}, retrying in {wait_time}s...")
                time.sleep(wait_time)

        return {}

    def fetch(
        self,
        country: str,
        dataset: str,
        limit: int = 50,
        changed_since: str | None = None,
        topic: str | None = None,
        facets: str | None = None,
        retries: int = 3,
        timeout: float = 30.0,
        force: bool = False,
    ):
        cached_params = {
            "country": country,
            "dataset": dataset,
        }

        return self._cache.get_or_fetch(
            source="OpenSanction",
            params=cached_params,
            fetch_fn=lambda: self._fetch(
                country=country,
                dataset=dataset,
                limit=limit,
                changed_since=changed_since,
                topics=topic,
                facets=facets,
                retries=retries,
                timeout=timeout,
            ),
            force=force,
            ttl=timedelta(days=30),
        )
