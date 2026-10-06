from fastapi import APIRouter , status
from app.schemas.welcome import WelcomeResponse

router = APIRouter()

@router.get("" , response_model=WelcomeResponse , status_code=status.HTTP_200_OK)
async def welcome():
    return WelcomeResponse()
