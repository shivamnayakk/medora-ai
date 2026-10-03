
from pathlib import Path

ROOT = Path(r"E:\Modera ai")

directories = [
    "backend/app/api/routes",
    "backend/app/core",
    "backend/app/db/models",
    "backend/app/schemas",
    "backend/app/repositories",
    "backend/app/services",
    "backend/app/agents",
    "backend/app/rag",
    "backend/app/voice",
    "backend/app/cache",
    "backend/app/utils",

    "backend/tests/unit",
    "backend/tests/integration",
    "backend/tests/api",
    "backend/alembic",

    "frontend/public",
    "frontend/src/app",
    "frontend/src/components",
    "frontend/src/features/chat",
    "frontend/src/features/voice",
    "frontend/src/features/doctors",
    "frontend/src/features/appointments",
    "frontend/src/services",
    "frontend/src/hooks",
    "frontend/src/types",
    "frontend/src/lib",

    "data/hospital_docs",
    "data/seed",

    "scripts",

    "infrastructure/nginx",
    "infrastructure/monitoring/grafana",
    "infrastructure/deployment",

    "docs",
    ".github/workflows",
]

files = [
    "backend/app/__init__.py",
    "backend/app/main.py",
    "backend/app/dependencies.py",

    "backend/app/api/__init__.py",
    "backend/app/api/router.py",
    "backend/app/api/routes/health.py",
    "backend/app/api/routes/auth.py",
    "backend/app/api/routes/chat.py",
    "backend/app/api/routes/voice.py",
    "backend/app/api/routes/doctors.py",
    "backend/app/api/routes/appointments.py",

    "backend/app/core/config.py",
    "backend/app/core/security.py",
    "backend/app/core/logging.py",
    "backend/app/core/exceptions.py",
    "backend/app/core/middleware.py",

    "backend/app/db/base.py",
    "backend/app/db/session.py",
    "backend/app/db/models/user.py",
    "backend/app/db/models/doctor.py",
    "backend/app/db/models/appointment.py",
    "backend/app/db/models/conversation.py",

    "backend/app/schemas/auth.py",
    "backend/app/schemas/user.py",
    "backend/app/schemas/doctor.py",
    "backend/app/schemas/appointment.py",
    "backend/app/schemas/chat.py",

    "backend/app/repositories/doctor_repository.py",
    "backend/app/repositories/appointment_repository.py",
    "backend/app/repositories/conversation_repository.py",

    "backend/app/services/doctor_service.py",
    "backend/app/services/appointment_service.py",
    "backend/app/services/chat_service.py",
    "backend/app/services/voice_service.py",

    "backend/app/agents/state.py",
    "backend/app/agents/graph.py",
    "backend/app/agents/nodes.py",
    "backend/app/agents/tools.py",
    "backend/app/agents/prompts.py",
    "backend/app/agents/guardrails.py",

    "backend/app/rag/loaders.py",
    "backend/app/rag/chunking.py",
    "backend/app/rag/embeddings.py",
    "backend/app/rag/vector_store.py",
    "backend/app/rag/retriever.py",
    "backend/app/rag/fusion.py",
    "backend/app/rag/reranker.py",
    "backend/app/rag/ingestion.py",

    "backend/app/voice/stt.py",
    "backend/app/voice/tts.py",
    "backend/app/voice/websocket.py",

    "backend/app/cache/redis_client.py",
    "backend/app/cache/session_manager.py",

    "backend/app/utils/validators.py",
    "backend/app/utils/response_builder.py",

    "backend/tests/unit/test_services.py",
    "backend/tests/unit/test_agents.py",
    "backend/tests/unit/test_rag.py",
    "backend/tests/integration/test_database.py",
    "backend/tests/integration/test_booking.py",
    "backend/tests/api/test_doctors.py",
    "backend/tests/api/test_appointments.py",
    "backend/tests/api/test_chat.py",

    "backend/alembic.ini",
    "backend/requirements.txt",
    "backend/Dockerfile",
    "backend/.env.example",

    "frontend/src/services/api.ts",
    "frontend/package.json",
    "frontend/tsconfig.json",
    "frontend/Dockerfile",

    "data/seed/sample_data.json",

    "scripts/seed_database.py",
    "scripts/ingest_documents.py",

    "infrastructure/monitoring/prometheus.yml",

    "docs/architecture.md",
    "docs/database.md",
    "docs/api.md",
    "docs/evaluation.md",

    ".github/workflows/ci.yml",

    "docker-compose.yml",
    ".env.example",
    ".gitignore",
    "README.md",
    "LICENSE",
]

def create_structure():
    ROOT.mkdir(parents=True, exist_ok=True)

    for directory in directories:
        (ROOT / directory).mkdir(parents=True, exist_ok=True)

    for file in files:
        path = ROOT / file
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)

    print("\nMEDORA AI structure created successfully!")
    print(f"Location: {ROOT}\n")

    print("Total directories:", sum(1 for p in ROOT.rglob("*") if p.is_dir()))
    print("Total files:", sum(1 for p in ROOT.rglob("*") if p.is_file()))

if __name__ == "__main__":
    create_structure()
