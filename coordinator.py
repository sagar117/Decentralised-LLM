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
BASE_DIR =os.path.dirname(os.path.abspath(__file__))

NODE_DIR = os.path.join(BASE_DIR, "node")
# FRONTEND_PATH = os.path.join(BASE_DIR,"frontend")
BLOCKCHAIN_FOLDER = os.path.join(os.path.dirname(__file__), "/node/blockchain_folder")
BLOCKCHAIN_FOLDER = os.path.join(os.path.dirname(__file__), "/node/blockchain_folder/blockchain.json")
CURRENT_CID_PATH = os.path.join(NODE_DIR, "current_cid.txt")

class QueryRequest(BaseModel):
    query: str

@app.post("/submit_query/")
def submit_query(req: QueryRequest):
    try:
        # Get current CID
        # current_cid_path = os.path.join(os.path.dirname(__file__), "/node/current_cid.txt")
        # print (current_cid_path)
        if not os.path.exists(CURRENT_CID_PATH):
            return {"error": "No available nodes — CID missing"}

        with open(CURRENT_CID_PATH) as f:
            cid = f.read().strip()

        # Fetch blockchain.json from IPFS
        # ipfs_url = f"https://ipfs.io/ipfs/{cid}/blockchain.json"
        ipfs_url = f"https://dweb.link/ipfs/{cid}/blockchain.json"

        resp = requests.get(ipfs_url, timeout=5)
        if resp.status_code != 200:
            return {"error": "Failed to fetch blockchain from IPFS"}

        nodes = resp.json()
        if not nodes:
            return {"error": "No available nodes"}

        # Randomly select a node
        import random
        selected_node = random.choice(nodes)
        node_url = f"http://{selected_node['host']}:{selected_node['port']}/process_query"

        try:
            node_resp = requests.post(node_url, json={"query": req.query}, timeout=60)
            return {
                "response": node_resp.json(),
                "node": selected_node
            }
        except Exception as e:
            return {
                "error": f"Failed to reach node at {selected_node['host']}:{selected_node['port']}",
                "details": str(e)
            }

    except Exception as e:
        return {"error": "Internal error", "details": str(e)}

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
        resp = requests.post(node_url, json={"query": req.query}, timeout=60)
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
