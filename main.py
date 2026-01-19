# main.py
"""
Crypto Market Intelligence Agent
Real-time cryptocurrency analysis powered by AWS Bedrock (Claude 3.5 Sonnet)
"""

import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from datetime import datetime

# LangChain imports
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools import Tool
from langchain_aws import ChatBedrock
from langchain import hub

# Our crypto service
from services.crypto_api import (
    get_market_data,
    get_market_overview,
    get_fear_greed
)


# ============================================
# Configuration
# ============================================

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0")


# ============================================
# Define Tools
# ============================================

tools = [
    Tool(
        name="GetCryptoMarketData",
        func=get_market_data,
        description="""Get real-time market data for a specific cryptocurrency.
        Returns current price, 24h/7d/30d price changes, volume, market cap, and trend analysis.
        Input: cryptocurrency symbol (e.g., 'BTC', 'ETH', 'SOL', 'XRP')
        Use this when asked about a specific coin's price, performance, or trend."""
    ),
    Tool(
        name="GetMarketOverview",
        func=get_market_overview,
        description="""Get overview of top 10 cryptocurrencies by market cap.
        Returns prices and 24h changes for major coins.
        Input: can be empty string ''
        Use this when asked about overall market state or top performing coins."""
    ),
    Tool(
        name="GetFearGreedIndex",
        func=get_fear_greed,
        description="""Get the current Crypto Fear & Greed Index.
        Indicates market sentiment from 0 (Extreme Fear) to 100 (Extreme Greed).
        Input: can be empty string ''
        Use this when asked about market sentiment, fear, greed, or market mood."""
    ),
]


# ============================================
# Initialize Agent
# ============================================

def build_agent():
    """Build the LangChain agent with AWS Bedrock"""
    
    # Pull the ReAct prompt from LangChain Hub
    prompt = hub.pull("hwchase17/react")
    
    # Initialize AWS Bedrock LLM
    llm = ChatBedrock(
        model_id=BEDROCK_MODEL_ID,
        region_name=AWS_REGION,
        model_kwargs={
            "temperature": 0.3,
            "max_tokens": 4096,
        }
    )
    
    # Create the agent
    agent = create_react_agent(llm, tools, prompt)
    
    # Create executor with error handling
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5
    )


# ============================================
# FastAPI Application
# ============================================

app = FastAPI(
    title="Crypto Market Intelligence Agent",
    description="Real-time cryptocurrency analysis powered by AWS Bedrock & Claude 3.5",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent
agent_executor = build_agent()


# ============================================
# Request/Response Models
# ============================================

class QueryRequest(BaseModel):
    q: str
    
class QueryResponse(BaseModel):
    query: str
    response: str
    timestamp: str
    model: str


# ============================================
# Endpoints
# ============================================

@app.get("/")
async def root():
    return {
        "service": "Crypto Market Intelligence Agent",
        "version": "2.0.0",
        "model": BEDROCK_MODEL_ID,
        "status": "running",
        "endpoints": {
            "query": "POST /query",
            "health": "GET /health",
            "docs": "GET /docs"
        }
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model": BEDROCK_MODEL_ID
    }


@app.post("/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    """
    Query the Crypto Intelligence Agent
    
    Examples:
    - "What is the current price of BTC?"
    - "Is Bitcoin bullish or bearish right now?"
    - "Give me a market overview"
    - "What's the fear and greed index?"
    - "Analyze ETH market trend"
    """
    
    if not request.q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    # Enhanced prompt for crypto analysis
    prompt_text = f"""You are an expert Cryptocurrency Market Analyst. 
    
Your task: {request.q}

Instructions:
1. Use the available tools to fetch REAL-TIME market data
2. Analyze the data objectively
3. Provide clear bullish/bearish assessment based on:
   - Price changes (24h, 7d, 30d)
   - Volume trends
   - Market sentiment (Fear & Greed if relevant)
4. Give a brief, actionable summary

Be concise but informative. Use emojis for visual clarity.
Always cite the actual numbers from the data."""

    try:
        # Execute agent
        result = agent_executor.invoke({"input": prompt_text})
        
        return QueryResponse(
            query=request.q,
            response=result["output"],
            timestamp=datetime.now().isoformat(),
            model=BEDROCK_MODEL_ID
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Agent error: {str(e)}"
        )


# ============================================
# Quick Analysis Endpoints (No Agent, Direct)
# ============================================

@app.get("/api/price/{symbol}")
async def get_price(symbol: str):
    """Get quick price data for a symbol"""
    from services.crypto_api import CryptoAPIService
    return CryptoAPIService.get_current_price(symbol)


@app.get("/api/market")
async def get_market():
    """Get market overview"""
    from services.crypto_api import CryptoAPIService
    return CryptoAPIService.get_market_overview()


@app.get("/api/sentiment")
async def get_sentiment():
    """Get fear & greed index"""
    from services.crypto_api import CryptoAPIService
    return CryptoAPIService.get_fear_greed_index()


# ============================================
# Run Server
# ============================================

if __name__ == "__main__":
    print(f"""
    🚀 Crypto Market Intelligence Agent
    ====================================
    Model: {BEDROCK_MODEL_ID}
    Region: {AWS_REGION}
    
    Endpoints:
    - POST /query - Ask the AI agent
    - GET /api/price/BTC - Quick price check
    - GET /api/market - Market overview
    - GET /api/sentiment - Fear & Greed Index
    - GET /docs - API Documentation
    """)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
