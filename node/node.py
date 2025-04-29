from fastapi import FastAPI, Request
from transformers import pipeline
from ipfs_blockchain import get_current_cid, fetch_blockchain, publish_blockchain

import json
import os
import threading
import requests
import torch

app = FastAPI()

# Node config
NODE_HOST = "192.168.1.25"  # Change to this node's IP
NODE_PORT = 8001
BLOCKCHAIN_FILE = "blockchain.json"

# LLM
device = 0 if torch.cuda.is_available() else -1
generator = pipeline("text-generation", model="gpt2", device=device)

def register_node():
    node_entry = {"host": NODE_HOST, "port": NODE_PORT, "model": "gpt2", "status": "active"}

    cid = get_current_cid()
    if cid:
        registry = fetch_blockchain(cid)
    else:
        registry = []

    if not any(n["host"] == NODE_HOST and n["port"] == NODE_PORT for n in registry):
        registry.append(node_entry)

    new_cid = publish_blockchain(registry)
    print(f"📡 Node registered to IPFS with CID: {new_cid}")

@app.post("/process_query")
async def process_query(request: Request):
    data = await request.json()
    query = data["query"]
    result = generator(query, max_length=50, truncation=True, pad_token_id=50256)[0]["generated_text"]
    return {"result": result}

# Register on startup
threading.Thread(target=register_node).start()
