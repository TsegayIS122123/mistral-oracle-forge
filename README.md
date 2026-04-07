# 🔮 Mistral Oracle Forge

## Production Data Analytics Agent for Multi-Database Workloads
 Production-grade data analytics agent for multi-database workloads. Team Mistral submission for The Oracle Forge challenge
## What This Agent Does

This agent answers complex business questions across **multiple databases** — PostgreSQL, MongoDB, SQLite, DuckDB — something most AI agents cannot do reliably.

**Example capability:**
> *"Which customer segments had declining repeat purchase rates in Q3, and does that pattern correlate with support ticket volume in our CRM?"*

The agent navigates transaction DB + CRM DB, resolves inconsistent customer IDs, extracts structured data from unstructured notes, and produces a verifiable answer.

---

## Architecture
```mermaid
flowchart TB
    User(["👤 User Question"])

    subgraph AGENT["🤖 MISTRAL ORACLE FORGE AGENT"]
        direction TB
        
        subgraph KB["📚 KNOWLEDGE BASE (Karpathy Method)"]
            L1["Layer 1: Schema & Metadata<br/>kb/domain/schema.md"]
            L2["Layer 2: Institutional Knowledge<br/>kb/domain/join-glossary.md"]
            L3["Layer 3: Corrections Log<br/>kb/corrections/corrections-log.md"]
        end

        subgraph CORE["⚙️ CORE ENGINE"]
            R["Query Router"]
            G["Query Generator"]
            J["Join Resolver"]
        end

        subgraph LOOP["🔄 SELF-CORRECTION LOOP"]
            F["Detect Failure"]
            LOG["Log to KB v3"]
        end
    end

    subgraph MCP["🔌 MCP TOOLBOX"]
        PG[("PostgreSQL")]
        MG[("MongoDB")]
        SL[("SQLite")]
        DK[("DuckDB")]
    end

    subgraph EVAL["📊 EVALUATION HARNESS"]
        T["Query Trace"]
        S["Score Log"]
        REG["Regression Suite"]
    end

    subgraph OUTPUT["✅ OUTPUT"]
        ANS["Answer"]
        TRACE["Execution Trace"]
    end

    User --> R
    KB --> R
    KB --> G
    KB --> J
    
    R --> G
    G --> MCP
    MCP --> PG & MG & SL & DK
    
    PG --> J
    MG --> J
    SL --> J
    DK --> J
    
    J -->|Success| OUTPUT
    J -->|Failure| F
    F --> LOG
    LOG --> KB
    
    J --> EVAL
    EVAL --> T & S & REG
    
    OUTPUT --> ANS
    OUTPUT --> TRACE

    style KB fill:#3498db,color:#fff
    style CORE fill:#2ecc71,color:#fff
    style LOOP fill:#e74c3c,color:#fff
    style MCP fill:#9b59b6,color:#fff
    style EVAL fill:#f39c12,color:#fff
    style OUTPUT fill:#1abc9c,color:#fff
```

---

## Three Context Layers

| Layer | What It Contains | Where |
|-------|-----------------|-------|
| **Layer 1** | Schema & metadata from all databases | `kb/domain/schema.md` |
| **Layer 2** | Institutional knowledge (what "revenue" means, authoritative tables) | `kb/domain/` |
| **Layer 3** | Interaction memory (past corrections, successful patterns) | `kb/corrections/` |

---

## Project Structure
```bash
mistral-oracle-forge/
│
├── agent/ # Core agent code
│ ├── AGENT.md # Context file (loaded at session start)
│ ├── tools.yaml # MCP database connections
│ ├── main.py # Entry point
│ ├── query_router.py # Routes to correct database
│ ├── db_connector.py # Database connections
│ ├── join_resolver.py # Fixes format mismatches
│ └── requirements.txt # Python dependencies
│
├── kb/ # Knowledge Base (Karpathy method)
│ ├── architecture/ # Claude Code, OpenAI patterns
│ ├── domain/ # Schema, join keys, unstructured fields
│ ├── evaluation/ # DAB format, scoring
│ └── corrections/ # Self-learning log
│
├── eval/ # Evaluation harness
│ ├── harness.py # Main evaluation script
│ ├── score_log.md # Score improvement tracking
│ ├── regression_suite.py # Regression tests
│ └── held_out_queries.json # Test set
│
├── probes/ # Adversarial probes
│ └── probes.md # 15+ probes, 4 failure categories
│
├── planning/ # AI-DLC documentation
│ ├── inception.md # Press release, FAQ, definition of done
│ ├── approvals.md # Team gate approvals
│ └── mob-session-log.md # Daily mob session records
│
├── utils/ # Shared utilities
│ ├── retrieval_helper.py # Multi-pass retrieval
│ ├── schema_introspector.py # Schema discovery
│ ├── benchmark_wrapper.py # DAB benchmark runner
│ └── README.md
│
├── signal/ # Signal Corps outputs
│ ├── engagement_log.md # All posts and metrics
│ └── community_log.md # Reddit/Discord/X interactions
│
├── results/ # Benchmark results
│ └── (DAB results JSON)
│
├── scripts/ # Automation scripts
│ └── setup.sh # One-command setup
│
├── .github/workflows/ # CI/CD
│ └── ci.yml # Minimal CI
│
├── README.md # This file
├── .gitignore
├── .env.example
└── docker-compose.yml

```

---

## Quick Start

### Prerequisites

- Python 3.10+
- Docker (optional, for sandbox)
- Tailscale (for team server access)

### One-Command Setup

```bash
# Clone and setup
git clone https://github.com/TsegayIS122123/mistral-oracle-forge
cd mistral-oracle-forge
chmod +x scripts/setup.sh
./scripts/setup.sh