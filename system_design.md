# Market Intelligence Multi-Agent System

## 1. Problem Statement

The goal is to build an AI-powered system that generates **market intelligence reports** for a given company by combining:

- Latest news
- Financial data
- External knowledge (RAG)
- LLM-based reasoning

---

## 2. High-Level Architecture

User → FastAPI → LangGraph Orchestrator → Agents → LLM → Response

### Detailed Flow

User Query  
↓  
FastAPI Endpoint  
↓  
Coordinator Agent (LLM decides tools)  
↓  
News Agent  
↓  
Financial Agent  
↓  
Vector Retrieval (FAISS)  
↓  
Analysis Agent (LLM reasoning)  
↓  
Strategy Agent (Final report)  
↓  
Response (JSON)

---

## 3. Core Components

### 3.1 API Layer
- Built using FastAPI
- Handles user requests and returns structured JSON responses

---

### 3.2 Orchestration Layer (LangGraph)
- Manages workflow between agents
- Maintains shared state
- Supports conditional routing (ReAct-style planning)

---

### 3.3 Agents

**Coordinator Agent**
- Uses LLM to decide which tools to use
- Implements dynamic planning

**News Agent**
- Fetches latest company news using API

**Financial Agent**
- Retrieves financial metrics

**Analysis Agent**
- Combines:
  - News
  - Financial data
  - Retrieved knowledge
- Performs reasoning using LLM

**Strategy Agent**
- Generates final structured report:
  - Market outlook
  - Opportunities
  - Risks

---

### 3.4 Tool Layer

- news_api_tool → fetch news  
- financial_api_tool → fetch financial data  
- vector_retrieval_tool → retrieve company knowledge  

---

### 3.5 Vector Database (FAISS)

- Stores embedded company knowledge
- Enables semantic search
- Used as a lightweight RAG system

---

### 3.6 LLM Layer

- Centralized via llm_service
- Used for:
  - Planning (Coordinator)
  - Reasoning (Analysis)
  - Report generation (Strategy)

---

## 4. Data Flow

1. User provides company name  
2. Coordinator agent decides tool usage  
3. Tools fetch:
   - News data
   - Financial data  
4. Vector database retrieves relevant company knowledge  
5. Analysis agent synthesizes insights  
6. Strategy agent generates final report  

---

## 5. Design Decisions

| Decision | Reason |
|--------|--------|
| Multi-agent architecture | Separation of concerns |
| LangGraph | State management + orchestration |
| Prompt templates | Maintainability |
| FAISS vector DB | Lightweight and fast retrieval |
| LLM service layer | Reusability |

---

## 6. Scalability Considerations

- Agents can be parallelized  
- Replace FAISS with managed DB (Pinecone / Weaviate)  
- Deploy using Docker + Kubernetes  
- Add caching layer (Redis) for repeated queries  

---

## 7. Trade-offs

| Choice | Trade-off |
|------|--------|
| FAISS (local) | Not distributed |
| LLM API | Latency + cost |
| Sequential pipeline | Slight delay vs parallel execution |

---

## 8. Future Improvements

- Add caching layer (Redis)  
- Add monitoring (logging + tracing)  
- Replace FAISS with scalable vector DB  
- Add streaming responses  
- Introduce feedback loop for model improvement  

---

## 9. Key Learnings

- Multi-agent system design  
- LLM orchestration using LangGraph  
- Retrieval-Augmented Generation (RAG)  
- Prompt engineering  
- API + deployment architecture  

---