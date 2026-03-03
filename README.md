# 🎓 EduAI Connect

**AI-Powered Education Analytics Platform**

EduAI Connect helps teachers proactively identify at-risk students using AI-driven insights. It connects to school platforms like Canvas LMS, analyzes student performance data using RAG, and delivers actionable recommendations — all while maintaining strict FERPA compliance.

![Architecture Diagram](architecture/system-architecture.png)

---

## The Problem

Teachers spend hours manually reviewing fragmented data across systems like Canvas and PowerSchool. Insights tend to be reactive rather than proactive. By the time a struggling student is identified, it's often too late for effective intervention.

## The Solution

An AI system that:
- Analyzes student grades, attendance, and engagement in real-time
- Proactively flags at-risk students with risk levels (high/medium/low)
- Recommends specific interventions for each student
- Lets teachers ask natural language questions about their class
- Protects student privacy with FERPA-compliant guardrails

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| AI/ML | Amazon Bedrock (Claude 3 Sonnet, Titan Embeddings) |
| RAG Framework | LangChain 0.3, LCEL |
| Agent Orchestration | LangGraph (StateGraph) |
| Vector Store | FAISS |
| API Backend | FastAPI |
| Dashboard | Streamlit |
| Infrastructure | AWS CDK (Python) |
| Security | Bedrock Guardrails, KMS, IAM, CloudTrail |
| Data Sources | Canvas LMS API format (synthetic) |

---

## Architecture

**Data Flow:** Canvas LMS → EventBridge → Lambda → S3 (KMS Encrypted) → Titan Embeddings → FAISS → LangChain LCEL → Bedrock Claude → Guardrails → FastAPI → Streamlit

**Agent Orchestration:** START → Grading Agent → At-Risk Agent → END (LangGraph StateGraph with shared state)

### Key Architecture Decisions

- **RAG over Fine-Tuning:** Student data stays in FAISS/S3, never baked into model weights. Supports FERPA requirements for data deletion, auditing, and access control.
- **LangGraph over Simple Functions:** Shared state between agents enables grading analysis to inform risk assessment. Easy to add new agents (attendance, intervention tracking).
- **FAISS for Dev, OpenSearch for Prod:** FAISS is free and fast for development. CDK stack is designed for OpenSearch Serverless swap in production.
- **FastAPI + Streamlit:** Separates AI logic from UI. Same API serves dashboard, mobile apps, or third-party integrations.

---

## Features

### RAG Pipeline
- Document loader converts student JSON into LangChain Documents
- Titan Embeddings (1536-dimensional vectors) indexed in FAISS
- Query transformation rewrites vague questions into targeted search queries
- Re-ranking ensures most relevant student profiles come first
- Conversational memory for follow-up questions

### Multi-Agent System
- **Grading Agent:** Analyzes grade trends, identifies low scores, flags concerns
- **At-Risk Agent:** Combines grades + attendance + engagement to assign risk levels with recommended actions
- **Orchestrator:** LangGraph StateGraph chains agents sequentially with shared state

### API Endpoints
- `POST /chat` — General RAG Q&A about student performance
- `POST /insights/grading` — Grade analysis powered by Grading Agent
- `POST /insights/at-risk` — At-risk detection powered by At-Risk Agent
- `GET /health` — Health check

### FERPA Compliance
- Bedrock Guardrails filter PII (SSNs blocked, names anonymized by role)
- KMS encryption at rest with automatic key rotation
- TLS 1.2+ for all data in transit
- IAM least-privilege (no wildcard permissions)
- CloudTrail audit logging for all Bedrock API calls
- Synthetic data only — no real student data in development

---

## Quick Start

### Prerequisites
- Python 3.11+
- AWS CLI configured with Bedrock access
- Bedrock model access enabled (Claude 3 Sonnet, Titan Embeddings v1)

### Install
```bash
git clone https://github.com/jaythagreat1/eduai-connect.git
cd eduai-connect
pip install boto3 langchain langchain-aws langchain-community langgraph faiss-cpu streamlit fastapi uvicorn faker "numpy<2"
```

### Generate Synthetic Data
```bash
python3 src/etl/generate_data.py
```

### Build Vector Store
```bash
python3 src/rag/vector_store.py
```

### Run the API
```bash
uvicorn src.api.main:app --reload
```

### Run the Dashboard (new terminal)
```bash
streamlit run streamlit_app/app.py
```

Open http://localhost:8501 and start asking questions.

---

## Sample Queries

| Question | What It Does |
|----------|-------------|
| "Who needs help in Math?" | Finds students with low Math grades |
| "Which students are at risk?" | Runs full at-risk analysis with risk levels |
| "Tell me about Jessica Wallace" | Returns full student profile with grades and trends |
| "What about her attendance?" | Follow-up using conversational memory |
| "How is my class doing overall?" | Class-wide performance summary |

---

## Project Structure
```
eduai-connect/
├── data/                    # Synthetic student data (Canvas API format)
│   ├── students.json
│   ├── courses.json
│   ├── assignments.json
│   └── submissions.json
├── faiss_index/             # FAISS vector embeddings
├── src/
│   ├── etl/
│   │   └── generate_data.py      # Faker data generator
│   ├── rag/
│   │   ├── document_loader.py    # JSON → LangChain Documents
│   │   ├── vector_store.py       # FAISS + Titan Embeddings
│   │   ├── rag_chain.py          # LCEL chain with memory
│   │   ├── query_transform.py    # HyDE query rewriting
│   │   └── reranker.py           # LLM-based re-ranking
│   ├── agents/
│   │   ├── grading_agent.py      # LangGraph grading analysis
│   │   ├── at_risk_agent.py      # LangGraph risk detection
│   │   └── orchestrator.py       # Multi-agent orchestrator
│   ├── api/
│   │   └── main.py               # FastAPI endpoints
│   └── guardrails/
│       └── bedrock_guardrails.py # FERPA PII filtering
├── streamlit_app/
│   └── app.py                    # Teacher dashboard
├── terraform/
│   └── main.py                   # AWS CDK stack
├── notebooks/
│   └── rag_evaluation.ipynb      # RAG pipeline evaluation
└── docs/
    └── FERPA_COMPLIANCE.md       # Compliance documentation
```

---

## Security

See [FERPA_COMPLIANCE.md](docs/FERPA_COMPLIANCE.md) for full compliance documentation.

| Control | Implementation |
|---------|---------------|
| Encryption at Rest | KMS with auto key rotation |
| Encryption in Transit | TLS 1.2+ |
| Access Control | IAM least-privilege, role-based |
| PII Protection | Bedrock Guardrails |
| Audit Trail | CloudTrail + CloudWatch |
| Data Privacy | Synthetic data only, no real student data |


---

## Built With

Amazon Bedrock • LangChain • LangGraph • FAISS • FastAPI • Streamlit • AWS CDK • Python

---

*Built by Johnathan Horner*
