from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest
from app.services.chat_service import answer_question

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest):
	try:
		return answer_question(request.message)
	except FileNotFoundError as error:
		raise HTTPException(status_code=503, detail=str(error)) from error
