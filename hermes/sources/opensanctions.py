import logging
import time
import json

import httpx
import pycountry
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def iso3_to_iso2(iso3_code: str) -> str:
    try:
        country = pycountry.countries.get(alpha_3=iso3_code.upper())
        return country.alpha_2 if country else None
    except AttributeError:
        return None


class OpenSanction:
    def __init__(self, api_key: str):
        self._base_url = "https://api.opensanctions.org"
        self._api_key = api_key
        self._headers = {
            "Authorization": f"ApiKey {api_key}",
            "Accept": "application/json"
        }

    def fetch(
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
        country_iso2 = iso3_to_iso2(country)
        if not country_iso2:
            logger.warning(f"Invalid country code: {country}")
            return {}

        url = f"{self._base_url}/search/{dataset}"

        params = {
            "countries": country_iso2,
            "limit": min(limit, 1000)
        }

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
                resp = httpx.get(
                    url=url,
                    params=params,
                    headers=self._headers,
                    timeout=timeout,
                    follow_redirects=True
                )
                resp.raise_for_status()
                data = resp.json()
                logger.info(f"Fetched {data.get('total', {}).get('value', 0)} results")
                return data
                
            except httpx.ReadTimeout:
                if attempt == retries - 1:
                    logger.error(f"Timeout after {retries} attempts")
                    raise
                wait_time = 2 ** attempt
                logger.warning(f"Timeout, retrying in {wait_time}s...")
                time.sleep(wait_time)
                
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    logger.error(f"Dataset '{dataset}' not found")
                    return {}
                if attempt == retries - 1:
                    raise
                wait_time = 2 ** attempt
                logger.warning(f"HTTP {e.response.status_code}, retrying in {wait_time}s...")
                time.sleep(wait_time)
                
            except Exception as e:
                if attempt == retries - 1:
                    raise
                wait_time = 2 ** attempt
                logger.warning(f"Error: {e}, retrying in {wait_time}s...")
                time.sleep(wait_time)

        return {}


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    API_KEY = os.getenv("OPEN_SANCTIONS_API")
    
    if not API_KEY:
        print("Please set OPEN_SANCTIONS_API environment variable")
        exit(1)
    
    os_client = OpenSanction(api_key=API_KEY)
    
    # Test with US OFAC SDN list
    print("Fetching USA sanctions from US OFAC SDN list...")
    data = os_client.fetch(
        country="USA",
        dataset="us_ofac_sdn",
        limit=10
    )
    
    if data:
        print(f"\nResponse keys: {list(data.keys())}")
        print(f"Total results: {data.get('total', {}).get('value', 0)}")
        
        results = data.get("results", [])
        print(f"Results returned: {len(results)}")
        
        if results:
            print("\nFirst result:")
            print(json.dumps(results[0], indent=2))
    else:
        print("No data returned")