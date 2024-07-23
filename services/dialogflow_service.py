from google.cloud import dialogflow_v2 as dialogflow
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config/dialogflow/service-account-key.json"

session_client = dialogflow.SessionsClient()
session_path = session_client.session_path('YOUR_PROJECT_ID', 'SESSION_ID')

async def detect_intent(text: str):
    request = {
        "session": session_path,
        "query_input": {
            "text": {
                "text": text,
                "language_code": 'en-US',
            }
        }
    }
    response = session_client.detect_intent(request=request)
    return response.query_result
