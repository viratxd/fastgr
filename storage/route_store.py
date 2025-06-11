import json
import os
from typing import List, Dict, Any
from pathlib import Path

class RouteStore:
    def __init__(self, storage_path: str = None):
        if storage_path is None:
            # Get the project root directory (where gradio_router_app is located)
            project_root = Path(__file__).parent.parent.parent
            self.storage_path = "./data/routes.json"
        else:
            self.storage_path = storage_path
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        """Ensure the storage directory and file exist."""
        storage_dir = os.path.dirname(self.storage_path)
        os.makedirs(storage_dir, exist_ok=True)
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as f:
                json.dump([], f)

    def save_routes(self, routes: List[Dict[str, Any]]) -> None:
        """Save routes to the storage file."""
        with open(self.storage_path, 'w') as f:
            json.dump(routes, f, indent=2)

    def load_routes(self) -> List[Dict[str, Any]]:
        """Load routes from the storage file."""
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def add_route(self, route: Dict[str, Any]) -> None:
        """Add a new route to storage."""
        routes = self.load_routes()
        routes.append(route)
        self.save_routes(routes)

    def get_route(self, route_name: str) -> Dict[str, Any]:
        """Get a specific route by name."""
        routes = self.load_routes()
        for route in routes:
            if route['route'] == route_name:
                return route
        return None

    def delete_route(self, route_name: str) -> bool:
        """Delete a route by name."""
        routes = self.load_routes()
        initial_length = len(routes)
        routes = [r for r in routes if r['route'] != route_name]
        if len(routes) != initial_length:
            self.save_routes(routes)
            return True
        return False 