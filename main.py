from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()

VERIFY_TOKEN = "my_expense_assistant_token"


@app.get("/")
def home():
    return {"message": "Personal Expense Assistant is running!"}


@app.get("/webhook")
def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)

    return PlainTextResponse("Verification failed", status_code=403)


@app.post("/webhook")
async def receive_webhook(request: Request):
    data = await request.json()

    value = data["entry"][0]["changes"][0]["value"]

    if "messages" in value:
        message = value["messages"][0]

        sender = message["from"]
        message_type = message["type"]

        if message_type == "text":
            text = message["text"]["body"]

            print("Sender:", sender)
            print("Message:", text)

    return {"status": "ok"}