#pip install python-multipart


import os, shutil, tempfile
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from fastapi import UploadFile, File, Form
from app.rag.retriever import index_image
import uuid 
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.graph import graph, invoke_function


#Configration 
app = FastAPI(title="Ai Doubt Solver")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

VALID_MODE = ["Short", "Medium", "Long"]


# Validation State
class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None


class ChatResponse(BaseModel):
    thread_id: str
    status: str
    interrupt: Optional[dict] = None
    bot_response: Optional[str] = None
    sources: Optional[list[str]] = None


# Endpoints
@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/upload")
def upload_image(
    file: UploadFile = File(...),
    source_id: Optional[str] = Form(None),
    language: str = Form("eng")
):
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        result = index_image(tmp_path, source_id=source_id or file.filename, language=language)
    finally:
        os.remove(tmp_path)

    return {
        "source": result["source"],
        "chunks_created": result["chunks_created"],
        "document_ids": result["document_ids"]
    }


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    
    thread_id =  req.thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    state = graph.get_state(config)
    pending = any(t.interrupts for t in state.tasks)
    if pending and req.message not in VALID_MODE:
        raise HTTPException(
            status_code=400,
            detail=f"Answer length select: {sorted(VALID_MODE)}"
        )

    try:
        result = invoke_function(graph, req.message, thread_id)
    except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))

    return ChatResponse(thread_id=thread_id, **result)