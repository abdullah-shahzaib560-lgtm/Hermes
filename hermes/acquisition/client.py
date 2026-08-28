import aiohttp

from typing import Dict

class Client:

    def __init__(self, 
        connector: str, 
        timeout: float = 30.0
    ):
        self.connector = connector
        self.timeout = timeout
            

async def create_client(
    self,

) -> Client:
    ...