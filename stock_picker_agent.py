"""
╔══════════════════════════════════════════════════════════════╗
║          Stock Picker Agent — Built with CrewAI              ║
║     Automate your search for investment gems!                ║
║                                                              ║
║  Author : Fatima Chahal (FatimaUPPA)                         ║
║  Project: AI Engineering Portfolio — Project 4               ║
╚══════════════════════════════════════════════════════════════╝

A multi-agent pipeline that:
  1. Searches the web for trending stocks & financial news
  2. Performs fundamental + sentiment analysis
  3. Ranks candidates and produces an investment report
"""

import os
import json
from datetime import datetime
from textwrap import dedent

from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import ScrapeWebsiteTool
from crewai.tools import BaseTool
from duckduckgo_search import DDGS

llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434",
    temperature=0.2,
)

# ─────────────────────────────────────────────
# 1. Tools
# ─────────────────────────────────────────────
from pydantic import Field

class DuckDuckGoSearchTool(BaseTool):
    name: str = "search_the_internet"
    description: str = "Search the internet for current financial news and stock information."

    def _run(self, query: str) -> str:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
        return "\n\n".join([f"{r['title']}\n{r['href']}\n{r['body']}" for r in results])

search_tool = DuckDuckGoSearchTool()
scrape_tool = ScrapeWebsiteTool()

# ─────────────────────────────────────────────
# 2. Agents
# ─────────────────────────────────────────────

