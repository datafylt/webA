web: uvicorn app:app --host 0.0.0.0 --port $PORT
release: python -c "import asyncio; from app.core.init_app import init_db; asyncio.run(init_db())"