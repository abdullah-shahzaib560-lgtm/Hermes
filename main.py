import os

from dotenv import load_dotenv

from hermes import Hermes

load_dotenv()

os_api = os.getenv("OPEN_SANCTIONS_API")

hr = Hermes(opensanction_api=os_api)

print(hr.list_countries)
