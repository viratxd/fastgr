from fastapi import APIRouter, HTTPException, Request
from typing import Dict, Any
from models.schema import RouteConfig, GradioInput
from services.gradio_manager import GradioManager
from storage.route_store import RouteStore

router = APIRouter()
gradio_manager = GradioManager()
route_store = RouteStore()

@router.post("/create")
async def create_route(config: RouteConfig):
    """Create a new dynamic route."""
    # Check if route already exists
    if route_store.get_route(config.route):
        raise HTTPException(status_code=400, detail="Route already exists")
    
    # Store the route configuration
    route_store.add_route(config.dict())
    
    return {"message": f"Route {config.route} created successfully"}

@router.post("/{route_name}")
async def handle_dynamic_route(route_name: str, request: Request):
    """Handle requests to dynamic routes."""
    # Get route configuration
    route_config = route_store.get_route(route_name)
    if not route_config:
        raise HTTPException(status_code=404, detail="Route not found")
    
    # Parse request body
    try:
        body = await request.json()
        inputs = body.get("inputs")
        if inputs is None:
            raise HTTPException(status_code=400, detail="Missing 'inputs' in request body")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request body: {str(e)}")
    
    # Call Gradio space
    try:
        result = await gradio_manager.predict(
            space_id=route_config["gradio_space"],
            api_name=route_config["api_name"],
            inputs=inputs,
            output_type=route_config["output_type"]
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{route_name}")
async def delete_route(route_name: str):
    """Delete a dynamic route."""
    if route_store.delete_route(route_name):
        return {"message": f"Route {route_name} deleted successfully"}
    raise HTTPException(status_code=404, detail="Route not found") 