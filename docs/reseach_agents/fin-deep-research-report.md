# Finance Portfolio Insight Agent System – Design Report (English Translation)

## Executive Summary

This report translates a detailed Chinese design for a **Finance Portfolio Insight Agent** into English, preserving all technical content and citations. It describes a multi-agent architecture that ingests real-time market and news data, performs iterative research, and produces explainable investment insights. Key components include data pipelines for market and news feeds, specialized LLM-driven agents (planner, retriever, extractor, etc.), controlled iterative loops, state/memory management, quality scoring, and domain-specific analysis (risk, exposure, allocation). The system is structured and implementable, with example schemas and prompts. All citation markers from the original report are kept intact for traceability.  

## System Overview

【45†embed_image】**Figure 1:** Illustration of the multi-agent investment analysis workflow. A central Portfolio Manager agent acts as the hub, delegating subtasks to specialist agents (macro, fundamental, quantitative) and then synthesizing their outputs into a final report【16†L602-L610】. The design follows a **hub-and-spoke architecture**: one orchestrator agent coordinates multiple specialized sub-agents. This modular approach ensures clear responsibility separation and parallelism【16†L602-L610】. For example, one agent analyzes macroeconomic factors, another examines company fundamentals, while a third handles quantitative signals; their results are then integrated. 

Key design principles include **modularity** (each agent has a focused role), **explainability** (agents use explicit tools and cite sources to ground claims【11†L239-L242】), and **reliability** (an integrated tracing system automatically checks for hallucinations and relevancy errors【8†L75-L84】【11†L233-L242】). The system blends traditional financial analysis (risk models, historical data) with advanced AI. It emphasizes **truthfulness and accountability**: every claim must be backed by data or tools【11†L238-L242】. The goal is an enterprise-grade system where complex analysis is transparent and auditable.

## Business Workflow

The end-to-end pipeline proceeds as follows:

- **Input:** The user provides a natural-language query (e.g. “How would a Fed rate cut affect my GOOGL holdings?”) along with the portfolio holdings and parameters. Structured data about positions, benchmarks, and constraints are loaded.  

- **Planning and Task Decomposition:** A **Planner agent** interprets the query and breaks it into sub-questions or tasks (e.g. “analyze macro impact on tech sector”, “assess Alphabet’s fundamentals”, “evaluate technical signals”)【16†L602-L610】【43†L78-L86】. This step may involve crafting a chain of thought to ensure no aspect is overlooked, producing a research plan.

- **Iterative Research Loop:** For each planned task, the system enters a loop:  
  1. **Query Generation:** A Query Generator creates specific search queries or API requests based on the task (e.g. “Alphabet Inc news AND Fed rate decision”, or retrieving economic indicators).  
  2. **Retrieval:** A Retrieval agent (or tool) fetches information from data sources: real-time market feeds, news APIs, databases, etc. Results include documents or data tables.  
  3. **Filtering:** A Filtering agent ranks and prunes these results by relevance, credibility, and recency. It discards low-quality or duplicate information (e.g. by URL or content similarity【29†L217-L225】【33†L156-L164】).  
  4. **Extraction:** An Extraction agent parses the filtered documents to extract facts, figures, or summaries. For example, it might extract stock price changes, P/E ratios, or key news sentiments【29†L145-L153】. Each fact is labeled with its source and a confidence score.  
  5. **Validation:** A Critic/Validator agent checks these extracted facts for accuracy and consistency, flagging any hallucinations or contradictions【8†L90-L98】. For instance, it may cross-check a quoted earnings figure against the original SEC filing.  
  6. **State Update:** The validated information is stored in the system state (memory) and used to refine subsequent queries. New findings may prompt adjustments to the plan (e.g. a follow-up query).  
  7. **Loop Control:** The cycle repeats until all sub-tasks are addressed or stopping criteria are met (see next section). 

- **Synthesis and Output:** Once research loops conclude, a Synthesis agent combines all collected insights into a coherent report. This includes quantitative analysis (charts, tables) and qualitative summaries. The **Portfolio Analyst** logic applies domain-specific models (risk metrics, factor exposures) to interpret the findings. The final output is a comprehensive investment insight report, with clear explanations and cited sources, ready for decision-making.

**Failure Modes:** If data sources fail or queries return no relevant information, the system may only produce partial insights. For example, an interrupted news feed could lead to stale analysis. The design includes fallback notices (e.g. “data not available”) and encourages user clarification when needed. Loop failures (e.g. endless retrieval of duplicates) are avoided by query tracking and diversification strategies. 

