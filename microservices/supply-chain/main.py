import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging
from datetime import datetime, timedelta
import random
import requests

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

class InventoryRequest(BaseModel):
    product_id: str
    quantity: int

class ShippingEstimateRequest(BaseModel):
    product_ids: List[str]
    destination_zip: str
    shipping_method: str = "standard"

class Supplier:
    def __init__(self, id: str, name: str, lead_time: int, reliability: float):
        self.id = id
        self.name = name
        self.lead_time = lead_time  # in days
        self.reliability = reliability  # 0-1

# Mock suppliers
SUPPLIERS = [
    Supplier("sup1", "Global Suppliers Inc.", 7, 0.95),
    Supplier("sup2", "Quick Ship Co.", 3, 0.85),
    Supplier("sup3", "Budget Parts Ltd.", 14, 0.98),
]

@app.post("/check-inventory")
async def check_inventory(request: InventoryRequest):
    try:
        # In a real system, we'd check actual inventory databases
        # Mock implementation with random availability
        
        available = random.random() > 0.3  # 70% chance of being in stock
        stock = random.randint(0, 100) if available else 0
        
        if available and stock >= request.quantity:
            status = "in_stock"
            message = f"Available ({stock} in stock)"
            suppliers = [sup for sup in SUPPLIERS if random.random() < sup.reliability]
        else:
            status = "out_of_stock"
            message = "Currently unavailable"
            suppliers = []
            
            # Check if any suppliers can fulfill
            for sup in SUPPLIERS:
                if random.random() < sup.reliability * 0.8:  # Lower chance for restock
                    suppliers.append(sup)
        
        return {
            "product_id": request.product_id,
            "status": status,
            "message": message,
            "current_stock": stock if available else 0,
            "suppliers": [
                {
                    "id": sup.id,
                    "name": sup.name,
                    "lead_time": sup.lead_time,
                    "estimated_restock_date": (
                        datetime.now() + timedelta(days=sup.lead_time)
                        .strftime("%Y-%m-%d")
                    if sup else None,
                }
                for sup in suppliers
            ],
        }
    except Exception as e:
        logger.error(f"Error checking inventory: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/estimate-shipping")
async def estimate_shipping(request: ShippingEstimateRequest):
    try:
        # Mock shipping estimates based on product count and destination
        base_days = 3 if request.shipping_method == "standard" else 1
        additional_days = len(request.product_ids) * 0.5  # Half day per additional item
        
        # Simulate distance factor based on zip code
        distance_factor = abs(int(request.destination_zip[:3]) - 100) / 1000
        total_days = base_days + additional_days + distance_factor * 2
        
        # Add some randomness
        total_days *= random.uniform(0.9, 1.1)
        total_days = max(1, round(total_days))
        
        return {
            "estimated_days": total_days,
            "delivery_date": (datetime.now() + timedelta(days=total_days))
            .strftime("%Y-%m-%d"),
            "shipping_method": request.shipping_method,
            "products": request.product_ids,
        }
    except Exception as e:
        logger.error(f"Error estimating shipping: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/supply-risks")
async def get_supply_risks():
    try:
        # Mock supply risk data
        risks = [
            {
                "product_category": "electronics",
                "risk_level": "medium",
                "primary_risk": "semiconductor shortages",
                "alternative_suppliers": 2,
            },
            {
                "product_category": "textiles",
                "risk_level": "low",
                "primary_risk": "shipping delays",
                "alternative_suppliers": 5,
            },
        ]
        return {"risks": risks, "updated_at": datetime.now().isoformat()}
    except Exception as e:
        logger.error(f"Error getting supply risks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5002)