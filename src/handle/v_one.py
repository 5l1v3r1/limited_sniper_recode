import time, os, aiohttp, asyncio

from . import split_list

from ..lookup import v_one
from ..lookup import reseller
from ..buy import buy

async def run(self):
    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=None), cookies={".ROBLOSECURITY": self.cookie}, headers={'Accept-Encoding': 'gzip, deflate'})
    
    items = split_list.get([*self.items["list"].keys()])
    while True:
     try:
        for item_list in items:
            item_data = await v_one.get(self, item_list, session)
            self.total_searchers += len(items)
            for item in item_data:
                info = {"creator": None, "price": int(item.get("lowestResalePrice", 999999999)), "productid_data": None, "collectible_item_id": item.get("collectibleItemId"), "item_id": str(item.get("id"))}
                
                if item.get("priceStatus") == "Off Sale":
                    del self.items["list"][info['item_id']]
                    continue

                if not item.get("hasResellers") or info["price"] > self.items['global_max_price'] or info['price'] > self.items["list"][info['item_id']]["max_price"]:
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
        self.error_logs.append(f"V1 [{time.strftime('%H:%M:%S', time.localtime())}] {e}")
        
     finally:   
        items = split_list.get([*self.items["list"].keys()])
        
        os.system(self.clear)
        print("Total Searches: " + repr(self.total_searchers)
              + "\n\n\nSearch Logs:\n" + '\n'.join(log for log in self.search_logs) 
              + f"\n\nBuy Logs:" + '\n'.join(log for log in self.buy_logs) 
              + f"\n\n\nTotal Items bought: {len(self.buy_logs)}" 
              + "\n\n\nError Logs:\n" + '\n'.join(log for log in self.error_logs)
        )
        await asyncio.sleep(1)
        