market_scout = Agent(
    role="Senior Market Scout",
    goal=dedent("""
        Identify the top 5 promising stocks across sectors based on
        current financial news, momentum signals, and analyst buzz.
        Focus on companies with strong fundamentals and recent catalysts.
    """),
    backstory=dedent("""
        You are a seasoned equity analyst with 15 years on Wall Street.
        You have an uncanny ability to spot emerging opportunities before
        they hit mainstream radars. You combine macro awareness with
        sector-level precision to surface investment gems.
    """),
    tools=[search_tool, scrape_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

fundamental_analyst = Agent(
    role="Fundamental Analyst",
    goal=dedent("""
        For each candidate stock, research and summarise:
        - Revenue & earnings growth trajectory
        - P/E, P/S, debt-to-equity ratios
        - Competitive moat and market position
        - Recent insider activity or institutional flows
        - Key risks and catalysts
    """),
    backstory=dedent("""
        Former CFA charterholder who spent a decade at a top-tier hedge fund
        stress-testing company financials. You have zero tolerance for hype —
        you base every judgment on hard numbers and rigorous reasoning.
    """),
    tools=[search_tool, scrape_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

sentiment_analyst = Agent(
    role="Market Sentiment & News Analyst",
    goal=dedent("""
        Gauge the sentiment surrounding each candidate stock by analysing:
        - Recent news headlines and press releases
        - Social media chatter (Reddit, X/Twitter trends)
        - Analyst upgrades/downgrades in the last 30 days
        - Sector tailwinds or headwinds
        Assign a sentiment score (Bullish / Neutral / Bearish) with justification.
    """),
    backstory=dedent("""
        Data journalist turned quant researcher. You developed NLP-driven
        sentiment pipelines for major trading desks. You know how to separate
        signal from noise in an ocean of financial chatter.
    """),
    tools=[search_tool, scrape_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

investment_strategist = Agent(
    role="Chief Investment Strategist",
    goal=dedent("""
        Synthesise all research into a concise, actionable investment report:
        - Final ranking of the top 3 stocks (with conviction levels)
        - One-paragraph thesis per pick
        - Entry considerations (support zones, catalysts to watch)
        - Risk warnings and suggested position sizing
        - Executive summary suitable for a portfolio manager
    """),
    backstory=dedent("""
        You are a veteran fund manager who has navigated bull markets, crashes,
        and everything in between. Your reports are legendary for their clarity
        and actionable insights. You synthesise complex research into decisive
        recommendations that help investors act with confidence.
    """),
    tools=[],
    llm=llm,
    verbose=True,
    allow_delegation=False,
)

# ─────────────────────────────────────────────
# 3. Tasks
# ─────────────────────────────────────────────

def build_tasks(sector: str, investment_horizon: str) -> list[Task]:
    """Dynamically build the task pipeline for a given sector & horizon."""

    task_scout = Task(
        description=dedent(f"""
            Today is {datetime.now().strftime('%B %d, %Y')}.

            Search for the top 5 promising stocks in the **{sector}** sector.
            Investment horizon: **{investment_horizon}**.

            For each candidate, provide:
            - Ticker symbol & company name
            - Why it caught your attention (catalyst, momentum, news)
            - 1–2 URLs you used to surface it

            Format your output as a numbered list.
        """),
        agent=market_scout,
        expected_output="A numbered list of 5 stock candidates with tickers, names, reasons, and source URLs.",
    )

    task_fundamentals = Task(
        description=dedent(f"""
            Using the 5 candidate stocks identified by the Market Scout,
            perform a fundamental analysis for each one.

            Focus on:
            - Revenue growth (YoY %)
            - Earnings per share (EPS) trend
            - Key valuation ratios (P/E, P/S, EV/EBITDA if available)
            - Balance-sheet health (debt levels, cash position)
            - Competitive advantages / moat

            Investment horizon context: {investment_horizon}.
            Be precise and cite your sources.
        """),
        agent=fundamental_analyst,
        expected_output="A structured fundamental analysis section for each of the 5 stocks.",
        context=[task_scout],
    )

    task_sentiment = Task(
        description=dedent(f"""
            For the same 5 stocks, perform a sentiment & news analysis:

            1. Search for the latest headlines (last 7 days)
            2. Check for analyst rating changes
            3. Identify any upcoming catalysts (earnings, product launches, regulatory events)
            4. Assign a sentiment verdict: 🟢 Bullish / 🟡 Neutral / 🔴 Bearish

            Be concise but rigorous.
        """),
        agent=sentiment_analyst,
        expected_output="Sentiment analysis and news summary for each of the 5 stocks with a verdict.",
        context=[task_scout],
    )

    task_report = Task(
        description=dedent(f"""
            You have received fundamental analysis and sentiment analysis for
            5 candidate stocks in the {sector} sector.

            Produce a professional **Investment Research Report** with:

            ## Executive Summary
            (3–4 sentences — the key takeaway for a busy portfolio manager)

            ## Top 3 Stock Picks — Ranked by Conviction
            For each pick:
            - **Ticker & Company**
            - **Conviction Level**: High / Medium
            - **Investment Thesis** (2–3 sentences)
            - **Key Catalysts to Watch**
            - **Main Risks**
            - **Entry Consideration** (price zone or trigger event)

            ## Stocks to Monitor (Rank 4–5)
            Brief note on why they didn't make the top 3.

            ## Risk Disclaimer
            Standard disclaimer reminding readers this is not financial advice.

            ---
            Date: {datetime.now().strftime('%B %d, %Y')}
            Prepared by: Stock Picker Agent (CrewAI)
            Investment Horizon: {investment_horizon}
            Sector Focus: {sector}
        """),
        agent=investment_strategist,
        expected_output="A complete, well-structured investment research report in Markdown format.",
        context=[task_fundamentals, task_sentiment],
        output_file="investment_report.md",
    )

    return [task_scout, task_fundamentals, task_sentiment, task_report]


# ─────────────────────────────────────────────
# 4. Crew
# ─────────────────────────────────────────────

def run_stock_picker(sector: str = "AI & Technology",
                     investment_horizon: str = "6–12 months") -> str:
    """
    Launch the Stock Picker Crew and return the final investment report.

    Parameters
    ----------
    sector              : e.g. "AI & Technology", "Clean Energy", "Healthcare"
    investment_horizon  : e.g. "Short-term (1–3 months)", "6–12 months", "2–3 years"
    """
    print(f"\n{'='*60}")
    print(f"  🤖 Stock Picker Agent — CrewAI Pipeline")
    print(f"  Sector   : {sector}")
    print(f"  Horizon  : {investment_horizon}")
    print(f"  Date     : {datetime.now().strftime('%B %d, %Y')}")
    print(f"{'='*60}\n")

    tasks = build_tasks(sector, investment_horizon)

    crew = Crew(
        agents=[market_scout, fundamental_analyst, sentiment_analyst, investment_strategist],
        tasks=tasks,
        process=Process.sequential,   # Scout → Fundamentals → Sentiment → Report
        verbose=True,
        # memory=True,                  # Agents share a short-term memory store
        # embedder={
        #     "provider": "openai",
        #     "config": {
        #         "model": "text-embedding-3-small",
        #         "api_key": os.environ.get("OPENAI_API_KEY", ""),
        #     },
        # },
    )

    result = crew.kickoff()
    return result


# ─────────────────────────────────────────────
# 5. Entry point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # ── Customise your run here ──────────────────
    SECTOR             = "AI & Semiconductors"
    INVESTMENT_HORIZON = "6–12 months"
    # ────────────────────────────────────────────

    report = run_stock_picker(
        sector=SECTOR,
        investment_horizon=INVESTMENT_HORIZON,
    )

    print("\n" + "="*60)
    print("  ✅  Report generated → investment_report.md")
    print("="*60)
    print(report)
