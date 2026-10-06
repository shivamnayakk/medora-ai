# MEDORA AI — Senior Engineer Mentor Guide

> **Role**: Senior Staff AI Engineer, Backend Architect, Full-Stack Engineer, DevOps Mentor  
> **Student**: B.Tech AI/ML → Target: AI Engineer / GenAI Engineer  
> **Style**: Demanding but supportive. Real-world. No hand-holding without understanding.

---

## 20-Phase Progress Tracker

| Phase | Title | Status |
|-------|-------|--------|
| 1  | Engineering Environment and Project Foundation | 🟡 IN PROGRESS |
| 2  | Python Engineering and Backend Architecture | ⬜ NOT STARTED |
| 3  | FastAPI Fundamentals and REST APIs | ⬜ NOT STARTED |
| 4  | PostgreSQL and Database Engineering | ⬜ NOT STARTED |
| 5  | Authentication and Security | ⬜ NOT STARTED |
| 6  | Doctor Search and Hospital Operations | ⬜ NOT STARTED |
| 7  | Appointment Management | ⬜ NOT STARTED |
| 8  | Redis and Background Processing | ⬜ NOT STARTED |
| 9  | LLM Fundamentals and Provider Integration | ⬜ NOT STARTED |
| 10 | Hospital Knowledge Base and RAG Ingestion | ⬜ NOT STARTED |
| 11 | Advanced Retrieval and RAG Evaluation | ⬜ NOT STARTED |
| 12 | LangGraph Agent Architecture | ⬜ NOT STARTED |
| 13 | Patient AI Chat and Conversation Memory | ⬜ NOT STARTED |
| 14 | Voice AI and WebSocket Engineering | ⬜ NOT STARTED |
| 15 | Frontend Engineering | ⬜ NOT STARTED |
| 16 | Integration and End-to-End Workflows | ⬜ NOT STARTED |
| 17 | Testing and Reliability Engineering | ⬜ NOT STARTED |
| 18 | Docker and CI/CD | ⬜ NOT STARTED |
| 19 | Cloud Deployment and Observability | ⬜ NOT STARTED |
| 20 | Production Hardening and Interview Readiness | ⬜ NOT STARTED |

> Legend: ✅ COMPLETE · 🟡 IN PROGRESS · 🔴 BLOCKED · ⬜ NOT STARTED

A phase is **COMPLETE** only when:
- Core concepts are understood (you can explain them out loud)
- Implementation runs without errors
- Relevant tests pass
- You can explain the architecture, tradeoffs, and alternatives
- Deliverables are verified by terminal output

---

---

# PHASE 1 — Engineering Environment and Project Foundation

**Status**: 🟡 IN PROGRESS

---

## Session Header

| Field | Value |
|-------|-------|
| **Current Phase** | 1 — Engineering Environment and Project Foundation |
| **Current Block** | Block 1 — System Architecture and Request Lifecycle |
| **Learning Objective** | Understand what happens from the moment a user opens MEDORA to when data comes back from the server |
| **Concepts to Understand** | Client-server model, HTTP, request-response cycle, DNS, ports, ASGI, environment separation |
| **What We Will Build** | Mental model + project skeleton verification + .env.example + requirements.txt |
| **Expected Output** | You can draw and explain the full request lifecycle. Files are verified on disk. |
| **How We Will Verify** | Terminal tree output, file content inspection, verbal explanation |

---

## Block 1 — System Architecture and the Request Lifecycle

### 1.1 — What Actually Happens When You Open MEDORA

Before writing a single line of code, you need to understand what you are building and *why* each layer exists.

**Scenario**: A patient opens `https://medora.ai` and types:
> "Can I book an appointment with a cardiologist tomorrow?"

Here is the complete journey:

