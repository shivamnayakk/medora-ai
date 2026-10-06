from pydantic import BaseModel


class WelcomeResponse(BaseModel):
    message: str = "Welcome to Medora AI - Healthcare Intelligence Platform"
    version: str = "0.1.0"
