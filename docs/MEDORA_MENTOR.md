# MEDORA AI — Senior Engineer Mentor Guide & Product Roadmap

> **Role**: Senior Staff AI Engineer, Backend Architect, Technical Lead, and Coding Mentor  
> **Student**: Shivam (B.Tech AI/ML → Target: 15–20 LPA AI Engineer / GenAI Engineer)  
> **Mode**: 100% Ownership Mode (70% Student Implementation, 30% AI Guidance)  
> **Architecture**: Modular Monolith (FastAPI + LangGraph + Qdrant + PostgreSQL + Deepgram)

---

## 🔒 10 Non-Negotiable Ownership Rules

### Rule 1 — No Copy-Paste Coding
AI ka complete solution directly copy nahi karna. Pehle khud attempt compulsory.

### Rule 2 — 30-Minute Struggle
Problem milne ke baad minimum 30 minutes khud sochna, design karna aur attempt karna. Stuck ho toh progressive hints lena.

### Rule 3 — Explain Before Implement
Code likhne se pehle batao:
- Kya banana hai?
- Input kya hoga?
- Output kya hoga?
- Logic kya hoga?

### Rule 4 — One File, One Ownership
Har file ka purpose, functions, inputs, outputs aur dependencies samajhne honge. Sirf padhkar complete nahi maana jayega.

### Rule 5 — AI Only as Mentor
AI se hints, debugging questions, code review aur alternative approaches maangna. Direct solution last resort hoga.

### Rule 6 — Debug Before Asking
Error aane par pehle:
1. Error message padho.
2. Suspected cause identify karo.
3. Khud fix try karo.
4. Phir AI se review lo.

### Rule 7 — Tests Are Mandatory
Har meaningful feature ke liye happy path, invalid input aur failure case test karna.

### Rule 8 — Build From Blank
Feature complete hone ke baad relevant part ko blank file se dobara implement karo. Tutorial dekhkar reproduce karna independent mastery nahi hai.

### Rule 9 — Weekly Viva
Har Sunday MEDORA ka ek feature bina notes ke explain karna:
- Architecture & Request flow
- Database interaction & Concurrency
- Error handling & Trade-offs

### Rule 10 — Ship, Don't Just Study
Har week ek working, tested, committed deliverable. GitHub par actual progress, fake completion nahi.

---

## 📊 Ownership Levels

| Level | Meaning | Target |
|---|---|---|
| **0** | AI ne likha, tumne copy kiya | ❌ Strictly Prohibited |
| **1** | Code samajh aata hai | 🟡 Baseline |
| **2** | Hints se implement karte ho | 🟡 Good Progress |
| **3** | Independently implement + debug + test | 🟢 Target Minimum |
| **4** | Design, optimize, explain trade-offs & failure modes | 🏆 Target on Flagship Features |

---

## 🗺️ 13-Phase Micro-Task Roadmap

