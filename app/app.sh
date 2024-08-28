alembic upgrade e89456e9ee38
uvicorn --factory application.api.main:create_app --reload --host 0.0.0.0 --port 8000