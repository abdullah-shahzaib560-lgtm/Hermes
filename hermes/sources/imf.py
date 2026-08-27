import asyncio
import logging
from datetime import timedelta
from functools import partial

import aiohttp
import pandas as pd

from hermes.core.cache import RawCache

logger = logging.getLogger(__name__)


class IMF:
    def __init__(self, cache: RawCache | None = None):
        self._cache = cache or RawCache()
        self.url: str = "https://api.imf.org/external/sdmx/3.0/data/dataflow/"

    async def _fetch(
        self,
        country: str,
        agency: str,
        dataflow_id: str,
        key: str,
        version: str = "~",
        timeout: float = 30.0,
        retries: int = 3,
    ) -> pd.DataFrame:

        url = f"{self.url}{agency}/{dataflow_id}/{version}/{country}.{key}"
        headers = {"Accept": "application/json"}

        empty = pd.DataFrame(columns=["date", "indicator_id", "country", "value", "source"])

        r = None
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as client:
            for attempt in range(retries):
                try:
                    resp = await client.get(url=url, headers=headers)
                    resp.raise_for_status()
                    r = await resp.json()
                    break
                except TimeoutError:
                    if attempt == retries - 1:
                        raise
                    await asyncio.sleep(2**attempt)
                except aiohttp.ClientResponseError as e:
                    if e.status == 404:
                        logger.warning(f"404: country={country}, dataflow={dataflow_id}, key={key}")
                        return empty
                    logger.error(f"HTTP error: {e.status}")
                    raise
        return r['data']


    async def normalize(self, data):
        _obs = data['dataSets']['series']['0:0:0']['observations']
        obs = []
        for key, value in _obs.items():
            obs.append(str(value))

        _freq = data['structures'][0]['dimensions']['series']

        for idx, _fr in enumerate(_freq):

            if _fr['id'].value() == "FREQUENCY":
                logger.info('frequency is found')
                freq_idx = idx

            else:
                logger.info('frequency is not found')

        freq_values = len(_freq['values'])
        if freq_values > 1: logger.info('There are multiple freq taking the first value')

        freq = _freq['values'][freq_idx]
        ind =  data['structures'][0]['dimensions']['series']

        for idx, i in enumerate(ind):
            if i['id'].value() == 'INDICATOR':
                logger.info('INDICATOR is found')
                ind_idx = idx

            else:
                logger.info('INDICATOR is not found')

        _time = data['structures'][0]['dimensions']['observation'][0]
        time = []
        if _time['id'] != 'TIME_PERIOD':
            logger.warning('The Dates are not in the places')

        for key, value in _time['values'].items():
            time.append(int(value))

        observation = pd.Series(obs)
        frequency = pd.Series(freq)
        Time = pd.Series(time)
        df = pd.concat([observation, frequency, Time], axis=1)
        df['indicator'] = f'{data}'

    async def fetch(
        self,
        country: str,
        agency: str,
        dataflow_id: str,
        key: str,
        timeout: float = 30.0,
        retries: int = 3,
        force: bool = False,
    ) -> pd.DataFrame:

        cache_params = {
            "country": country,
            "key": key,
            "agency": agency,
            "dataflow_id": dataflow_id,
        }

        return await self._cache.get_or_fetch(
            source="imf",
            params=cache_params,
            fetch_fn=partial(
                self._fetch,
                country=country,
                agency=agency,
                dataflow_id=dataflow_id,
                key=key,
                timeout=timeout,
                retries=retries,
            ),
            force=force,
            ttl=timedelta(days=7),
        )

async def main():
    import json
    imf = IMF()
    data = await imf._fetch(country='USA', agency="IMF.RES", dataflow_id="WEO", key="GGXWDG_NGDP")
    with open('data/imf.json', 'w') as file:
        json.dump(data, file, indent=4)
    print('Done')

# 2. Use asyncio.run to execute the coroutine
if __name__ == '__main__':
    import os
    os.makedirs('data', exist_ok=True)
    asyncio.run(main())

