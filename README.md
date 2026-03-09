# 🪐 Orion AI Platform

**Enterprise AI Operating System**

Orion 是一个 **企业级 AI 平台框架**，用于构建：

* RAG 知识库问答
* AI Agent 工作流
* 企业 AI Copilot
* AI 工具调用
* 多模型统一网关

适用于：

* 🏦 银行
* 💰 金融机构
* 🏢 企业知识库
* 🤖 AI Copilot
* 📊 智能业务系统

---

# ✨ Core Features

## 🧠 RAG Engine

高性能企业级 **Retrieval Augmented Generation**：

* Vector Search
* Hybrid Search
* Reranking
* Context Builder
* Multi-source Knowledge

---

## 🤖 Agent Workflow

基于 **LangGraph** 构建的 Agent 状态机：

* Query Analysis
* Planning
* Tool Calling
* Retrieval
* Reflection
* Final Generation

支持：

* Multi-step Reasoning
* Tool Invocation
* Autonomous Decision

---

## 📚 Enterprise Knowledge Base

支持多数据源：

* PDF
* Word
* Excel
* Web Pages
* OCR 文档
* API Data

能力：

* 文档解析
* Chunking
* Embedding
* Metadata 管理

---

## 🧰 AI Gateway

统一 AI 模型管理：

* Model Routing
* Token Control
* Cost Guard
* Rate Limiting
* API Key 管理

支持：

* OpenAI
* Zhipu
* Local LLM
* Future models

---

## 📊 Observability

AI 可观测性：

* LLM Trace
* Prompt Logs
* Latency Metrics
* Token Usage
* Cost Monitoring

---

# 🏗 System Architecture

```
                    ┌──────────────────────────┐
                    │        AI Gateway        │
                    │  Model Router / Guard    │
                    └────────────┬─────────────┘
                                 │
                        ┌────────▼────────┐
                        │       API       │
                        │     FastAPI     │
                        └────────┬────────┘
                                 │
       ┌─────────────────────────▼────────────────────────┐
       │                     AI Engine                    │
       │                                                  │
       │ Query → Retrieve → Rerank → Generate             │
       │ Agent → Planner → Tools                          │
       │                                                  │
       └──────────────┬───────────────┬───────────────────┘
                      │               │
            ┌────────▼───────┐  ┌────▼─────────┐
            │ Knowledge Base │  │   Workflow   │
            │  Vector Store  │  │  LangGraph   │
            └────────┬───────┘  └────┬─────────┘
                     │               │
              ┌──────▼──────────────▼─────┐
              │         Infra Layer       │
              │  LLM / DB / Redis / OCR   │
              └───────────────────────────┘
```

---

# ⚙️ Technology Stack

| Layer         | Technology      |
| ------------- | --------------- |
| API           | FastAPI         |
| Agent         | LangGraph       |
| LLM Framework | LangChain       |
| Vector DB     | Chroma / Milvus |
| Database      | PostgreSQL      |
| Cache         | Redis           |
| OCR           | RapidOCR        |
| Queue         | Celery          |
| Tracing       | LangSmith       |
| Container     | Docker          |

---

# 📂 Project Structure

```
orion-ai-platform/
│
├── app/
│
├── api/
│
├── engine/
│
├── knowledge/
│
├── workflows/
│
├── infra/
│
├── observability/
│
├── evaluation/
│
└── studio/
```

完整结构见项目目录。

---

# 🚀 Quick Start

## 1 Install Dependencies

```
pip install -r requirements.txt
```

---

## 2 Configure Environment

```
OPENAI_API_KEY=
ZHIPU_API_KEY=
REDIS_URL=
POSTGRES_URL=
```

---

## 3 Start Service

```
uvicorn app.main:app --reload
```

访问：

```
http://localhost:8000
```

---

# 📡 API Example

## Chat API

```
POST /v1/chat
```

Request

```json
{
  "query": "虚拟信用卡可以提现吗？",
  "knowledge_base": "banking"
}
```

Response

```json
{
  "answer": "虚拟信用卡通常仅用于线上支付...",
  "sources": [
    {
      "document": "Virtual Card Guide",
      "page": 3
    }
  ]
}
```

---

# 🤖 Agent API

```
POST /v1/agent/chat
```

支持：

* Tool Calling
* Multi-step Reasoning
* Streaming

---

# 📚 Document Ingestion

```
POST /v1/document/upload
```

流程：

```
Upload
   ↓
Loader
   ↓
Text Split
   ↓
Embedding
   ↓
Vector Store
```

---

# 🔄 RAG Workflow

```
User Query
   │
Rewrite Query
   │
Vector Search
   │
Rerank
   │
Context Builder
   │
LLM Generate
   │
Final Answer
```

---

# 🧠 Agent Workflow

基于 **LangGraph**

```
Analyze
  ↓
Retrieve
  ↓
Grade
  ↓
Generate
```

支持：

* Tool Calling
* Self Reflection
* Multi-step Reasoning

---

# 🧪 Evaluation

RAG 评估指标：

* Context Precision
* Answer Faithfulness
* Answer Relevance

---

# 📊 Observability

平台提供：

* Prompt Logs
* LLM Trace
* Latency Metrics
* Token Usage

---

# 🐳 Docker Deployment

```
docker compose up
```

启动服务：

* API
* Redis
* PostgreSQL
* Vector DB

---

# 📜 License

MIT License

---

# ❤️ Contributing

欢迎贡献：

* RAG 改进
* 新 Agent 能力
* 新 Tools
* 新数据源

---
