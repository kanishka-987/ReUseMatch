# ReUseMatch Architecture

ReUseMatch is an autonomous multi-agent platform designed to drive the circular economy by facilitating item evaluation, need matching, and routing for reuse. This document provides a high-level overview of the architectural layers and components.

## Architecture Diagram

```mermaid
graph TB
    subgraph Frontend Layer
        UI[Vanilla HTML/CSS/JS App]
    end

    subgraph Backend Layer (FastAPI)
        API[API Routers /routes]
        Service[Services Layer /services]
        Models[SQLAlchemy Models /models]
    end

    subgraph Orchestration Layer
        Orch[Coordinator Orchestrator]
    end

    subgraph Agent Layer
        OA[Object Agent]
        CA[Condition Agent]
        NA[Need Agent]
        LA[Logistics Agent]
    end

    subgraph Database Layer
        DB[(MySQL Database)]
    end

    UI <-->|REST API / HTTP| API
    API <--> Service
    Service <--> Models
    Models <-->|SQLAlchemy / PyMySQL| DB
    Service <--> Orch
    Orch --> OA
    Orch --> CA
    Orch --> NA
    Orch --> LA
```

---

## Architectural Layers

### 1. Frontend Client
- **Tech Stack**: HTML5, CSS3 (Vanilla design system), Vanilla JavaScript (modules/fetch).
- **Functionality**:
  - Provides a Donor Dashboard to submit items.
  - Features an **Agent Execution Monitor** that tracks active and completed stages in the agent pipeline.
  - Displays match recommendations, highlighting location, recommended delivery routes, and quality evaluation scores.

### 2. Backend API
- **Tech Stack**: FastAPI, Uvicorn, Pydantic, Python-dotenv.
- **Functionality**:
  - Receives item submissions.
  - Manages database transactions.
  - Passes incoming submissions to the **Orchestration Layer** and returns matched results.

### 3. Orchestration Layer
- **Tech Stack**: Pure Python.
- **Functionality**:
  - Manages sequential/parallel processing of the agents.
  - Acts as the workflow controller, passing the output of previous steps into subsequent agents (e.g. Object Agent output is passed to the Condition Agent).
  - Determines final ranking/matches based on compiled results.

### 4. Agent Layer
- **Tech Stack**: Python, LangChain / LLM APIs (when implemented).
- **Structure**:
  - **Object Agent**: Identifies type, description, and keywords.
  - **Condition Agent**: Calculates condition tier and structural grade.
  - **Need Agent**: Matches item traits against registry databases.
  - **Logistics Agent**: Evaluates routing, distance, cost, and logistics mode.

### 5. Database Layer
- **Tech Stack**: MySQL, SQLAlchemy (ORM), PyMySQL (Driver).
- **Functionality**:
  - Stores user submissions, item listings, non-profit profile records, matching transactions, and audit logs.
  - Connection pooling managed in `database/connection.py`.
