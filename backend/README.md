# Backend

FastAPI backend for OpenData Ghost.

Commands (from backend folder):

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Index sample data:

```bash
python scripts/index_data.py
```