## Data Layer Design

The data layer ingests and processes all necessary information. Key components are:

- **Data Sources:**  
  - *Market Data:* Real-time price feeds and historical data (tick data, OHLCV) for equities, bonds, derivatives. Examples include direct exchange feeds (e.g. ICE, Bloomberg), and APIs like Polygon or Yahoo Finance via an MCP (Model Context Protocol) server【16†L623-L631】. Stored fundamentals (P/E, market cap) come from providers or scraped filings. Macroeconomic indicators are pulled from sources like FRED【16†L623-L631】.  
  - *News:* Financial news and reports from agencies (Reuters, Bloomberg, SEC, company press releases). Ingestion may use RSS/webhooks, news APIs (with deduplication features), or web scraping. Both mainstream media and social sentiment (Twitter/X, Reddit) are included for a 360° view.  
  - *Alternative Data:* Non-traditional signals (satellite imagery, credit card spending, foot traffic, ESG ratings). These are typically batch-loaded from specialized vendors.  

- **Ingestion Strategy:**  
  - *Real-Time Streaming:* High-frequency market data and breaking news use streaming pipelines (e.g. Kafka/Kinesis). For example, as Golden Door notes, a **streaming-first** architecture ingests tick data continuously and applies real-time validation【24†L139-L148】. This provides up-to-the-second intelligence.  
  - *Batch Processing:* Slower data (daily fundamentals, monthly economic releases, historical files) are pulled periodically. Batch ETL jobs normalize and load this data during off-hours.  
  - *Data Pipeline Architecture:* We follow an **ETL** pattern【20†L128-L136】【20†L139-L147】: *Extraction* from diverse sources (APIs, web, databases), *Transformation* (cleaning, deduplicating, standardizing schema), and *Loading* into storage. The pipeline is fault-tolerant and scalable, ensuring data freshness without overloading source systems【20†L139-L147】.

- **Storage Layers:**  
  - *Raw Layer:* All raw ingested feeds are stored (e.g. in a cloud data lake) for auditing and reprocessing.  
  - *Processed Layer:* Cleaned, structured tables (e.g. time-series DB for prices, relational tables for fundamentals) support analytics.  
  - *Vector Store:* Embeddings of text (news articles) and concepts are indexed in a vector database to enable semantic retrieval (for filtering deduplication and similarity searches).  
  - *Serving Layer:* A specialized serving store (databases or in-memory cache) holds the final data for the agents (e.g. an API for latest price and news queries).

- **News Ingestion (Special Focus):** News data is updated frequently to maintain freshness. The system periodically queries sources (e.g. News API) with dynamic keywords. Each cycle:  
  1. **Fetch:** Use keyword queries (like “GOOGL stock news”, “Fed decision tech sector”) to retrieve recent articles.  
  2. **Deduplication:** Compare new articles to recent ones (7-day window) using semantic similarity and edit-distance【33†L156-L164】【33†L174-L182】. Remove near-duplicates or syndicated repeats, keeping the original or highest-quality source.  
  3. **Entity Extraction:** An LLM-based pipeline processes the article text to identify companies mentioned, relevant tickers, sentiments, and key events【31†L31-L39】. It outputs a JSON structure (see example below) with fields like `ticker`, `summary`, `confidence`.  
  4. **Normalization:** Store the cleaned content, summary, and metadata (source, publish date) in the database. Attach a timestamp for recency ranking.

*Example of structured news item after extraction (JSON):*  

```json
{
  "asset_id": "ABC123",
  "symbol": "GOOGL",
  "title": "Alphabet Reports Q1 Earnings Beat Expectations",
  "source": "reuters.com",
  "published_at": "2025-04-02T12:00:00Z",
  "content_text": "Alphabet Inc. (GOOGL) reported first-quarter earnings per share of $...", 
  "summary": "Alphabet’s Q1 earnings exceeded analysts’ expectations, driven by growth in ad revenue and cloud services.",
  "quality_score": 0.92,
  "confidence": 0.89,
  "reasoning": "Revenue growth was primarily due to strong ad performance."
}
```

All such items are indexed (including embeddings of `content_text`) for efficient retrieval in the agent loop.

## Agentic Architecture

The system defines specialized agents (modules) with clear roles, input/output schemas, and prompt strategies. Examples are:

