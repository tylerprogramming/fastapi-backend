# FastAPI backend for todo-ai

A FastAPI server with an OpenAI Agents SDK chatbot and Supabase storage. It is the backend that the [todo-ai](https://github.com/tylerprogramming/todo-ai) frontend calls.

Endpoints (see `main.py`):
- GET `/`: returns a welcome message
- POST `/items/`: accepts an item with name and description
- POST `/chatbot/`: sends `{message, user}` to the todo assistant agent, which can list and add the user's todos
- POST `/recommendations/`: returns the recommended todos stored for `{id, email}`
- POST `/thumbs`: records a thumbs up or down on a recommended todo

## Setup and Running

Requires Python 3.10+.

1. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill in `SUPABASE_URL`, `SUPABASE_KEY` and `OPENAI_API_KEY`. The Supabase project needs the `todos` and `recommended_todos` tables that `database/my_supabase.py` queries.

4. Run the application:
```bash
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`
