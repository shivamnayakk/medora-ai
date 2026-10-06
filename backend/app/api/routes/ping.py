
from fastapi import APIRouter , status
from app.schemas.ping import Pingresponse

router = APIRouter()

@router.get("", response_model=Pingresponse , status_code = status.HTTP_200_OK)

async def ping():
    return Pingresponse()
