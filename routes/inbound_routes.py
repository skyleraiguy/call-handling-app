from fastapi import APIRouter, Request
from controllers import inbound_controller

router = APIRouter()

@router.post("/")
async def inbound_call(request: Request):
    body = await request.json()
    from_number = body.get('from')
    to_number = body.get('to')
    text = body.get('speech')  # Assuming the speech to text is done by VAPI
    ncco = await inbound_controller.handle_inbound_call(from_number, to_number, text)
    return ncco
