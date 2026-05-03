# 📈 Stock Picker Agent — Built with CrewAI

> **AI Engineering Portfolio — Project 4**  
> Automate your search for investment gems using a multi-agent pipeline!

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![CrewAI](https://img.shields.io/badge/CrewAI-latest-FF6B6B?style=flat)](https://crewai.com)
[![Ollama](https://img.shields.io/badge/LLM-Ollama%20%7C%20LLaMA3.2-black?style=flat)](https://ollama.com)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat)](LICENSE)

---

## 🧠 What This Project Does

A **four-agent CrewAI pipeline** that autonomously researches a stock market sector,
performs fundamental and sentiment analysis, and delivers a structured investment
research report — in minutes, not hours.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    STOCK PICKER AGENT PIPELINE                      │
│                                                                     │
│   ┌──────────────┐    ┌──────────────────┐    ┌─────────────────┐  │
│   │ Market Scout │───▶│  Fundamental     │───▶│   Sentiment     │  │
│   │              │    │  Analyst         │    │   Analyst       │  │
│   │ • Web search │    │ • Revenue trends │    │ • News analysis │  │
│   │ • Top 5 picks│    │ • Valuation KPIs │    │ • Social signal │  │
│   │ • Catalysts  │    │ • Moat analysis  │    │ • Analyst rtgs  │  │
│   └──────────────┘    └──────────────────┘    └─────────────────┘  │
│                                                        │            │
│                              ┌─────────────────────────┘            │
│                              ▼                                      │
│                    ┌──────────────────────┐                         │
│                    │  Investment          │                         │
│                    │  Strategist          │                         │
│                    │ • Ranks top 3 picks  │                         │
│                    │ • Conviction levels  │                         │
│                    │ • Entry zones        │──▶ investment_report.md │
│                    │ • Risk assessment    │                         │
│                    └──────────────────────┘                         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Agent Framework** | [CrewAI](https://crewai.com) — latest |
| **LLM** | [Ollama](https://ollama.com) — LLaMA 3.2 (local, free, no rate limits) |
| **Web Search** | [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/) — free, no API key needed |
| **Web Scraping** | CrewAI `ScrapeWebsiteTool` |
| **LLM Router** | [LiteLLM](https://litellm.ai) — unified LLM interface |
| **Output** | Structured Markdown investment report |

> 💡 **100% free stack** — no paid API keys required. Everything runs locally on your machine.

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/FatimaUPPA/stock-picker-agent.git
cd stock-picker-agent
```

### 2. Install Ollama and pull the model

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull the LLaMA 3.2 model (runs locally)
ollama pull llama3.2

# Start Ollama in a separate terminal
ollama serve
```

> On Ubuntu, if the installer fails: `sudo apt-get install zstd -y` then re-run the install command.

### 3. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
pip install litellm
```

### 5. Run the agent

```bash
python stock_picker_agent.py
```

The report is saved as `investment_report.md` in the project root.

> No `.env` file needed — this stack requires zero API keys!

---

## ⚙️ Customisation

Edit the bottom of `stock_picker_agent.py` to target any sector or horizon:

```python
SECTOR             = "Clean Energy"
INVESTMENT_HORIZON = "Short-term (1–3 months)"
```

**Example sector strings:**
- `"AI & Semiconductors"` (default)
- `"Healthcare & Biotech"`
- `"Clean Energy & EVs"`
- `"Fintech & Payments"`
- `"Consumer Discretionary"`

---

## 📄 Sample Output

See [`investment_report_sample.md`](investment_report_sample.md) for a full example report
generated for the AI & Semiconductors sector.

**Preview:**
```
## Top 3 Stock Picks — Ranked by Conviction

### 1. 🏆 NVDA — NVIDIA Corporation
Conviction Level: High
Investment Thesis: NVIDIA maintains an unassailable moat in AI training...

### 2. 🥈 AMD — Advanced Micro Devices
Conviction Level: High
...
```

---

## 🏗️ Project Architecture

```
stock-picker-agent/
├── stock_picker_agent.py        # Main pipeline (agents + tasks + crew)
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template (optional)
├── investment_report_sample.md  # Example output report
└── README.md                    # This file
```

---

## 💡 Key AI Engineering Concepts Demonstrated

- **Multi-agent orchestration** — four specialised agents with distinct roles and goals
- **Sequential task pipeline** with context passing between agents
- **Tool use** — web search + scraping integrated into agent reasoning loops
- **Dynamic task construction** — tasks parametrised at runtime (sector, horizon)
- **Local LLM inference** — fully offline execution via Ollama
- **Structured output** — final report written to file by the strategist agent

---

## 🗺️ Portfolio Context

This project is part of my AI Engineering Portfolio:

| # | Project | Stack |
|---|---------|-------|
| 1 | Local RAG for Geospatial Docs | ChromaDB · Ollama · LangChain |
| 2 | Multimodal AI Agent | Gemini · Voyage AI · MongoDB |
| 3 | Paris Travel AI Agent | yt-dlp · DPR+FAISS · CrewAI · ElevenLabs |
| **4** | **Stock Picker Agent** | **CrewAI · Ollama · DuckDuckGo** |
| 5 | Career Digital Twin | LangGraph · ChromaDB · Gradio |

---

## ⚠️ Disclaimer

This tool is for **educational and research purposes only**. It does not constitute
financial advice. Always consult a licensed financial adviser before making
investment decisions.

---

## 📬 Connect

**Fatima Chahal**  
Postdoctoral Researcher · AI Engineering  
[GitHub](https://github.com/FatimaUPPA) · [LinkedIn](https://linkedin.com/in/fatima-chahal)

---
*Built with ❤️ by Fatima Chahal — AI Engineering Portfolio*