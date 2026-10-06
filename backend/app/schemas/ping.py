from pydantic import BaseModel
class Pingresponse(BaseModel):
    message : str = "pong"
    alive : bool = True    