from fastapi import HTTPException
from services.dialogflow_service import detect_intent
from services.vonage_service import create_vonage_response

async def handle_inbound_call(from_number: str, to_number: str, text: str):
    try:
        response = await detect_intent(text)
        ncco = create_vonage_response(response.fulfillment_text)
        return ncco
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
