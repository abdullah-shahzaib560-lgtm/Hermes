import asyncio
import os

from dotenv import load_dotenv

from hermes import Hermes

load_dotenv()

os_api = os.getenv("OPEN_SANCTIONS_API")
new_api = os.getenv("NEWs_DATA_API")
hr = Hermes(opensanction_api=os_api, new_data_api=new_api)

print(hr.list_countries)


async def main():
    result = await hr.features.get_country_risk_features("USA")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
