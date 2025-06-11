# Gradio Router API

A scalable and modular FastAPI backend that allows users to dynamically create and use API routes at runtime, using the gradio_client to interact with Hugging Face Gradio spaces.

## Features

- Dynamic route creation and management
- Persistent route storage
- Automatic route restoration on server restart
- Support for both text and JSON responses
- Easy integration with any Gradio space

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
# From the gradio_router_app directory
uvicorn gradio_router_app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Usage

### Create a New Route

```bash
curl -X POST "http://localhost:8000/api/create" \
     -H "Content-Type: application/json" \
     -d '{
           "route": "chat1",
           "gradio_space": "yuntian-deng/ChatGPT",
           "api_name": "/predict",
           "output_type": "txt"
         }'
```

### Use a Dynamic Route

```bash
curl -X POST "http://localhost:8000/api/chat1" \
     -H "Content-Type: application/json" \
     -d '{
           "inputs": "Hello!!",
           "top_p": 1,
           "temperature": 1,
           "chat_counter": 0,
           "chatbot": []
         }'
```

### Delete a Route

```bash
curl -X DELETE "http://localhost:8000/api/chat1"
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
gradio_router_app/
├── __init__.py         # Package initialization
├── main.py            # FastAPI application entry point
├── routes/
│   ├── __init__.py    # Routes package initialization
│   └── dynamic.py     # Dynamic route handlers
├── services/
│   ├── __init__.py    # Services package initialization
│   └── gradio_manager.py # Gradio client management
├── models/
│   ├── __init__.py    # Models package initialization
│   └── schema.py      # Pydantic models
├── storage/
│   ├── __init__.py    # Storage package initialization
│   └── route_store.py # Route persistence
├── data/
│   └── routes.json    # Route storage
└── requirements.txt   # Project dependencies
``` 