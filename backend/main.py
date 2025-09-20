from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import aiofiles
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="IA Multimodale - Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    messages: list

@app.post("/api/chat")
async def chat(body: ChatRequest):
    if not openai.api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not set")
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=body.messages,
            max_tokens=512,
        )
        return {"reply": resp.choices[0].message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/image")
async def create_image(payload: dict):
    if not openai.api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not set")
    prompt = payload.get("prompt")
    size = payload.get("size", "512x512")
    if not prompt:
        raise HTTPException(status_code=400, detail="prompt required")
    try:
        resp = openai.Image.create(prompt=prompt, n=1, size=size)
        url = resp.data[0].url if hasattr(resp.data[0], 'url') else resp.data[0]['url']
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/transcribe")
async def transcribe(file: UploadFile = File(...)):
    if not openai.api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not set")
    tmp = f"/tmp/{file.filename}"
    async with aiofiles.open(tmp, "wb") as f:
        content = await file.read()
        await f.write(content)
    try:
        with open(tmp, "rb") as audio_file:
            resp = openai.Audio.transcribe("whisper-1", audio_file)
        return {"text": resp["text"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