- **Planner Agent**  
  - **Role:** Decompose the high-level user query into specific research tasks.  
  - **Input Schema:** `{"user_query": string, "state": object}`.  
  - **Output Schema:** `{"tasks": [string]}` (e.g. `["Macro economic impact on holdings", "Company fundamentals analysis", ...]`).  
  - **Prompt Strategy:** A system prompt instructs the LLM to break down the problem systematically. For example: *“Given the user’s query and portfolio context, list a sequence of focused analysis tasks needed.”*  

- **Query Generator Agent**  
  - **Role:** Formulate concrete search queries or data requests for each task.  
  - **Input Schema:** `{"task": string}`.  
  - **Output Schema:** `{"search_query": string}` or parameterized API query (e.g. `{"ticker": "GOOGL", "keywords": ...}`).  
  - **Prompt Strategy:** Prompt the model with the task description to generate effective search terms or API call parameters. For instance, *“Generate an effective news search string for: [task]”*.  

- **Retrieval Agent**  
  - **Role:** Fetch information from data sources based on the queries.  
  - **Input Schema:** `{"search_query": string}`.  
  - **Output Schema:** `{"documents": [ {id: string, content: string, metadata: {...}} ]}`.  
  - **Prompt Strategy:** This can be a wrapper that calls tools (e.g. web search API, database query) rather than an LLM prompt. Output is raw text/documents.  

- **Filtering Agent**  
  - **Role:** Filter and rank the retrieved documents.  
  - **Input Schema:** `{"documents": [...], "search_query": string}`.  
  - **Output Schema:** `{"filtered_documents": [ {id, content, metadata} ]}`.  
  - **Prompt Strategy:** Prompt the LLM (or use vector search) to score relevance. E.g., *“From these results, select and justify the ones most relevant to [task query].”* Optionally apply hard filters (date, source) first.  

- **Extraction Agent**  
  - **Role:** Extract structured facts or answers from documents.  
  - **Input Schema:** `{"document": {id, content, ...}, "query": string}`.  
  - **Output Schema:** `{"facts": [ {"fact": string, "source": string} ]}` (or key-value).  
  - **Prompt Strategy:** Use a prompt like: *“Based on this document, extract key facts relevant to [query] as JSON.”* The output should adhere to a predefined JSON schema.  

- **Critic/Validator Agent**  
  - **Role:** Validate extracted information for correctness and consistency.  
  - **Input Schema:** `{"facts": [...], "state": object}`.  
  - **Output Schema:** `{"validated": boolean, "feedback": string}`.  
  - **Prompt Strategy:** The system can instruct the agent to fact-check: *“Review each fact for consistency and credibility. Mark any suspicious entries.”* It may compare with previous facts or known data.  

- **Memory Agent**  
  - **Role:** Manage the system’s memory state (past queries, sources, facts).  
  - **Input Schema:** `{"new_facts": [...], "current_state": object}`.  
  - **Output Schema:** `{"memory_id": string, "updated_state": object}`.  
  - **Prompt Strategy:** Typically implemented as a database/store rather than an LLM prompt. It updates a structured state with new information.  

- **Synthesis Agent**  
  - **Role:** Summarize and combine all findings into a final answer.  
  - **Input Schema:** `{"facts": [...], "portfolio": {...}}`.  
  - **Output Schema:** `{"report": string, "source_refs": [string]}`.  
  - **Prompt Strategy:** Instruct the model: *“Write a concise report combining these findings. Cite sources inline.”* The output is a coherent narrative or bullet-point summary, with references to facts.  

- **Portfolio Analyst Agent**  
  - **Role:** Apply domain logic (risk metrics, sector analysis) to the portfolio using gathered data.  
  - **Input Schema:** `{"holdings": [...], "facts": [...], "market_data": {...}}`.  
  - **Output Schema:** `{"insights": {...}, "recommendations": {...}}`.  
  - **Prompt Strategy:** Provide the model with portfolio composition and key metrics, and prompt for analysis: *“Analyze the portfolio’s risk exposures based on the given holdings and market trends, and suggest adjustments.”*

Below is an example **JSON schema** for some agent I/O (simplified):

```json
{
  "Planner": {
    "input_schema": { "user_query": "string", "state": "object" },
    "output_schema": { "tasks": ["string"] }
  },
  "QueryGenerator": {
    "input_schema": { "task": "string" },
    "output_schema": { "search_query": "string" }
  },
  "Retrieval": {
    "input_schema": { "search_query": "string" },
    "output_schema": { "documents": [ {"id": "string", "text": "string", "source": "string"} ] }
  },
  "Filtering": {
    "input_schema": { "documents": "array", "query": "string" },
    "output_schema": { "filtered_docs": "array" }
  },
  "Extraction": {
    "input_schema": { "document": "object", "query": "string" },
    "output_schema": { "facts": [ {"fact": "string", "source": "string"} ] }
  }
}
```

