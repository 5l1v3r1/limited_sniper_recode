import time, aiohttp, asyncio

from ..lookup import v_two
from ..buy import buy
from ..lookup import reseller

async def run(self):
    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=None), cookies={".ROBLOSECURITY": self.cookie}, headers={'Accept-Encoding': 'gzip, deflate'})
    
    while True:
        try:
           for item_id in self.items["list"].copy():
               item = await v_two.get(self, item_id, session)
               self.total_searchers += 1
               info = {"creator": 0, "price": item.get("CollectiblesItemDetails", {}).get("CollectibleLowestResalePrice", 9999999), "productid_data": item.get("CollectibleProductId"), "collectible_item_id": item.get("CollectibleItemId"), "item_id": str(item.get("AssetId"))} 
               
               if not item.get("IsForSale"):
                    del self.items["list"][info['item_id']]
                    continue
               
               if info['price'] > self.items['global_max_price'] or info['price'] > self.items["list"][item_id]["max_price"]:
                   continue
               
               rss = await reseller.get(self, info["collectible_item_id"], session)
               info['price'] = rss['price']
               info["productid_data"] = rss["collectibleProductId"]
               info["creator"] = rss["seller"]["sellerId"]
               info["collectible_item_instance_id"] = rss["collectibleItemInstanceId"]
            
               if info['price'] > self.items['global_max_price'] or info['price'] > self.items["list"][info['item_id']]["max_price"]:
                continue
            
               await buy.purchase(self, info, session)
               
        except Exception as e:
            await session.close()
            session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=None), cookies={".ROBLOSECURITY": self.cookie}, headers={'Accept-Encoding': 'gzip, deflate'})  # just to refresh the session
            self.error_logs.append(f"V2 [{time.strftime('%H:%M:%S', time.localtime())}] {e}")
            
        finally:
            await asyncio.sleep(max((60 / 1000) - max(sum(list(self.average_speed)) / len(self.average_speed), 0), 0) * len(self.items["list"]))