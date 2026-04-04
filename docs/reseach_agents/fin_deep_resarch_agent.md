# References
1. [deep-agent-course](https://academy.langchain.com/courses/take/deep-agents-with-langgraph/texts/68193154-getting-set-up)
2. [deep-agent-course-repo](https://github.com/langchain-ai/deep-agents-from-scratch.git)
2. [deepagent-repo](https://github.com/langchain-ai/deepagents)


#  open-source projects
- Karpathy 开源的 autoresearch 让 agent 自主优化大模型训练。
- [Open Deep Research](https://blog.langchain.com/open-deep-research/)
  Deep research workflows	Open-source deep research agent pattern with configurable models, search tools, and MCP servers. 

- [OpenBB](https://openbb.co/)
  [OpenBB github](https://github.com/OpenBB-finance/OpenBB)
  Finance data and analysis	Open-source financial analysis platform for market, macro, and portfolio research.
  - https://github.com/AI4Finance-Foundation/FinRobot/blob/master/tutorials_advanced/agent_openbb.ipynb
  - 


- [FinRobot](https://github.com/ai4finance-foundation/finrobot)
  Finance research agents, Open-source AI agent platform for financial analysis using LLMs. 



# Portfolio Insight Workflow for portfolios 
Here’s a practical step-by-step guide to building an **AI Portfolio Assistant** for portfolios, using open-source tools and a finance/research workflow. The strongest open-source building blocks I found are **OpenBB** for portfolio and market data, **FinRobot** for financial analysis agents, and **Langfuse** for monitoring, traces, and prompt evaluation. [openbb](https://openbb.co/blog/open-portfolio-a-suite-for-asset-managers-on-openbb/)

## Step-by-step guide

### 1) Define the assistant’s job
Start with a read-only assistant that can answer questions like:
- What changed in my portfolio today?
- Which positions drifted away from target allocation?
- What are the biggest risks, news, or catalyst events?
- What should I research before rebalancing?

A real-world example of this pattern is an open-source AI portfolio assistant that sends morning portfolio allocation, buy suggestions, limit prices, and news sentiment alerts. [linkedin](https://www.linkedin.com/posts/furic_opensource-ai-investing-activity-7432440082726518784-TITI)

### 2) Pick the core data layer
Use **OpenBB** as your market and portfolio analytics layer. OpenBB’s SDK supports normalized financial data, portfolio analysis, and custom reporting, which makes it a strong base for portfolio insight workflows. [pypi](https://pypi.org/project/openbb/0.0.1/)

### 3) Add the agent layer
Use **FinRobot** if you want a finance-specific agent framework. FinRobot is designed for financial analysis with a workflow that includes perception, reasoning, task routing, and report generation. [github](https://github.com/ai4finance-foundation/finrobot)

### 4) Add observability
Use **Langfuse** to log traces, prompts, outputs, and evaluations. Langfuse is an open-source observability platform for LLM apps and integrates with OpenTelemetry, which is useful when you want to monitor quality and improve prompts over time. [zenml](https://www.zenml.io/blog/langsmith-alternatives)

### 5) Design the research workflow
A good portfolio assistant usually follows this flow:
1. Ingest holdings and target allocations.
2. Pull market data, fundamentals, news, and macro signals.
3. Run screening and risk checks.
4. Rank opportunities or concerns.
5. Generate a short investment memo.
6. Store feedback and later compare outcomes.  

FinRobot’s workflow and the open-source “deep research” agent pattern both fit this multi-step structure well. [blog.langchain](https://blog.langchain.com/open-deep-research/)

### 6) Add decision rules
Keep the first version rule-based before making it “fully agentic.”
- Rebalance if drift exceeds a threshold.
- Flag positions with negative news sentiment.
- Highlight concentration risk, volatility spikes, or earnings events.
- Suggest research-only actions, not trades, unless you explicitly add execution later.

This matches how portfolio-assistant projects typically separate insight generation from execution. [github](https://github.com/AdityaPrakash-26/ai-portfolio-assistant)

### 7) Build the output format
Make the assistant produce a daily or weekly digest:
- Portfolio summary.
- Allocation drift.
- Top risks.
- Top opportunities.
- Evidence links.
- Action items for manual review.

OpenBB’s reporting and portfolio tooling, combined with LLM-based summaries, are a good fit for this style of output. [openbb](https://openbb.co/blog/open-portfolio-a-suite-for-asset-managers-on-openbb/)

### 8) Add feedback and continuous improvement
Capture user feedback such as:
- “Useful / not useful.”
- “Wrong ticker.”
- “Too verbose.”
- “Missed this risk.”

Then use those annotations to refine prompts, retrieval sources, and ranking logic. Langfuse is designed for this kind of iterative improvement loop. [langfuse](https://langfuse.com/integrations/native/opentelemetry)

## Suggested stack
| Layer | Recommendation | Why |
|---|---|---|
| Data and portfolio analytics | OpenBB | Strong finance data, portfolio, and reporting support.  [pypi](https://pypi.org/project/openbb/0.0.1/) |
| Agent framework | FinRobot | Finance-oriented multi-agent analysis workflows.  [github](https://github.com/ai4finance-foundation/finrobot) |
| Research orchestration | LangGraph or Open Deep Research pattern | Good for multi-step deep research flows.  [business20channel](https://business20channel.tv/top-10-best-agentic-ai-courses-to-attend-online-in-2026-27-february-2026) |
| Observability | Langfuse | Open-source tracing, logs, prompt/version tracking.  [zenml](https://www.zenml.io/blog/langsmith-alternatives) |

## Recommended MVP
If you want the fastest path, build this first:
- Read holdings from CSV or broker export.
- Pull quotes and fundamentals via OpenBB.
- Summarize news and risks with an LLM.
- Generate a morning email report.
- Log everything in Langfuse.

That gets you a useful portfolio assistant without taking on trading automation too early. [linkedin](https://www.linkedin.com/posts/furic_opensource-ai-investing-activity-7432440082726518784-TITI)

If you want, I can turn this into either:
1. a **system architecture diagram**, or  
2. a **Python implementation plan with folder structure and code modules**.





# Questions and some ideas


- Q: how to deal with multi-step search loops?
  multi-step search react loop : query, search, validate, and repeat. 
  One structural shift that helps is adding a "planner" first to break the main topic into sub-tasks.  

- Q: When you're running those loops, how are you managing the state so the agent tracks what it already knows?

- Q: how to write high-quality queries for search?
Building high-quality queries is a common hurdle. One practical move is to have the agent first generate a "search plan" with three distinct angles for the same topic to ensure it doesn't get tunnel vision. 



- Q: how would you want the agent to distinguish between a truly useful source and one that's just cluttering the context?
A common move is to have a "filtering agent" score each search result for relevance before it even hits the synthesis step.

- Q: Since search can be noisy and search results can be messy, what criteria would you give that agent to decide if a page is worth keeping or if it's just noise?
- Q: how are you planning to filter out irrelevant pages so they don't clutter your synthesis?

a simple relevance score is a great starting point. When you were running those LangChain demos, 


evaluation and validation are often the hardest parts of any agentic system. 

One practical way to handle that is to use a "multi-critique" prompt that forces the LLM to look for specific evidence like dates or citations before it gives a passing score.


- Q: what was the biggest "failure" you actually noticed—did the agent tend to get stuck in a loop, or did it just bring back a lot of data that didn't really answer the main question?

- Q: how do you prevent it from just searching for the same thing again or getting stuck in a loop?
  A practical move is to store a "history" of tried queries in your LangGraph state and pass it back to the LLM so it knows what already failed. 

 One quick tip for that loop issue: you can maintain a "search history" list in your LangGraph state and have a router node compare new queries against it to force a broader search. 


- Q: Once it gathers enough data, how are you handling the final synthesis to ensure it's a cohesive report?
- Q: Regarding that final synthesis,  how do you plan to handle the context window if the agent collects a massive amount of text from all those different search loops?
- Q: how the agent synthesizes large amounts of retrieved data?


A solid move for synthesis is a "Map-Reduce" pattern: have a summarizer agent turn each raw search result into a bulleted list of facts before the final writer combines them. 


# Prompting

I want to build a deep reseach agent for finance portfolio insight， 
Bussiness workflow:
what kind of workflow do you recommend?
what will be the bottleneck and challenges?

Data Layer:
what kind of data source and data layer do you recommend?
How to ingest the latest news data?


Agentic Design:
what kind of agentic structure do you recommend?
what kind of agents do we need?
what kind of agentic pattern do you recommend?


## Meta prompt for building a Deep Research report prompt

write a meta prompt to use in the chatgpt deep reseach , which will help to generate Deep Research report for building solution of finance portfolio insight agent, based on the above infor


## Deep Research report prompt
```
You are operating in Deep Research mode.

Your role is:
A senior AI systems architect + quantitative financial researcher tasked with designing a production-grade finance portfolio insight agent.

You must behave like a disciplined research system, not a chatbot.

---

# 🎯 Mission

Produce a comprehensive, evidence-based, implementation-ready research report for building a "Finance Portfolio Insight Agent System".

This system must:
- analyze portfolios
- ingest real-time market + news data
- perform multi-step research loops
- generate high-quality, explainable insights

---

# 🧠 REQUIRED THINKING MODE

You MUST follow this internal workflow:

1. Problem Decomposition
   - Break the problem into subsystems:
     (workflow, data layer, agent design, loop control, evaluation)

2. Multi-Step Research
   For EACH subsystem:
   - generate multiple search angles
   - gather diverse sources
   - compare perspectives

3. Evidence Filtering
   - prioritize high-authority sources
   - remove redundant / low-signal content

4. Structured Extraction
   - convert findings into structured knowledge:
     facts, patterns, architectures, trade-offs

5. Cross-Validation
   - verify key claims across sources
   - highlight uncertainty explicitly

6. Synthesis
   - integrate findings into a coherent system design
   - avoid disjoint summaries

---

# 🔁 RESEARCH LOOP CONTROL

You MUST:

- Avoid repeating similar queries
- Maintain a mental "search history"
- Expand queries if results are narrow
- Stop when:
  - marginal information gain is low
  - sufficient coverage is achieved

---

# 📊 OUTPUT STRUCTURE (STRICT)

Your final report MUST follow this structure:

---

## 1. System Overview
- High-level architecture
- Key design principles

---

## 2. Business Workflow
- End-to-end pipeline
- Stage-by-stage breakdown:
  - input
  - processing
  - output
- Failure modes

---

## 3. Data Layer Design
- Data sources:
  - market data
  - news
  - alternative data
- Ingestion strategy (real-time vs batch)
- Data pipeline architecture
- Storage layers:
  - raw
  - processed
  - vector
  - serving

- Special focus:
  - news ingestion (freshness, deduplication, entity extraction)

---

## 4. Agentic Architecture

Define ALL required agents:

- Planner
- Query Generator
- Retrieval
- Filtering
- Extraction
- Critic / Validator
- Memory
- Synthesis
- Portfolio Analyst

For EACH agent:
- role
- input/output schema
- prompt strategy

---

## 5. Multi-Step Research Loop Design

Define a controlled loop:

Plan → Multi-Query → Retrieve → Filter → Extract → Validate → Update State

You MUST include:
- stopping criteria
- loop failure cases
- query diversification mechanism
- redundancy prevention

---

## 6. State & Memory Design

Define system state:

- query history
- retrieved sources
- extracted facts
- confidence scores

Explain:
- how to prevent repeated queries
- how to manage long context
- how to persist memory

---

## 7. Information Quality Control

Define scoring system:

- relevance
- recency
- authority
- novelty
- factual density

Explain:
- filtering strategy
- noise reduction

---

## 8. Synthesis Strategy

Design how to combine large information:

- Map-Reduce summarization
- structured intermediate outputs

Explain:
- hallucination mitigation
- traceability to sources

---

## 9. Portfolio Insight Engine

Define domain-specific logic:

- risk analysis
- macro exposure
- sector allocation
- scenario analysis

Explain:
- how LLM integrates with quantitative signals

---

## 10. Bottlenecks & Challenges

Identify real-world issues:

- loop degeneration
- noisy search results
- stale data
- evaluation difficulty
- latency / cost

For each:
- root cause
- mitigation strategy

---

## 11. Evaluation Framework

Define how to measure quality:

- factual correctness
- reasoning quality
- completeness

Include:
- multi-critic validation approach

---

# ⚙️ OUTPUT REQUIREMENTS

- Be precise and technical
- Avoid generic explanations
- Prefer structured formats (tables / JSON where useful)
- Provide concrete mechanisms, not vague ideas
- Ensure internal consistency

---

# 🚫 WHAT TO AVOID

- shallow summaries
- repeating the same idea
- unverified claims
- over-reliance on a single source
- excessive verbosity without structure

---

# ✅ SUCCESS CRITERIA

Your output should read like:
- a system design document
- a research-backed architecture proposal
- something directly implementable in an agent framework (e.g., LangGraph)

---

# 🔥 OPTIONAL (HIGH VALUE)

If possible, include:
- example state schema
- pseudo DAG / graph workflow
- sample agent prompts

```

## Deep Research Prompt (Finance Portfolio Insight Agent Builder)
```
You are a senior AI systems architect and quantitative financial researcher.

Your task is to design a production-grade "Deep Research Agent System" for finance portfolio insight.

This is NOT a simple explanation task. You must:
- think in systems (data + agents + workflows)
- reason step-by-step
- evaluate trade-offs
- produce actionable architecture

---

## 🎯 Objective

Design a complete solution for a finance portfolio insight agent that can:
- analyze a portfolio
- incorporate real-time market + news data
- perform multi-step research
- generate high-quality investment insights

---

## 🧩 Required Output Structure

You MUST structure your response into the following sections:

---

### 1. Business Workflow Design

Define the full lifecycle:

- user intent → structured task
- planning phase
- iterative research loop
- aggregation / synthesis
- portfolio analysis layer
- final report generation

For each stage:
- describe purpose
- define inputs/outputs
- highlight failure modes

---

### 2. Data Layer Architecture

Design a scalable data system:

#### Data Sources
- market data (prices, fundamentals)
- news (real-time ingestion)
- alternative data (optional)

#### Data Pipeline
- ingestion (streaming vs batch)
- cleaning & deduplication
- entity extraction (tickers, companies)
- storage layers:
  - raw
  - processed
  - vector DB
  - online serving

#### Key Requirements
- freshness (low latency updates)
- deduplication
- time-awareness

---

### 3. Agentic System Design

Define a modular agent system.

You MUST include:

- Planner Agent
- Query Generator Agent
- Retrieval Agent
- Filtering Agent
- Extraction Agent
- Critic / Validator Agent
- Memory Agent
- Synthesis Agent
- Portfolio Analyst Agent

For each agent:
- role
- input/output schema
- key prompt strategy

---

### 4. Multi-Step Research Loop Design

Design a controlled loop (NOT naive ReAct):

Loop structure:
- plan → multi-query → retrieve → filter → extract → validate → update state

You MUST specify:
- stopping criteria
- loop failure modes
- query diversification strategy
- redundancy avoidance mechanism

---

### 5. State & Memory Design

Define how the system tracks knowledge across steps.

Include:

- query history
- retrieved sources
- extracted facts
- confidence scores

Explain:
- how to prevent repeated queries
- how to manage long context (token limits)
- how to persist memory across runs

---

### 6. Information Quality & Filtering

Define a scoring system for sources.

Include scoring dimensions:
- relevance
- recency
- authority
- novelty
- factual density

Explain:
- how to filter noise before synthesis
- how to detect low-quality or redundant content

---

### 7. Synthesis Strategy

Design how the system handles large-scale information.

You MUST include:
- Map-Reduce pattern
- intermediate structured summaries
- final narrative generation

Explain:
- how to avoid hallucination
- how to preserve traceability to sources

---

### 8. Portfolio Insight Engine

Define domain-specific logic:

- risk analysis (beta, drawdown, correlation)
- macro exposure
- sector concentration
- scenario analysis

Explain how LLM + quantitative signals interact.

---

### 9. Bottlenecks & Challenges

Identify REAL system risks:

- loop degeneration
- noisy data
- stale information
- evaluation difficulty
- latency / cost

For each:
- explain why it happens
- propose mitigation strategies

---

### 10. Evaluation & Validation Framework

Design how to measure system quality.

Include:
- factual accuracy checks
- reasoning validation
- completeness scoring

You MUST include a "multi-critic" evaluation approach.

---

## ⚙️ Constraints

- Prefer structured outputs (JSON where useful)
- Avoid vague statements
- Provide concrete mechanisms, not just ideas
- Think like a production system designer

---

## 🔁 Reasoning Requirements

Before answering:
1. Decompose the problem into sub-systems
2. Consider trade-offs
3. Validate internal consistency

---

## 📤 Output Quality Bar

Your response should:
- feel like a system design doc from a senior engineer
- be implementable (LangGraph / agent framework ready)
- avoid generic LLM explanations

---

## 🔥 Bonus (Optional but Valuable)

If possible, include:
- example state schema
- example agent prompts
- pseudo DAG / graph structure
```

  



