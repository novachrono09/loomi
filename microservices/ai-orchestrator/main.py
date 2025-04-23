import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import requests
from typing import Optional
import logging
from datetime import datetime

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID")
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:4000")

openai.api_key = OPENAI_API_KEY
openai.organization = OPENAI_ORG_ID

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    user_id: Optional[str] = None

class VisualSearchRequest(BaseModel):
    image_url: str
    user_id: Optional[str] = None

class EmotionAnalysisRequest(BaseModel):
    text: str
    user_id: Optional[str] = None

@app.post("/chat")
async def chat_with_ai(request: ChatRequest):
    try:
        # Get user context from backend if user_id is provided
        user_context = ""
        if request.user_id:
            try:
                response = requests.get(
                    f"{BACKEND_URL}/users/{request.user_id}/context",
                    headers={"Content-Type": "application/json"},
                )
                if response.status_code == 200:
                    user_context = response.json().get("context", "")
            except Exception as e:
                logger.error(f"Failed to fetch user context: {str(e)}")

        # Construct prompt with user context
        prompt = f"""
        User context: {user_context}
        Current message: {request.message}
        
        You are Loomi, an AI shopping assistant for the Loomi e-commerce platform.
        Provide helpful, concise responses to shopping-related queries.
        """

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful shopping assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=500,
        )

        return {
            "response": response.choices[0].message.content,
            "conversation_id": request.conversation_id or str(datetime.now().timestamp()),
        }
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/visual-search")
async def visual_search(request: VisualSearchRequest):
    try:
        # In a real implementation, we would:
        # 1. Download the image
        # 2. Use a vision model to extract features
        # 3. Search products based on those features
        
        # Mock implementation for now
        mock_products = [
            {
                "id": "1",
                "name": "Striped Cotton T-Shirt",
                "price": 29.99,
                "image": "https://example.com/tshirt.jpg",
                "similarity": 0.92,
            },
            {
                "id": "2",
                "name": "Blue Denim Jeans",
                "price": 59.99,
                "image": "https://example.com/jeans.jpg",
                "similarity": 0.87,
            },
        ]
        
        return {"products": mock_products}
    except Exception as e:
        logger.error(f"Error in visual search: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-emotion")
async def analyze_emotion(request: EmotionAnalysisRequest):
    try:
        # Mock implementation - in reality we'd use an NLP model
        positive_words = ["happy", "excited", "love", "great", "awesome"]
        negative_words = ["angry", "sad", "hate", "terrible", "awful"]
        
        positive_count = sum(1 for word in positive_words if word in request.text.lower())
        negative_count = sum(1 for word in negative_words if word in request.text.lower())
        
        sentiment = "neutral"
        if positive_count > negative_count:
            sentiment = "positive"
        elif negative_count > positive_count:
            sentiment = "negative"
        
        return {"sentiment": sentiment, "scores": {"positive": positive_count, "negative": negative_count}}
    except Exception as e:
        logger.error(f"Error in emotion analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)