| Phase | Sub-Phase | Task ID | Requirement | Deliverable | Verification | Status |
|---|---|---|---|---|---|---|
| **1. Engineering Foundation** | 1.1 Workspace & Git | `TASK-1.1` | Environment isolation & secrets protection | `.env.example`, `.gitignore`, `README.md` | `git status`, file inspection | ✅ COMPLETED |
| | 1.2 Dependencies | `TASK-1.2` | Package management with `uv` | `requirements.txt`, `.venv` | `uv pip list` | ✅ COMPLETED |
| **2. Python & FastAPI Setup** | 2.1 Configuration | `TASK-2.1` | Pydantic v2 Fail-Fast settings | `app/core/config.py` | Pytest settings load & validation | ⬜ NOT STARTED |
| | 2.2 Error Hierarchy | `TASK-2.2` | Base & domain exception hierarchy | `app/core/exceptions.py` | Pytest exception serialization | ⬜ NOT STARTED |
| | 2.3 Structured Logging | `TASK-2.3` | Structlog JSON/Dev logging setup | `app/core/logging.py` | Console log formatting verification | ⬜ NOT STARTED |
| | 2.4 App Factory | `TASK-2.4` | FastAPI factory with Lifespan & CORS | `app/main.py` | Uvicorn startup & shutdown logs | ⬜ NOT STARTED |
| **3. REST API Development** | 3.1 DTO Schemas | `TASK-3.1` | Pydantic response models | `app/schemas/health.py` | Schema validation | ⬜ NOT STARTED |
| | 3.2 Modular Routing | `TASK-3.2` | APIRouter setup for `/api/v1` | `app/api/router.py`, `routes/health.py` | `GET /api/v1/health` returns 200 | ⬜ NOT STARTED |
| | 3.3 Global Handlers | `TASK-3.3` | Exception handler middleware | `app/main.py` | Custom error returns structured JSON | ⬜ NOT STARTED |
| **4. Database Engineering** | 4.1 Base Model | `TASK-4.1` | SQLAlchemy 2.0 async base & audit fields | `app/db/base.py` | Model inheritance test | ⬜ NOT STARTED |
| | 4.2 Async Engine | `TASK-4.2` | Asyncpg engine & sessionmaker pool | `app/db/session.py` | DB ping test | ⬜ NOT STARTED |
| | 4.3 Domain Models | `TASK-4.3` | User, Doctor, Appointment, Chat models | `app/db/models/*.py` | Table metadata generation | ⬜ NOT STARTED |
| | 4.4 Migrations | `TASK-4.4` | Alembic autogenerate setup | `alembic/versions/` | `alembic upgrade head` | ⬜ NOT STARTED |
| | 4.5 Dependency | `TASK-4.5` | `get_db` session dependency injection | `app/dependencies.py` | Mock DB session test | ⬜ NOT STARTED |
| **5. Auth & Security** | 5.1 Password Hashing | `TASK-5.1` | Secure hashing via `pwdlib` / `bcrypt` | `app/core/security.py` | Unit test hash & verify | ⬜ NOT STARTED |
| | 5.2 JWT Tokens | `TASK-5.2` | Access & Refresh token issuance | `app/core/security.py` | Unit test token decode & expiry | ⬜ NOT STARTED |
| | 5.3 Auth Routes | `TASK-5.3` | Signup, Login, and `get_current_user` | `app/api/routes/auth.py` | `POST /api/v1/auth/login` returns token | ⬜ NOT STARTED |
| **6. Hospital Core Features** | 6.1 Doctor Service | `TASK-6.1` | Doctor repository & search filtering | `app/repositories/doctor_repo.py` | Query doctors by specialty | ⬜ NOT STARTED |
| | 6.2 Appointment Booking | `TASK-6.2` | ACID booking with conflict prevention | `app/services/appointment_service.py` | Concurrency booking test | ⬜ NOT STARTED |
| | 6.3 Doctor/Appt APIs | `TASK-6.3` | REST routes for doctors and bookings | `app/api/routes/` | API tests with auth header | ⬜ NOT STARTED |
| **7. LLM Integration** | 7.1 Provider Client | `TASK-7.1` | Groq / OpenAI client with fallback | `app/core/llm.py` | Streaming completion test | ⬜ NOT STARTED |
| | 7.2 Structured Outputs | `TASK-7.2` | Function calling & Pydantic output parsing | `app/services/llm_service.py` | JSON extraction test | ⬜ NOT STARTED |
| **8. Hospital RAG** | 8.1 Vector DB Setup | `TASK-8.1` | Qdrant collection setup & client | `app/rag/vector_store.py` | Qdrant health check | ⬜ NOT STARTED |
| | 8.2 Ingestion Pipeline | `TASK-8.2` | Document chunking & embedding generation | `app/rag/ingest.py` | Seed docs indexed in Qdrant | ⬜ NOT STARTED |
| | 8.3 Hybrid Retrieval | `TASK-8.3` | Dense search with metadata filtering | `app/rag/retriever.py` | Retrieval similarity evaluation | ⬜ NOT STARTED |
| **9. LangGraph Agentic AI** | 9.1 State Definition | `TASK-9.1` | AgentState schema & memory channels | `app/agents/state.py` | State transition test | ⬜ NOT STARTED |
| | 9.2 Agent Nodes | `TASK-9.2` | Triage, RAG, Booking, Emergency nodes | `app/agents/nodes.py` | Single node execution tests | ⬜ NOT STARTED |
| | 9.3 Graph Compilation | `TASK-9.3` | Conditional edge routing & compile | `app/agents/graph.py` | Intent routing test suite | ⬜ NOT STARTED |
| **10. Voice AI** | 10.1 WebSocket Route | `TASK-10.1` | Bidirectional WebSocket handler | `app/api/routes/voice.py` | WS connection handshake | ⬜ NOT STARTED |
| | 10.2 Deepgram STT/TTS | `TASK-10.2` | Live streaming audio transcription & speech | `app/voice/stream.py` | Audio chunk in -> Audio chunk out | ⬜ NOT STARTED |
| **11. Frontend** | 11.1 Next.js Setup | `TASK-11.1` | App router, Tailwind/CSS, UI layout | `frontend/` | UI boots on port 3000 | ⬜ NOT STARTED |
| | 11.2 Voice & Chat UI | `TASK-11.2` | Real-time audio visualizer & chat box | `frontend/src/components/` | Live WebSocket interaction | ⬜ NOT STARTED |
| **12. Testing & Quality** | 12.1 Unit & Integration | `TASK-12.1` | Complete test suite (>80% coverage) | `backend/tests/` | `pytest --cov=app` | ⬜ NOT STARTED |
| | 12.2 Concurrency Test | `TASK-12.2` | Simulating double-booking race condition | `tests/integration/` | Conflict prevention verified | ⬜ NOT STARTED |
| **13. Docker & Deployment** | 13.1 Docker Compose | `TASK-13.1` | Multi-container setup (API, Postgres, Qdrant, Redis) | `docker-compose.yml` | `docker compose up` all healthy | ⬜ NOT STARTED |
| | 13.2 CI/CD Pipeline | `TASK-13.2` | GitHub Actions workflow for lint & test | `.github/workflows/ci.yml` | GitHub Action green badge | ⬜ NOT STARTED |

---

## 🏛️ Core Architectural Invariants (Non-Negotiables)

1. **Modular Monolith**: One deployable unit with strict internal boundaries (`api` $\rightarrow$ `services` $\rightarrow$ `repositories` $\rightarrow$ `db`).
2. **Fail-Fast Configuration**: Pydantic v2 `BaseSettings` validates `.env` strictly at startup.
3. **Layer Isolation**: Route handlers NEVER query the database or execute business logic directly.
4. **Transactional Integrity**: All booking flows must commit within an explicit async transaction to prevent double-booking.
5. **Responsible AI Guardrails**:
   - AI NEVER provides medical diagnosis or prescriptions.
   - Emergency situations immediately trigger emergency escalation hotlines.
   - Disclaimers mandatory across all medical appointment views.

---

## 🏁 Definition of Done

MEDORA is complete only when:
- 100% of micro-tasks are verified and passed on terminal.
- Independently explainable and defendable on a whiteboard.
- Comprehensive test suite passing with high coverage.
- Dockerized multi-service architecture running smoothly.
- Deployed on live public cloud with a custom domain.
