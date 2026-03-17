# 🚀 Market Intelligence Multi-Agent System

An industry-aligned **LLM-powered multi-agent system** that generates structured **market intelligence reports** by combining:

- Real-time news
- Financial data
- Retrieval-Augmented Knowledge (RAG)
- LLM-based reasoning

---

## 🧠 Overview

This project demonstrates a **production-style AI system design** using:

- Multi-agent architecture  
- LangGraph orchestration  
- Tool-augmented LLM reasoning  

The system takes a **company name as input** and generates a **market insight report**.

---

## ⚙️ Architecture

User → FastAPI → LangGraph → Agents → LLM → Response  

### Workflow

1. Coordinator agent decides tool usage  
2. News agent fetches latest news  
3. Financial agent retrieves financial data  
4. Vector retrieval (FAISS) fetches relevant knowledge  
5. Analysis agent performs reasoning  
6. Strategy agent generates final report  

---

## 🧩 Tech Stack

- FastAPI  
- LangGraph  
- Groq (LLM)  
- HuggingFace Embeddings  
- FAISS (Vector DB)  
- Docker  

---

## 📁 Project Structure

app/  
├── agents/  
├── api/  
├── config/  
├── prompts/  
├── schemas/  
├── services/  
├── tools/  
├── workflows/  
└── main.py  

data/  
docker/
system_design.md   

---

## 🔍 Key Features

- Multi-agent orchestration using LangGraph  
- Tool-based reasoning (news + financial data)  
- Retrieval-Augmented Generation (RAG)  
- Modular and scalable architecture  
- Prompt-driven LLM workflows  

---

## 🏗️ System Design

For detailed architecture, data flow, and design decisions:

➡️ Refer to: [system_design.md](system_design.md)

---

## 🚀 Getting Started

### 1. Clone the repository

git clone <your-repo-url>  
cd market-intelligence-agent  

---

### 2. Create virtual environment

python -m venv venv  

Windows:  
venv\Scripts\activate  

Linux/Mac:  
source venv/bin/activate  

---

### 3. Install dependencies

pip install -r requirements.txt  

---

### 4. Setup environment variables

Create a `.env` file:

GROQ_API_KEY=your_api_key  
MODEL_NAME=llama3-8b-8192  

---

### 5. Run the application

uvicorn app.main:app --reload  

---

### 6. Test API

Open:  
http://127.0.0.1:8000/docs  

---

## 📤 Example Input

{
  "company": "Apple",
  "question": "Analyze market outlook"
}

---

## 📈 Example Output

{
  "analysis": "...",
  "final_report": {
    "market_outlook": "...",
    "opportunities": "...",
    "risks": "..."
  }
}

---

## ⚠️ Limitations

- Depends on external APIs for news and financial data  
- LLM responses may vary based on prompts and model behavior  
- Not optimized for large-scale production deployment  

---

## 🎯 What This Project Demonstrates

- Multi-agent AI system design  
- LLM orchestration using LangGraph  
- Practical application of RAG  
- Clean and modular backend architecture  

---

## 👨‍💻 Author

Nithin Gowda P  
Aspiring AI/ML Engineer  

---