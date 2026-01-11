# 🚀 Crypto Market Intelligence Agent

[![Live Demo](https://img.shields.io/badge/🤗_HuggingFace-Live_Demo-yellow?style=for-the-badge)](https://huggingface.co/spaces/Arnie1980/Crypto-Market-Intelligence-Agent)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![AWS Bedrock](https://img.shields.io/badge/AWS_Bedrock-Claude_3-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/bedrock/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Gradio](https://img.shields.io/badge/Gradio-UI-orange?style=for-the-badge)](https://gradio.app)

> **AI-powered real-time cryptocurrency market analysis using AWS Bedrock (Claude), live market data, and automated reporting.**

<p align="center">
  <a href="https://huggingface.co/spaces/Arnie1980/Crypto-Market-Intelligence-Agent">
    <img src="https://img.shields.io/badge/▶️_TRY_LIVE_DEMO-HuggingFace-FFD21E?style=for-the-badge&logoColor=black" alt="Live Demo" height="50">
  </a>
</p>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Live Demo](#-live-demo)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Automation with n8n](#-automation-with-n8n)
- [Deployment](#-deployment)
- [Screenshots](#-screenshots)
- [Project Structure](#-project-structure)
- [Lessons Learned](#-lessons-learned)
- [Future Improvements](#-future-improvements)
- [License](#-license)
- [Contact](#-contact)

---

## 🎯 Overview

**Crypto Market Intelligence Agent** is a full-stack AI application that provides real-time cryptocurrency market analysis. Ask any question about crypto markets in plain English and get instant, AI-powered insights based on live data.

### The Problem

- ❌ Crypto data is scattered across multiple sources
- ❌ Manual analysis is time-consuming
- ❌ No easy way to get AI-powered insights on live data
- ❌ Automated reporting requires complex setups

### The Solution

- ✅ **Unified Interface** - Ask questions in natural language
- ✅ **Live Data** - Real-time prices from CoinGecko
- ✅ **AI Analysis** - Claude analyzes trends and provides recommendations
- ✅ **Automated Reports** - Hourly updates via Slack & Email

---

## ✨ Features

### 🤖 AI-Powered Analysis
Ask questions like:
- *"Is BTC bullish or bearish right now?"*
- *"Compare ETH and SOL performance"*
- *"What's the market sentiment?"*

### 📊 Real-Time Data
- Live prices from **CoinGecko API**
- 24h, 7d, 30d price changes
- Market cap & volume
- **Fear & Greed Index** sentiment

### ⚡ Multiple Interfaces
- **Web UI** - Gradio interface on HuggingFace
- **REST API** - FastAPI backend
- **Automated Reports** - n8n workflows

### 🔔 Automated Notifications
- Hourly Slack messages
- Beautiful HTML email reports
- Fully customizable schedule

---

## 🌐 Live Demo

**Try it now:** [https://huggingface.co/spaces/Arnie1980/Crypto-Market-Intelligence-Agent](https://huggingface.co/spaces/Arnie1980/Crypto-Market-Intelligence-Agent)

### Example Queries:
```
"What is the current price of BTC and is it bullish or bearish?"
"Give me a market overview of top cryptocurrencies"
"What's the fear and greed index right now?"
"Analyze ETH market trend"
```

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              USER INTERFACES                             │
├─────────────────────────────────────────────────────────────────────────┤
│  🌐 Gradio Web UI          📱 REST API           ⏰ n8n Automation       │
│  (HuggingFace Spaces)      (FastAPI)             (Scheduled Jobs)        │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           APPLICATION LAYER                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    │
│   │  Query Parser   │───▶│  Data Fetcher   │───▶│   AI Analyzer   │    │
│   │                 │    │                 │    │                 │    │
│   │ • Detect coins  │    │ • CoinGecko API │    │ • AWS Bedrock   │    │
│   │ • Parse intent  │    │ • Fear & Greed  │    │ • Claude 3      │    │
│   └─────────────────┘    └─────────────────┘    └─────────────────┘    │
│                                                                          │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           EXTERNAL SERVICES                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    │
│   │   CoinGecko     │    │  Alternative.me │    │   AWS Bedrock   │    │
│   │                 │    │                 │    │                 │    │
│   │ • Live prices   │    │ • Fear & Greed  │    │ • Claude 3      │    │
│   │ • Market data   │    │   Index         │    │   Sonnet        │    │
│   │ • Top coins     │    │                 │    │                 │    │
│   └─────────────────┘    └─────────────────┘    └─────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User Query
    │
    ▼
┌──────────────────┐
│ Parse Query      │──▶ Detect mentioned coins (BTC, ETH, etc.)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Fetch Live Data  │──▶ CoinGecko API + Fear & Greed Index
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ AI Analysis      │──▶ Claude 3 Sonnet via AWS Bedrock
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Format Response  │──▶ Markdown with emojis & insights
└────────┬─────────┘
         │
         ▼
    User Response
```

---

## 🛠 Tech Stack

### AI/ML
| Technology | Purpose |
|------------|---------|
| **AWS Bedrock** | Managed AI service |
| **Claude 3 Sonnet** | Text generation & analysis |
| **LangChain** | Agent orchestration |

### Backend
| Technology | Purpose |
|------------|---------|
| **Python 3.11** | Core language |
| **FastAPI** | REST API framework |
| **Pydantic** | Data validation |
| **Uvicorn** | ASGI server |

### Data Sources
| Source | Data Provided |
|--------|---------------|
| **CoinGecko API** | Live prices, market cap, volume |
| **Alternative.me** | Fear & Greed Index |

### Frontend & Deployment
| Technology | Purpose |
|------------|---------|
| **Gradio** | Web UI framework |
| **HuggingFace Spaces** | Hosting |
| **n8n** | Workflow automation |

### Notifications
| Channel | Integration |
|---------|-------------|
| **Slack** | Real-time alerts |
| **Gmail** | HTML email reports |

---

## 📦 Installation

### Prerequisites
- Python 3.11+
- AWS Account with Bedrock access
- (Optional) n8n for automation

### Local Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/crypto-intelligence-agent.git
cd crypto-intelligence-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your AWS credentials

# Run the server
python main.py
```

### Environment Variables

```env
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1

# Model Configuration
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0

# Server Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

---

## 🚀 Usage

### Web Interface

1. Open [https://huggingface.co/spaces/Arnie1980/Crypto-Market-Intelligence-Agent](https://huggingface.co/spaces/Arnie1980/Crypto-Market-Intelligence-Agent)
2. Type your question
3. Click "Analyze"
4. Get AI-powered insights!

### API Usage

```bash
# Health check
curl http://localhost:8000/health

# Quick price check
curl http://localhost:8000/api/price/BTC

# AI-powered analysis
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"q": "Is BTC bullish or bearish right now?"}'
```

### Python Client

```python
import requests

def analyze_crypto(question: str) -> dict:
    response = requests.post(
        "http://localhost:8000/query",
        json={"q": question}
    )
    return response.json()

# Example
result = analyze_crypto("What is the current BTC price and trend?")
print(result["response"])
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Service info |
| `GET` | `/health` | Health check |
| `POST` | `/query` | AI-powered analysis |
| `GET` | `/api/price/{symbol}` | Quick price check |
| `GET` | `/api/market` | Top 10 cryptocurrencies |
| `GET` | `/api/sentiment` | Fear & Greed Index |
| `GET` | `/docs` | Swagger documentation |

### Example Response

```json
{
  "query": "What is the current price of BTC?",
  "response": "🏆 **Bitcoin (BTC) Market Analysis**\n\n💰 Current Price: $94,523.00\n\n📈 24h Change: 🟢 +2.1%\n📈 7d Change: 🟢 +5.3%\n📉 30d Change: 🔴 -1.2%\n\n🌐 Market Sentiment: 😰 Fear (29/100)\n\n💼 **Analysis:** BTC is showing positive momentum...",
  "timestamp": "2026-01-11T15:30:00",
  "model": "anthropic.claude-3-sonnet-20240229-v1:0"
}
```

---

## ⚙️ Automation with n8n

### Workflow Overview

```
⏰ Schedule (Hourly)
      │
      ▼
🤖 HTTP Request ──▶ POST /query
      │
      ▼
💬 Slack ──▶ Send formatted message
      │
      ▼
📧 Gmail ──▶ Send HTML report
```

### Setup Steps

1. Import `n8n_workflow.json` into n8n
2. Configure Slack credentials
3. Configure Gmail OAuth2
4. Set the API URL (ngrok or deployed)
5. Activate the workflow

### Email Report Preview

The automated emails include:
- 📊 AI-generated market analysis
- 💰 Current prices and trends
- 📈 Fear & Greed Index
- ⏰ Timestamp and next update time

---

## 🌐 Deployment

### HuggingFace Spaces

1. Create a new Space (Gradio SDK)
2. Upload `app.py`, `requirements.txt`, `README.md`
3. Add secrets in Settings:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_REGION`
   - `BEDROCK_MODEL_ID`
4. Wait for build (~2-3 minutes)

### Docker (Coming Soon)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

---

## 📸 Screenshots

### Web Interface
*Gradio UI with AI Analysis tab*

### Example Analysis
```
🤖 AI-Powered Crypto Analysis
⏰ 2026-01-11 15:30:00

🏆 Bitcoin (BTC) Market Analysis

💰 Current Price: $94,523.00 

📈 24h Change: 🟢 +2.1%
📈 7d Change: 🟢 +5.3%  
📉 30d Change: 🔴 -1.2%

🌐 Market Sentiment: 😰 Fear (29/100 on Fear & Greed Index)

💼 Analysis: BTC is showing positive short-term momentum 
with gains over the past 24 hours and week. However, the 
30-day performance shows slight decline. The Fear & Greed 
Index at 29 indicates market fear, which historically 
presents potential accumulation opportunities.

📊 Recommendation: Consider dollar-cost averaging during 
this fear period while monitoring for trend confirmation.
```

---

## 📁 Project Structure

```
crypto-intelligence-agent/
├── 📄 main.py                 # FastAPI server + LangChain agent
├── 📁 services/
│   ├── __init__.py
│   └── crypto_api.py          # CoinGecko & Fear/Greed integration
├── 📄 app.py                  # Gradio UI (HuggingFace)
├── 📄 requirements.txt        # Python dependencies
├── 📄 .env.example            # Environment template
├── 📁 automation/
│   └── n8n_workflow.json      # n8n automation workflow
├── 📁 docs/
│   ├── SETUP_GUIDE.md
│   └── DEPLOYMENT_GUIDE.md
└── 📄 README.md               # This file
```

---

## 💡 Lessons Learned

### Technical
1. **AWS Bedrock model IDs** - Newer models require inference profiles (`us.` prefix)
2. **JSON formatting** - Use `json.dumps()` instead of f-strings for API bodies
3. **Dependency management** - Pin versions to avoid conflicts (especially Gradio + HuggingFace Hub)

### Process
1. **Start simple** - Get basic API working before adding AI
2. **Test incrementally** - Each component separately before integration
3. **Document as you go** - Saves time when deploying

### Architecture
1. **Fallback gracefully** - App works without AI (shows raw data)
2. **Separate concerns** - Data fetching vs AI analysis vs UI
3. **Make it configurable** - Environment variables for all settings

---

## 🚀 Future Improvements

- [ ] Add more cryptocurrencies
- [ ] Historical price charts
- [ ] Portfolio tracking
- [ ] Price alerts
- [ ] Technical indicators (RSI, MACD)
- [ ] Multi-language support
- [ ] Mobile app
- [ ] Discord bot integration

---

## 📄 License

MIT License - feel free to use this project for learning and portfolio purposes.

---

## 📞 Contact

**Arnold Németh**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/arnold-nemeth)
[![HuggingFace](https://img.shields.io/badge/🤗_HuggingFace-Arnie1980-yellow?style=for-the-badge)](https://huggingface.co/Arnie1980)

---

## ⭐ Star History

If you found this project useful, please consider giving it a star! ⭐

---

<p align="center">
  <b>Built with ❤️ using AWS Bedrock, Claude AI, FastAPI & Gradio</b>
</p>

<p align="center">
  <a href="https://huggingface.co/spaces/Arnie1980/Crypto-Market-Intelligence-Agent">
    <img src="https://img.shields.io/badge/▶️_TRY_THE_DEMO-HuggingFace-FFD21E?style=for-the-badge" alt="Demo">
  </a>
</p>
