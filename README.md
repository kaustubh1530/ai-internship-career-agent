#  AI Internship Career Agent (RAG + Hybrid AI Matching)

An AI-powered job search assistant that uses **Retrieval-Augmented Generation (RAG)** and **LLMs** to match users with real-time internship opportunities based on skills and semantic understanding.

---

## Overview

This project simulates a real-world AI system used in modern job platforms.

It:
- Fetches live job listings from APIs
- Converts them into embeddings (vector database)
- Uses semantic search to find relevant jobs
- Applies skill-based scoring for precise matching
- Displays results in an interactive UI

---

## Key Features

-  **Live Job Fetching** (Adzuna API)
-  **RAG-based Semantic Search** (FAISS Vector DB)
-  **OpenAI Skill Intelligence**
-  **Hybrid Ranking System**
  - Semantic similarity (AI)
  - Skill matching (rule-based)
-  **Skill Gap Analysis**
-  **Interactive Dashboard (Streamlit)**
-  Direct job application links

---

##  System Architecture

Adzuna API → Job Data
↓
Embedding Model (OpenAI)
↓
FAISS Vector Database
↓
User Query → Embedding
↓
Semantic Retrieval (RAG)
↓
Skill Matching Engine
↓
Hybrid Ranking
↓
Streamlit UI (Final Output)


---

##  Tech Stack

- **Python**
- **OpenAI API**
- **FAISS (Vector Database)**
- **Streamlit (UI)**
- **Adzuna API**
- NumPy / JSON

---

##  How It Works

1. Fetch real-time job listings  
2. Convert jobs into embeddings using OpenAI  
3. Store embeddings in FAISS vector database  
4. Convert user query into embedding  
5. Perform semantic search (RAG)  
6. Apply skill-based scoring  
7. Rank jobs using hybrid AI system  
8. Display results in UI  

---

##  Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Step 1: Fetch jobs
python3 fetch_jobs.py

# Step 2: Create embeddings (RAG)
cd rag_system
python3 create_embeddings.py

# Step 3: Run app
cd ../final_app
streamlit run app.py


Example

Input:
    Query: AI internship
    Skills: python, fastapi, git

Output:
    Top ranked jobs
    Match scores (%)
    Matched skills
    Missing skills
    Apply links

##  Demo Proof
![Fetch Jobs](assets/fetch.png)
![Results](assets/results.png)
![Demo](assets/demo.gif)

Why This Project Matters
This project demonstrates real-world AI engineering concepts:

Retrieval-Augmented Generation (RAG)
Vector databases (FAISS)
LLM integration in production workflows
Hybrid ranking systems
End-to-end AI application development

 This is similar to how:
    AI job platforms work
    Resume screening systems operate
    Intelligent search engines are built
    Key Highlight

Built a Hybrid AI Ranking System combining:
    Semantic similarity (RAG)
    Skill-based matching

Author
Kaustubh Patil