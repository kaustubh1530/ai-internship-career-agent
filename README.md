# 🚀 AI Career Intelligence System

A startup-style AI career platform that analyzes resumes, refreshes live job listings, ranks jobs using semantic AI matching, and provides personalized career recommendations through a multi-agent AI system.

This project is built as a flagship AI + backend engineering portfolio project using Python, Streamlit, OpenAI, LangChain, embeddings, live job APIs, and multi-agent orchestration.

---

## Project Overview

The **AI Career Intelligence System** helps users:

- Upload a resume PDF
- Extract skills from the resume
- Refresh live job listings from a job API
- Rank jobs using semantic similarity and skill matching
- View explainable job matches with match scores
- Get AI-powered career advice
- Understand skill gaps and next steps

This is not just a chatbot.  
It is a full AI system with agents, memory, decision logic, semantic matching, and a product-style Streamlit interface.

---

## Key Features

### Resume Intelligence

- Upload resume as PDF
- Extract resume text
- Identify skills from the resume
- Use resume content for AI job matching and career advice

### Live Job Refresh

- Fetch fresh job listings using Adzuna API
- Save live jobs into a structured local data layer
- Automatically rebuild job embeddings after refreshing jobs
- Use updated job data during analysis

### Multi-Agent AI System

The system uses multiple agents with shared state and communication:

- **Resume Agent**  
  Extracts skills and profile strengths from the resume.

- **Job Agent**  
  Loads jobs, performs semantic matching, scores jobs, removes duplicates, and selects top matches.

- **Advisor Agent**  
  Generates personalized career recommendations based on resume, skills, and job matches.

- **Strategy Agent**  
  Provides fallback career strategy when job matches are weak.

- **Decision Agent**  
  Evaluates output quality and supports intelligent retry decisions.

### Agent-to-Agent Communication

Agents communicate using a shared message system.


## Screenshots

### Profile Section
![Profile](assets/profile.png)

### Resume Upload
![Resume](assets/resume.png)

### Job Matches
![Match1](assets/match1.png)
![Match2](assets/match2.png)

### AI Insights
![Insights](assets/insights.png)

### Career Advice
![Insights](assets/career_advice.png)
---

## Demo
### Full App Walkthrough
![Demo](assets/demo.gif)
---

Example:

```text
ResumeAgent → JobAgent: User skills extracted
JobAgent → AdvisorAgent: Top semantic job matches ready 

### Semantic Job Matching

The app uses OpenAI embeddings and cosine similarity to compare resume meaning with job descriptions.

Instead of only checking exact words, the system understands semantic similarity.

Example:

Resume: backend APIs, Python, FastAPI
Job: build scalable web services


### System Architecture

User Uploads Resume
        ↓
Resume Parser
        ↓
Resume Agent
        ↓
Shared Agent State
        ↓
Job Agent
        ↓
Semantic Matching Engine
        ↓
Advisor Agent / Strategy Agent
        ↓
Decision Agent
        ↓
Streamlit Product UI


### Project Structure

ai-internship-career-agent/
│
├── ai_agents/
│   ├── base.py
│   ├── state.py
│   ├── orchestrator.py
│   └── agents/
│       ├── resume_agent.py
│       ├── job_agent.py
│       ├── advisor_agent.py
│       ├── strategy_agent.py
│       ├── feedback_agent.py
│       └── decision_agent.py
│
├── ai_langchain/
│   ├── chains/
│   │   ├── resume_chain.py
│   │   ├── job_chain.py
│   │   └── advisor_chain.py
│   ├── prompts/
│   │   ├── resume_prompt.py
│   │   ├── job_prompt.py
│   │   └── advisor_prompt.py
│   └── utils/
│       └── llm.py
│
├── backend/
│   ├── resume_parser.py
│   ├── job_data_source.py
│   ├── live_job_fetcher.py
│   ├── embedding_utils.py
│   ├── build_job_embeddings.py
│   ├── job_embeddings.json
│   └── memory_utils.py
│
├── data/
│   └── live_jobs.json
│
├── final_app/
│   └── app.py
│
├── smart_agent.py
├── requirements.txt
├── runtime.txt
├── .env.example
├── .gitignore
└── README.md

## Setup & Installation

### Clone & Environment

git clone https://github.com/kaustubh1530/ai-internship-career-agent.git
cd ai-internship-career-agent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

### Configuration

Create a .env file in the root directory:

Code snippet
OPENAI_API_KEY=your_openai_key
ADZUNA_APP_ID=your_adzuna_id
ADZUNA_APP_KEY=your_adzuna_key

### Run Application

streamlit run final_app/app.py
---


Example User Flow
Upload: User drops a PDF resume into the app.

Refresh: The app pulls live "Software Engineering" jobs in "Maryland."

Analyze: The Resume Agent extracts technical skills.

Rank: The Job Agent finds the best semantic matches.

Advise: The Advisor Agent suggests skill improvements and career steps.

What I Learned
Designing multi-agent workflows with shared state management.

Implementing semantic search using high-dimensional vector embeddings.

Integrating live third-party APIs into AI-driven decision engines.

Building "Explainable AI" to build user trust in recommendations.

👤 Author

Kaustubh Patil

Computer Science student focused on software engineering, backend development, and AI-powered applications.
