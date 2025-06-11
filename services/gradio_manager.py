from gradio_client import Client
from typing import Any, Dict, Optional

class GradioManager:
    def __init__(self):
        self._clients: Dict[str, Client] = {}

    def get_client(self, space_id: str) -> Client:
        """Get or create a Gradio client for the given space."""
        if space_id not in self._clients:
            self._clients[space_id] = Client(space_id)
        return self._clients[space_id]

    async def predict(
        self,
        space_id: str,
        api_name: str,
        inputs: Any,
        output_type: str = "txt"
    ) -> Any:
        """Make a prediction using the specified Gradio space."""
        try:
            client = self.get_client(space_id)
            result = client.predict(
                inputs,
                api_name=api_name
                )
            
            if output_type == "json":
                return result
            elif output_type == "txt":
                return str(result)
            else:
                return result
                
        except Exception as e:
            raise Exception(f"Error calling Gradio space: {str(e)}")

    def clear_client(self, space_id: str) -> None:
        """Clear a specific client from the cache."""
        if space_id in self._clients:
            del self._clients[space_id] 