```
[Patient's Browser]
       |
       | 1. DNS lookup: medora.ai → IP address
       v
[Internet / Network]
       |
       | 2. HTTPS request (TCP, port 443)
       v
[Nginx / Reverse Proxy]
       |
       | 3. Terminates SSL, routes to the right service
       | 4. Forwards to Next.js (port 3000) or FastAPI (port 8000)
       v
[Next.js Frontend — port 3000]
       |
       | 5. Renders the chat UI
       | 6. User types message → JavaScript sends HTTP POST
       v
[FastAPI Backend — port 8000]
       |
       | 7. ASGI server (Uvicorn) receives request
       | 8. Middleware runs (logging, auth check, CORS)
       | 9. Router directs to the correct endpoint: POST /api/v1/chat
       | 10. Dependency injection provides DB session, current user
       | 11. Service layer processes the message
       | 12. Agent decides: is this a booking intent?
       | 13. If yes → query PostgreSQL for doctor availability
       | 14. If RAG needed → query Qdrant vector store
       | 15. LLM generates a grounded response
       v
[PostgreSQL — 5432]   [Qdrant — 6333]   [Redis — 6379]
       |                     |                  |
       | Doctor/Appt data    | Knowledge base   | Session cache
       v                     v                  v
[FastAPI constructs JSON response]
       |
       | 16. Returns HTTP 200 with response body
       v
[Next.js renders the AI reply to the patient]
       |
       | 17. "Dr. Sharma is available tomorrow at 10 AM. Shall I book?"
       v
[Patient confirms → another HTTP request → DB transaction committed]
```

**Key insight**: Every layer has exactly one job. If you blur these responsibilities, debugging becomes a nightmare.

---

### 1.2 — Terminology You Must Know

| Term | Simple Explanation | Professional Term |
|------|--------------------|-------------------|
| Browser asking for data | Your browser sends a message to a server | HTTP Request |
| Server sending data back | The server replies with data | HTTP Response |
| Website address to IP | Phone book for the internet | DNS Resolution |
| Secure connection | Encrypted channel so nobody can snoop | HTTPS / TLS |
| Where a service listens | Like a door number in a building | Port |
| Python async web server | A very fast Python server handling many requests at once | ASGI / Uvicorn |
| Traffic director | Routes requests to correct handlers | Reverse Proxy / Router |
| Shared variables for config | Settings your app reads at startup, not hardcoded | Environment Variables |

---

### 1.3 — Port Map (Memorize This)

| Service | Port | What It Does |
|---------|------|--------------|
| Next.js (Frontend) | 3000 | Serves the web UI |
| FastAPI (Backend) | 8000 | Handles all API requests |
| PostgreSQL | 5432 | Stores structured data |
| Redis | 6379 | Caching and session storage |
| Qdrant | 6333 | Vector database for RAG |
| Nginx (Production) | 80 / 443 | Reverse proxy, SSL termination |

---

### 1.4 — Project Structure and Why Each Directory Exists

```
medora-ai/
├── backend/
│   ├── app/
│   │   ├── api/routes/       ← Thin HTTP handlers only. No business logic here.
│   │   ├── core/             ← Config, security, logging, custom exceptions
│   │   ├── db/               ← SQLAlchemy models and DB session management
│   │   ├── schemas/          ← Pydantic models for request/response validation
│   │   ├── repositories/     ← ONLY place that writes SQL queries
│   │   ├── services/         ← Business logic. Calls repositories + AI layers.
│   │   ├── agents/           ← LangGraph state machine and intent routing
│   │   ├── rag/              ← Embeddings, chunking, vector search, reranking
│   │   ├── voice/            ← STT, TTS, WebSocket session handling
│   │   ├── cache/            ← Redis client and session manager
│   │   └── utils/            ← Shared helpers (validators, response builders)
│   ├── tests/                ← Pytest test suite (unit, integration, api)
│   ├── alembic/              ← Database migration versions
│   └── requirements.txt      ← Pinned Python dependencies
│
├── frontend/                 ← Next.js + TypeScript + Tailwind CSS
├── data/                     ← Synthetic hospital docs and seed data
├── infrastructure/           ← Nginx, Prometheus, Grafana configs
├── scripts/                  ← Operational one-off scripts (seed_db, ingest)
├── docs/MEDORA_AI/           ← All teaching and architecture documentation
├── docker-compose.yml        ← Orchestrates all local services
└── .env.example              ← Secret template (safe to commit)
```

**Golden rule**: `api/routes/` calls `services/`. `services/` calls `repositories/`. `repositories/` calls the DB. No shortcuts. No spaghetti.

---

## Block 1 — Tasks

