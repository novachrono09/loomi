import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging
import requests
import numpy as np
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:4000")
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")

class ProductPricingRequest(BaseModel):
    product_id: str
    current_price: float
    user_id: Optional[str] = None

class DynamicPricingRequest(BaseModel):
    products: List[ProductPricingRequest]
    market_conditions: Optional[dict] = None

@app.post("/calculate-price")
async def calculate_price(request: ProductPricingRequest):
    try:
        # In a real implementation, we would:
        # 1. Fetch product demand data
        # 2. Check inventory levels
        # 3. Analyze competitor pricing
        # 4. Consider user's purchase history if available
        
        # Mock implementation with simple rules
        base_price = request.current_price
        
        # Simulate demand factor (0.8 to 1.2)
        demand_factor = 0.8 + 0.4 * np.random.random()
        
        # Simulate time-based adjustment (discounts at certain times)
        hour = datetime.now().hour
        time_factor = 1.0
        if 1 <= hour <= 5:  # Late night discount
            time_factor = 0.9
        elif 12 <= hour <= 14:  # Lunchtime surge
            time_factor = 1.1
            
        # Calculate final price
        final_price = round(base_price * demand_factor * time_factor, 2)
        
        # Ensure price doesn't go below a minimum
        min_price = base_price * 0.7
        final_price = max(final_price, min_price)
        
        return {
            "product_id": request.product_id,
            "original_price": base_price,
            "dynamic_price": final_price,
            "discount": round((base_price - final_price) / base_price * 100, 1) if final_price < base_price else 0,
            "factors": {
                "demand": round(demand_factor, 2),
                "time": round(time_factor, 2),
            }
        }
    except Exception as e:
        logger.error(f"Error in pricing calculation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/bulk-pricing")
async def bulk_pricing(request: DynamicPricingRequest):
    try:
        results = []
        for product in request.products:
            result = await calculate_price(product)
            results.append(result)
        return {"results": results}
    except Exception as e:
        logger.error(f"Error in bulk pricing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/market-trends")
async def get_market_trends():
    try:
        # Mock market trends data
        categories = ["electronics", "clothing", "home", "beauty"]
        trends = {}
        
        for category in categories:
            trends[category] = {
                "average_price_change": round(np.random.uniform(-0.1, 0.1), 2),
                "demand_change": round(np.random.uniform(-0.2, 0.2), 2),
                "popular_products": [
                    {"id": f"{category[:3]}{i}", "name": f"Popular {category} item {i}"} 
                    for i in range(1, 4)
                ]
            }
        
        return {"trends": trends, "as_of": datetime.now().isoformat()}
    except Exception as e:
        logger.error(f"Error fetching market trends: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)