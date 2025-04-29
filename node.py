from fastapi import FastAPI, Request
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware

import torch
import requests
import threading

app = FastAPI()  # <-- This is the key object uvicorn looks for!


# CORS Middleware to allow frontend (even from file:// or null origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for local dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Node registration details
COORDINATOR_URL = "http://127.0.0.1:8000/register_node"
NODE_HOST = "192.168.1.5"  # Change to your IP
NODE_PORT = 8001

# Register node function
def register_node():
    data = {"host": NODE_HOST, "port": NODE_PORT}
    try:
        res = requests.post(COORDINATOR_URL, json=data)
        print(f"Registered with coordinator: {res.status_code}")
    except Exception as e:
        print(f"Failed to register with coordinator: {e}")

# Start registration in a separate thread
threading.Thread(target=register_node).start()

# LLM Pipeline setup
device = 0 if torch.cuda.is_available() else -1
generator = pipeline('text-generation', model='gpt2', device=device)

@app.post("/process_query")
async def process_query(request: Request):
    data = await request.json()
    query = data['query']
    result = generator(query, max_length=50, truncation=True, pad_token_id=50256)[0]['generated_text']
    return {"result": result}
