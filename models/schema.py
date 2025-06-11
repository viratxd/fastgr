from pydantic import BaseModel, Field
from typing import List, Any, Optional

class RouteConfig(BaseModel):
    route: str = Field(..., description="The desired dynamic route name")
    gradio_space: str = Field(..., description="The Gradio space ID")
    api_name: str = Field(..., description="The API endpoint name to call")
    output_type: str = Field(..., description="Response format (txt or json)")

class GradioInput(BaseModel):
    inputs: Any = Field(..., description="Input data for the Gradio model")
    top_p: Optional[float] = Field(1.0, description="Top p sampling parameter")
    temperature: Optional[float] = Field(1.0, description="Temperature parameter")
    chat_counter: Optional[int] = Field(0, description="Chat counter for conversation models")
    chatbot: Optional[List[Any]] = Field([], description="Chat history for conversation models") 