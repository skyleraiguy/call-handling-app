import vonage

client = vonage.Client(application_id="YOUR_APPLICATION_ID", private_key="config/vonage/private.key")
voice = vonage.Voice(client)

def create_vonage_response(text: str):
    ncco = [
        {
            "action": "talk",
            "text": text
        }
    ]
    return ncco