These schemas guide each agent’s prompt and response formatting to ensure consistency. 

## Multi-Step Research Loop Design

The system uses a controlled loop to iteratively refine knowledge: **Plan → Generate Query → Retrieve → Filter → Extract → Validate → Update State → repeat**. Key elements:

- **Loop Control:** The Planner sets up subtasks. In each loop, the Query Generator may produce multiple queries. The loop continues until all planned tasks are addressed or stopping criteria are met (e.g. no new facts retrieved for several iterations, or a max iteration count).  
- **Stopping Criteria:** Stop if the information gain falls below a threshold (no novel facts), or if all tasks’ questions have been answered. Setting a maximum number of loops prevents infinite cycles.  
- **Failure Handling:** If a cycle yields no relevant results, the system flags a partial failure and can either terminate or attempt alternative strategies (e.g. broaden queries). Loop degeneration is avoided by tracking queries and results history to prevent repeats.  
- **Query Diversification:** The Query Generator purposely creates variations of searches (synonyms, related entities) if initial queries fail. This prevents getting stuck on one wording.  
- **Redundancy Prevention:** The Memory Agent records all previous queries and retrieved documents. Before issuing a new query or accepting a document, the system checks if similar queries or sources were already used【29†L217-L225】. This ensures each loop adds new information.

The overall pattern mimics a human analyst: each cycle answers some sub-questions, then plans the next steps based on updated context. Trace logs (recording each query, tool call, and reasoning) are maintained for auditability【11†L283-L290】【36†L74-L83】.

## State & Memory Design

The agent’s **state** includes:

- **Query History:** All past queries (strings and parameters) to avoid repetition.  
- **Retrieved Sources:** A list of documents or data items already fetched (with IDs/URLs). Used to track coverage and avoid duplicates.  
- **Extracted Facts:** Structured records of all facts collected (each with content, source ID, and a confidence score). This acts like a knowledge base.  
- **Confidence Scores:** Each fact or insight has a score (0.0–1.0) indicating trustworthiness. Scores can be propagated from source authority or model certainty.  
- **Long/Short-Term Context:** Recent dialogue or partial answers are kept in short-term memory (active context), while enduring knowledge (e.g. confirmed ticker mappings, static portfolio info) is in long-term memory (database or embeddings).  
- **Memory Persistence:** State is periodically serialized to a database (e.g. after each completed task). The Memory Agent handles loading relevant past info for new loops.

This design prevents re-asking the same question: before generating a query, the agent checks if a similar fact already exists in memory. Large context is handled by summarizing older content: for example, older chains of reasoning can be condensed into summary notes to keep prompt size manageable. The memory can be a combination of vector indexes (for semantic recall) and key-value stores (for exact records).

## Information Quality Control

We score and filter information along multiple dimensions:

- **Relevance:** How closely an item matches the query (measured by keyword match or embedding similarity). Low-relevance docs are dropped.  
- **Recency:** Newer information is preferred (especially for news). We may assign higher weight to items published after a certain date.  
- **Authority:** Credibility of the source. Trusted sources (e.g. official filings, well-known journals) are scored higher. A news dedup system, for example, identifies the “original” authoritative article【33†L189-L198】.  
- **Novelty:** New facts compared to what’s in memory are prioritized. Redundant info gets a lower novelty score.  
- **Factual Density:** Content rich in verifiable facts scores higher than opinion pieces. This can be approximated by counting data points or named entities.  

**Filtering:** We apply threshold rules on these scores. For example, discard any document below relevance 0.5 or older than 30 days unless directly relevant. We may also require cross-verification: a claimed fact must appear in at least one high-authority source. Noise reduction also involves forcing the agent to output structured JSON (so any hallucinated text that doesn’t fit the schema is caught).

## Synthesis Strategy

To combine the gathered information without hallucination:

- **Map-Reduce Summarization:** First, have each agent (or a dedicated sub-agent) summarize its own domain of facts. Then, feed those intermediate summaries into a final summarizer. This two-step process ensures all subtopics are covered systematically.  
- **Structured Intermediate Outputs:** By keeping facts in structured form (as in the Extraction step), the final composition can be more mechanical. For instance, an LLM can loop over a JSON list of facts and turn them into bullet points or sections.  
- **Grounding in Sources:** The final report must reference source IDs from the fact list. Prompts explicitly require citing sources (e.g. “According to [source], X happened”). This makes the result traceable【11†L239-L242】.  
- **Hallucination Mitigation:** The Critic agent double-checks the final draft against the fact base. Any statement lacking a source is either dropped or flagged. External checks (like regex for numerical consistency) can be applied.  
- **Traceability:** Every statement in the synthesis has an associated fact entry ID. This way, users (or auditors) can follow each insight back to the original data point or document.

