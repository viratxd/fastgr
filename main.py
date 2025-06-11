from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import dynamic
from storage.route_store import RouteStore

app = FastAPI(
    title="Gradio Router API",
    description="A dynamic API router for Gradio spaces",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include dynamic routes
app.include_router(dynamic.router, prefix="/api", tags=["dynamic"])

@app.on_event("startup")
async def startup_event():
    """Load saved routes on startup."""
    route_store = RouteStore()
    routes = route_store.load_routes()
    print(f"Loaded {len(routes)} saved routes on startup")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to the Gradio Router API",
        "endpoints": {
            "create_route": "POST /api/create",
            "use_route": "POST /api/{route_name}",
            "delete_route": "DELETE /api/{route_name}"
        }
    }

# ✅ Run with `python main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)