### Task 1A — Self-Check: Explain the Architecture

Answer these in your own words before touching code:

1. When a patient sends a voice message, what happens before they hear a reply?
2. What is the difference between a port and an IP address?
3. Why does MEDORA separate frontend and backend instead of one application?
4. Why does MEDORA have a `repositories/` layer?
5. What is an environment variable and why must it never be hardcoded?

---

### Task 1B — Populate `.env.example`

File: `E:\Modera ai\.env.example`  
**Already done** ✅ — verify it has content:

```powershell
(Get-Content "E:\Modera ai\.env.example").Count
# Should return > 40 lines
```

---

### Task 1C — Populate `requirements.txt`

File: `E:\Modera ai\backend\requirements.txt`  
**Already done** ✅ — verify:

```powershell
(Get-Content "E:\Modera ai\backend\requirements.txt").Count
# Should return > 40 lines
```

---

### Task 1D — Set Up Python Virtual Environment

```powershell
cd "E:\Modera ai\backend"

# Create venv
python -m venv .venv

# Activate
.\.venv\Scripts\Activate.ps1

# If execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install deps
pip install -r requirements.txt

# Verify
pip show fastapi uvicorn sqlalchemy langchain
```

Expected prompt after activation:
```
(.venv) PS E:\Modera ai\backend>
```

---

### Task 1E — Write `README.md`

File: `E:\Modera ai\README.md`

Write a professional README with:
- What MEDORA does (5 core features)
- Architecture diagram (text-based)
- Technology stack table
- Quick start commands for backend and frontend
- Disclaimer about synthetic data

---

### Task 1F — First Git Commit

```powershell
cd "E:\Modera ai"

git add .env.example .gitignore README.md backend/requirements.txt docs/

git commit -m "feat(foundation): add project skeleton, requirements, and env template

- Add requirements.txt with pinned dependencies for all 20-phase features
- Add .env.example with all required environment variables documented
- Add .gitignore excluding secrets, venv, and build artifacts
- Write initial README with architecture overview and setup instructions
- Add MEDORA_AI mentor guide to docs/"

git push origin main

git log --oneline -5
```

---

## Block 1 — End of Session

### Verification Commands

Run and share the output:

```powershell
cd "E:\Modera ai"

Write-Host "=== File checks ===" -ForegroundColor Cyan
Write-Host ".env.example lines: $((Get-Content .env.example).Count)"
Write-Host "requirements.txt lines: $((Get-Content backend/requirements.txt).Count)"
Write-Host ".gitignore lines: $((Get-Content .gitignore).Count)"

Write-Host "=== Venv check ===" -ForegroundColor Cyan
Test-Path "backend/.venv"

Write-Host "=== Git log ===" -ForegroundColor Cyan
git log --oneline -5
```

### Verification Checklist

- [ ] `.env.example` has content (all sections populated)
- [ ] `requirements.txt` has pinned dependencies
- [ ] `.gitignore` includes `!.env.example` rule
- [ ] Virtual environment created at `backend/.venv`
- [ ] `pip install -r requirements.txt` completed
- [ ] You can explain the request lifecycle from memory
- [ ] You answered all 5 self-check questions in Task 1A
- [ ] `README.md` written with architecture and setup
- [ ] First commit pushed to GitHub

---

### Phase 1 — Interview Questions

**Q1**: What is the difference between HTTP and HTTPS?  
*Expected*: HTTPS is HTTP over TLS. Same protocol, encrypted transport. A certificate proves server identity.

**Q2**: Why use a virtual environment instead of global packages?  
*Expected*: Isolates dependencies per project. `pip install fastapi` in one venv doesn't affect another project.

**Q3**: What happens if a developer commits the `.env` file with real API keys?  
*Expected*: Serious security incident. Even deleting the file later doesn't remove it from Git history. Keys must be rotated immediately.

**Q4**: What is the difference between a port and an IP address?  
*Expected*: IP = machine address on the network. Port = specific service/process on that machine. IP = building, port = apartment.

**Q5**: Why modular monolith instead of microservices?  
*Expected*: Microservices add network calls, distributed tracing, and ops overhead. Modular monolith has same code boundaries, deploys as one unit. Far simpler for one developer.

