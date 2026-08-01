from hermes import Hermes

import os
from dotenv import load_dotenv

load_dotenv()

os_api = os.getenv('OPEN_SANCTIONS_API')

hr = Hermes()

print(hr.list_countries)