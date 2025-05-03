import os
import json
import subprocess
from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# ==== Paths ====
BASE_DIR =os.path.dirname(os.path.abspath(__file__))

NODE_DIR = os.path.join(BASE_DIR, "node")
FRONTEND_PATH = os.path.join(BASE_DIR,"frontend")
CONFIG_PATH = os.path.join(NODE_DIR,"node_config.json")
BLOCKCHAIN_PATH = "blockchain.json"
FOLDER_NAME = os.path.join(NODE_DIR, "blockchain_folder")
CURRENT_CID_PATH = os.path.join(NODE_DIR, "current_cid.txt")



app = FastAPI()
print("🔍 CONFIG_PATH =", CONFIG_PATH)  # ← move here


# ==== Serve current_cid.txt ====
@app.get("/node/current_cid.txt")
def serve_current_cid():
    print("📄 Looking for:", CURRENT_CID_PATH)
    print("📄 Looking for:", CONFIG_PATH)
    if os.path.exists(CURRENT_CID_PATH):
        return FileResponse(CURRENT_CID_PATH)
    return JSONResponse(status_code=404, content={CURRENT_CID_PATH})


# ==== Serve Static Frontend ====
app.mount("/", StaticFiles(directory=FRONTEND_PATH, html=True), name="frontend")


# ==== Utility Functions ====
def get_current_cid():
    with open(CURRENT_CID_PATH) as f:
        return f.read().strip()

def fetch_blockchain(cid: str, folder: str):
    subprocess.run(["ipfs", "get", cid, "-o", folder])

def publish_blockchain(folder: str) -> str | None:
    result = subprocess.run(["ipfs", "add", "-r", folder], capture_output=True, text=True)
    print("🔍 IPFS output:\n", result.stdout)
    lines = result.stdout.strip().split("\n")
    folder_basename = os.path.basename(folder)
    folder_line = next((l for l in lines if l.endswith(folder_basename)), None)
    if folder_line:
        return folder_line.split()[1]
    print("❌ No matching folder line found in IPFS output.")
    return None

# ==== Node Registration on Startup ====
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH) as f:
        config = json.load(f)

    node_entry = {
        "host": os.getenv("NODE_HOST", "127.0.0.1"),
        "port": os.getenv("NODE_PORT", "8001"),
        "model": config.get("model"),
        "hardware": config.get("hardware"),
        "max_tokens": config.get("max_tokens"),
        "supports_streaming": config.get("supports_streaming"),
        "inference_server": config.get("inference_server"),
        "last_seen": datetime.utcnow().isoformat() + "Z"
    }

    # Sync latest blockchain
    if os.path.exists(CURRENT_CID_PATH):
        cid = get_current_cid()
        fetch_blockchain(cid, FOLDER_NAME)

    # Read or initialize blockchain.json
    blockchain_file = os.path.join(FOLDER_NAME, BLOCKCHAIN_PATH)
    if os.path.exists(blockchain_file):
        with open(blockchain_file, "r") as f:
            blockchain = json.load(f)
    else:
        blockchain = []

    # Update blockchain
    blockchain = [n for n in blockchain if not (n["host"] == node_entry["host"] and n["port"] == node_entry["port"])]
    blockchain.append(node_entry)

    os.makedirs(FOLDER_NAME, exist_ok=True)
    with open(blockchain_file, "w") as f:
        json.dump(blockchain, f, indent=2)

    # Publish to IPFS
    new_cid = publish_blockchain(FOLDER_NAME)
    if new_cid:
        with open(CURRENT_CID_PATH, "w") as f:
            f.write(new_cid)
        print(f"📡 Node registered to IPFS with CID: {new_cid}")
    else:
        print("❌ Failed to register node to IPFS.")
else:
    print("📄 Looking for:", CONFIG_PATH)
    print("⚠️ No node_config.json found. Skipping node registration.")
    