**Q6**: What is ASGI and why does FastAPI use it?  
*Expected*: Asynchronous Server Gateway Interface. Supports async I/O and WebSockets. WSGI (Flask) is synchronous — it can't handle WebSocket voice streaming.

**Q7**: What is the Repository pattern and why does MEDORA use it?  
*Expected*: Centralizes all DB queries. To swap databases or add a cache layer, you only change repositories — services and routes stay unchanged. Makes code testable.

---

## Next Block

**Block 2 — Git Discipline and Repository Hygiene**

You will learn:
- Conventional commit format used by professional teams
- MEDORA's branching strategy (main → develop → feature/*)
- How to write a production-grade README
- What `git log --oneline --graph` tells you about project history

---

---

# PHASE 1 — Final Completion Gate

**All items required before advancing to Phase 2.**

| Checkpoint | Done? |
|-----------|-------|
| Can explain full request lifecycle from memory | ⬜ |
| `.env.example` populated, all sections present | ⬜ |
| `requirements.txt` has pinned dependencies | ⬜ |
| `.gitignore` excludes `.env` but keeps `.env.example` | ⬜ |
| Virtual environment created and packages installed | ⬜ |
| `README.md` written with architecture and setup | ⬜ |
| First commit pushed to GitHub | ⬜ |
| Answered at least 5 of 7 interview questions | ⬜ |
| Can name all 5 core MEDORA features from memory | ⬜ |

---

---

# PHASE 2 — Python Engineering and Backend Architecture

**Status**: ⬜ NOT STARTED — Complete Phase 1 first

### Preview: What You Will Build

| File | Purpose |
|------|---------|
| `backend/app/core/config.py` | Pydantic Settings — reads `.env` at startup |
| `backend/app/core/exceptions.py` | Custom exception hierarchy for MEDORA |
| `backend/app/core/logging.py` | Structured JSON logging with structlog |
| `backend/app/main.py` | FastAPI app factory with lifespan context manager |

### Concepts You Will Learn

- Why Python classes matter for large codebases
- How Pydantic validates configuration at startup (fail-fast principle)
- Why structured JSON logging beats `print()` in production
- What a context manager is and when to use `@asynccontextmanager`
- How `async`/`await` works and why FastAPI requires it
- What dependency injection is and why it makes code testable and swappable

---

---

# ARCHITECT'S NOTES

## Key Design Decisions

| Decision | Why |
|----------|-----|
| Modular monolith | Microservices add distributed ops overhead with no user benefit at this scale |
| Pydantic v2 | 5–50x faster than v1 due to Rust core. FastAPI 0.100+ requires it. |
| LangGraph over chains | MEDORA needs conditional routing (booking vs RAG vs search) — impossible cleanly in a linear chain |
| Qdrant over Pinecone | Open-source, free local dev, Docker-native, no account needed |
| Groq over OpenAI | 300+ tokens/sec on Llama-3 — critical for low-latency voice conversations |
| Deepgram over Whisper | Real-time WebSocket streaming STT. Local Whisper batches audio and cannot stream. |

## Common Mistakes — Avoid These

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| DB queries inside route handlers | Spaghetti, untestable | Repository pattern |
| Hardcoded API keys | Security incident | Environment variables only |
| `except Exception` everywhere | Hides real bugs | Catch specific types |
| No transaction on booking | Double bookings | Explicit async transactions |
| Conversation state only in RAM | Lost on restart | Persist in Redis / PostgreSQL |
| HTTP 200 for all responses | Client cannot detect errors | Correct status codes always |
| No input validation | Injection attacks | Pydantic schemas on every input |
| Logging secrets or PII | Compliance violation | Sanitize all log fields |

## Emergency Escalation Rules (Non-Negotiable)

1. If a user describes a medical emergency, MEDORA **must** immediately provide emergency contact information and direct them to call emergency services. Never handle through AI.
2. The agent must never provide medical diagnosis or treatment recommendations.
3. All appointment flows must display a disclaimer: this is not a medical advice system.
4. If the LLM fails or intent cannot be routed, fall back to a human handoff message — never hallucinate an answer.

---

*Last updated: Phase 1, Block 1 — files populated and verified.*
