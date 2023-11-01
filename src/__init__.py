import os, aiohttp, asyncio

from .handle      import v_one
from .handle      import v_two
from .cookie      import user_id
from .cookie      import xcrf_token
from collections import deque

class sniper:
    error_logs: list = deque(maxlen=5)
    buy_logs: list = []
    search_logs: list = deque(maxlen=5)
    
    total_searchers: int = 0
    
    average_speed: list = deque(maxlen=20)

    clear: str = "cls" if os.name == 'nt' else "clear"

    def __init__(self, data: dict):
        self.items = data["items"]
        for item in self.items["list"]:
            if not item.isnumeric():
                raise ValueError("Item Id must be a number not a string")
            
        self.cookie = data["cookie"]
        
        self.account = {"xcsrf_token": asyncio.run(xcrf_token.get(self)), "user_id": asyncio.run(user_id.get(self))}

    async def run(self):
        await asyncio.gather(*[v_one.run(self), v_two.run(self)])