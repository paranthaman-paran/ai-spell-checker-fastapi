from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from services.openai_service import check_spelling

import os

app = FastAPI()

class TextRequest(BaseModel):
    text: str

@app.post("/check")
async def check_text(request: TextRequest):
    result = check_spelling(request.text)
    return result

# Serve static files
# Create static directory if it doesn't exist (handled by agent tools usually, but good to be safe)
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/", StaticFiles(directory="static", html=True), name="static")