## Portfolio Insight Engine

This domain-specific component applies financial logic to generate actionable insights:

- **Risk Analysis:** Compute portfolio risk metrics (e.g. value-at-risk, max drawdown, beta relative to benchmarks). The LLM interprets these (“Your portfolio’s VaR suggests a potential 5% loss under current volatility”). The system can simulate stress scenarios, using sources to justify assumptions.  
- **Macro Exposure:** Analyze sensitivity to macro factors. For instance, if all holdings are in tech, a Fed rate hike may disproportionately affect it. The engine quantifies this (e.g. % of value in rate-sensitive sectors) and prompts the model to explain.  
- **Sector/Allocation Assessment:** Break down holdings by sector, asset class, or geography. Compare to target allocations. If biotech is overweight, the agent explains possible implications with evidence.  
- **Scenario Analysis:** Model portfolio performance under hypothetical events (rate cuts, earnings surprises). The system might retrieve analogous historical cases and use them to inform the LLM’s reasoning.  
- **Integration of Quantitative Signals:** The engine feeds numerical signals (e.g. price momentum, P/E ratios) into the analysis. The LLM can incorporate exact figures by receiving them in the prompt (or via a custom Python tool) to explain, e.g. “Given GOOG’s P/E of X, the model suggests it may be overvalued relative to the market.”  

By combining LLM-based narrative with quantitative models, the output links data-driven results with natural-language insights.

## Bottlenecks & Challenges

Real-world deployment faces:

- **Loop Degeneration:** Agents might enter cyclical searches without progress if queries repeat or if information is scarce. *Mitigation:* Maintain a query history, diversify queries, and enforce loop limits.  
- **Noisy Search Results:** Generic web searches can yield irrelevant data. *Mitigation:* Use domain-specific sources and strict filters. For example, use specialized news APIs with deduplication【26†L63-L70】【33†L156-L164】.  
- **Stale Data:** Delays in data ingestion (especially for macro releases) may make analysis outdated. *Mitigation:* Implement real-time feeds (e.g. Kinesis), and clearly label any time-sensitive conclusions.  
- **Evaluation Difficulty:** Hard to quantify quality of insights (there is no single “ground truth”). *Mitigation:* Use rigorous evaluation framework (below) with automated metrics and human review loops.  
- **Latency and Cost:** Multi-agent systems and LLM calls are resource-intensive. *Mitigation:* Parallelize independent tasks, use smaller models for sub-tasks, and cache repeatable computations. 

## Evaluation Framework

We measure system performance on:

- **Factual Correctness:** Compare agent output against verified data. This can use automated scorers or human auditors to check if stated facts match sources.  
- **Reasoning Quality:** Use multi-critique evaluation: have separate “judge” agents or experts evaluate the argumentation. For instance, one LLM can check logical coherence, another can verify instructions were followed. Anthropic-style evals define tasks and multiple gradings per trial【36†L74-L83】.  
- **Completeness:** Assess if the answer covers all required aspects (e.g. did it address each sub-task?). This can be scored by checklist validation or LLM graders.  
- **Multi-Critic Validation:** Employ multiple evaluators (e.g. an LLM grader, a rules-based checker, and a human) to robustly assess outputs, similar to Anthropic’s multi-grader strategy【36†L74-L83】.  

In practice, we define test cases with expected topics (like specific risk factors) and run the agent. The final answers are scored on presence/accuracy of those topics. We log all reasoning traces for audit. Over time, the team collects metrics (precision/recall of facts, average confidence) to guide improvements.

**References:** This design draws on recent research and best practices. The multi-agent structure (Figure 1) and “agents as tools” pattern are from OpenAI’s multi-agent finance example【16†L602-L610】【45†L0-L0】. Quotient AI’s tutorial highlights traceability and tool usage to ground answers【8†L75-L84】【11†L239-L242】. Financial news processing via LLMs is adapted from an academic study【31†L31-L39】. Industry data pipeline patterns (streaming ingestion, Kafka, Spark) are exemplified by Golden Door’s architecture【24†L139-L148】. Each cited source informed a piece of this system design.