import uuid, time

async def purchase(self, info, session):
    data = {
        "collectibleItemId": info["collectible_item_id"],
        "expectedCurrency": 1,
        "expectedPrice": info['price'],
        "expectedPurchaserId": self.account['user_id'],
        "expectedPurchaserType": "User",
        "expectedSellerId": info["creator"],
        "expectedSellerType": "User",
        "idempotencyKey": str(uuid.uuid4()),
        "collectibleProductId": info['productid_data'],
        "collectibleItemInstanceId": info['collectible_item_instance_id']
    }
    
    async with session.post(f"https://apis.roblox.com/marketplace-sales/v1/item/{info['collectible_item_id']}/purchase-resale",
                            json=data,
                            headers={**session._default_headers, **{"x-csrf-token": self.account['xcsrf_token']}},
    ssl=False) as response:
        if response.status == 200:
            json_response = await response.json()
            if not json_response.get("purchased"):
                raise Exception(f"Failed to buy item {info['item_id']}, reason: {json_response.get('errorMessage')}")
            
            self.buy_logs.append(f"[{time.strftime('%H:%M:%S', time.localtime())}] Bought item {info['item_id']} for a price of {info['price']}")
        else:
            raise Exception(f"Failed to buy item {info['item_id']}")