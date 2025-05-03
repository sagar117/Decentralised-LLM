from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import json
import os
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


BLOCKCHAIN_FOLDER = os.path.join(os.path.dirname(__file__), "../node/blockchain_folder")
BLOCKCHAIN_PATH = os.path.join(BLOCKCHAIN_FOLDER, "blockchain.json")

class QueryRequest(BaseModel):
    query: str

@app.post("/submit_query/")
def submit_query(req: QueryRequest):
    # Load latest node list
    if not os.path.exists(BLOCKCHAIN_PATH):
        return {"error": "No available nodes"}

    with open(BLOCKCHAIN_PATH) as f:
        nodes = json.load(f)

    if not nodes:
        return {"error": "No available nodes"}

    # Pick a random node (could be improved later)
    import random
    selected_node = random.choice(nodes)
    node_url = f"http://{selected_node['host']}:{selected_node['port']}/process_query"

    try:
        resp = requests.post(node_url, json={"query": req.query}, timeout=10)
        return {
            "response": resp.json(),
            "node": selected_node
        }
    except Exception as e:
        return {
            "error": f"Failed to reach node at {selected_node['host']}:{selected_node['port']}",
            "details": str(e)
        }

@app.get("/")
def health():
    return {"status": "Coordinator running"}
