Sure, here is a comprehensive `README.md` for the Call Handling App:

```markdown

# 📞 Call Handling App

Welcome to the Call Handling App! This project is a full-stack application that uses Laravel for the backend, FastAPI for specific tasks, and Next.js for the frontend. The application integrates Vonage Voice API (VAPI) for handling inbound and outbound calls and includes functionality for booking appointments via Google Calendar and logging call details to a CRM.

## 🏗️ Project Structure

```

call-handling-app/ ├── backend-laravel/ ├── fastapi-service/ ├── frontend-nextjs/ ├── [README.md](http://README.md)

````

## 🚀 Getting Started

### Prerequisites

- PHP and Composer
- Python 3 and pip
- Node.js and npm
- Vonage, Google Cloud, and Dialogflow accounts

### Backend - Laravel

1. **Create Laravel Project**

```sh
composer create-project --prefer-dist laravel/laravel backend-laravel
cd backend-laravel
````

2.  **Set Up Routes and Controllers**

*   `routes/api.php`

```php

use App\Http\Controllers\CallController;

Route::post('/inbound', [CallController::class, 'handleInboundCall']);
Route::post('/outbound', [CallController::class, 'handleOutboundCall']);
Route::post('/appointment', [CallController::class, 'bookAppointment']);
Route::post('/crm', [CallController::class, 'logToCRM']);
```

*   `app/Http/Controllers/CallController.php`

```php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Services\FastAPIService;


class CallController extends Controller
{
    protected $fastAPIService;

    public 
function __construct(FastAPIService $fastAPIService
)
    {
        $this->fastAPIService = $fastAPIService;
    }

    public 
function handleInboundCall(Request $request
)
    {
        return $this->fastAPIService->handleInboundCall($request->all());
    }

    public 
function handleOutboundCall(Request $request
)
    {
        return $this->fastAPIService->handleOutboundCall($request->all());
    }

    public 
function bookAppointment(Request $request
)
    {
        return $this->fastAPIService->bookAppointment($request->all());
    }

    public 
function logToCRM(Request $request
)
    {
        return $this->fastAPIService->logToCRM($request->all());
    }
}
```

*   `app/Services/FastAPIService.php`

```php

namespace App\Services;

use GuzzleHttp\Client;


class FastAPIService
{
    protected $client;

    public 
function __construct(
)
    {
        $this->client = new Client(['base_uri' => env('FASTAPI_BASE_URL')]);
    }

    public 
function handleInboundCall(
$data
)
    {
        $response = $this->client->post('/inbound', [
            'json' => $data
        ]);
        return json_decode($response->getBody()->getContents(), true);
    }

    public 
function handleOutboundCall(
$data
)
    {
        $response = $this->client->post('/outbound', [
            'json' => $data
        ]);
        return json_decode($response->getBody()->getContents(), true);
    }

    public 
function bookAppointment(
$data
)
    {
        $response = $this->client->post('/appointment', [
            'json' => $data
        ]);
        return json_decode($response->getBody()->getContents(), true);
    }

    public 
function logToCRM(
$data
)
    {
        $response = $this->client->post('/crm', [
            'json' => $data
        ]);
        return json_decode($response->getBody()->getContents(), true);
    }
}
```

*   **Environment Configuration** (`.env`):

```
FASTAPI_BASE_URL=http://localhost:8000
```

### FastAPI Service

1.  **Create FastAPI Project**

```sh

mkdir fastapi-service
cd fastapi-service
python3 -m venv env
source env/bin/activate
pip install fastapi uvicorn google-cloud-dialogflow vonage
```

2.  **FastAPI Project Structure**

```
fastapi-service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── dialogflow_service.py
│   │   ├── google_calendar_service.py
│   │   └── vonage_service.py
├── config/
│   ├── dialogflow/
│   │   └── service-account-key.json
│   └── google-calendar/
│       └── credentials.json
├── requirements.txt
└── README.md
```

3.  **Implement FastAPI Endpoints**

*   `main.py`

```python

from fastapi import FastAPI
from app.routes import router

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

*   `routes.py`

```python

from fastapi import APIRouter, Request
from app.services import dialogflow_service, vonage_service, google_calendar_service

router = APIRouter()

@router.post(
"/inbound"
)
async def inbound_call(request: Request):
    data = await request.json()
    response = await dialogflow_service.detect_intent(data['speech'])
    return vonage_service.create_vonage_response(response.fulfillment_text)

@router.post(
"/outbound"
)
async def outbound_call(request: Request):
    data = await request.json()
    response = await dialogflow_service.detect_intent(data['speech'])
    return vonage_service.create_vonage_response(response.fulfillment_text)

@router.post(
"/appointment"
)
async def book_appointment(request: Request):
    data = await request.json()
    return google_calendar_service.book_appointment(data)

@router.post(
"/crm"
)
async def log_to_crm(request: Request):
    data = await request.json()
    return crm_service.log_to_crm(data)
```

*   `dialogflow_service.py`

```python

from google.cloud import dialogflow_v2 as dialogflow
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config/dialogflow/service-account-key.json"

session_client = dialogflow.SessionsClient()
session_path = session_client.session_path('YOUR_PROJECT_ID', 'SESSION_ID')

async def detect_intent(text: str
):
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
```

*   `vonage_service.py`

```python

import vonage

client = vonage.Client(application_id="YOUR_APPLICATION_ID", private_key="config/vonage/private.key")
voice = vonage.Voice(client)

def create_vonage_response(text: str
):
    ncco = [
        {
            "action": "talk",
            "text": text
        }
    ]
    return ncco
```

*   `google_calendar_service.py`

```python

from googleapiclient.discovery import build
from google.oauth2 import service_account
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = os.path.join('config/google-calendar', 'credentials.json')

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

async def book_appointment(data):
    event = {
        'summary': data['summary'],
        'start': {'dateTime': data['start'], 'timeZone': 'America/Los_Angeles'},
        'end': {'dateTime': data['end'], 'timeZone': 'America/Los_Angeles'}
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event
```

4.  **Requirements File**

*   `requirements.txt`

```
fastapi
uvicorn
google-cloud-dialogflow
vonage
google-api-python-client
google-auth
```

5.  **Run FastAPI**

```sh
uvicorn app.main:app --reload
```

### Frontend - Next.js

1.  **Create Next.js Project**

```sh
npx create-next-app frontend-nextjs
cd frontend-nextjs
```

2.  **Project Structure**

```
frontend-nextjs/
├── components/
│   └── CallForm.js
├── pages/
│   ├── api/
│   │   └── calls.js
│   ├── _app.js
│   └── index.js
├── public/
├── styles/
│   └── globals.css
├── .env.local
├── package.json
└── README.md
```

3.  **Implement Call Form Component**

*   `components/CallForm.js`

```jsx

import { useState } from 'react';

const CallForm = (
) => {
    const [formData, setFormData] = useState({
        from: '',
        to: '',
        speech: ''
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await fetch('/api/calls', {
            method: 'POST',
```