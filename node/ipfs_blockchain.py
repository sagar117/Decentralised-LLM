import json
import os
import subprocess
from datetime import datetime

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "node_config.json")
BLOCKCHAIN_PATH = "blockchain.json"
FOLDER_NAME = os.path.join(os.path.dirname(__file__), "blockchain_folder")
CURRENT_CID_PATH = "current_cid.txt"

# Utility functions for import

def get_current_cid():
    with open(CURRENT_CID_PATH) as f:
        return f.read().strip()

def fetch_blockchain(cid, folder):
    subprocess.run(["ipfs", "get", cid, "-o", folder])

def publish_blockchain(folder):
    result = subprocess.run(["ipfs", "add", "-r", folder], capture_output=True, text=True)
    print("🔍 IPFS output:\n", result.stdout)
    lines = result.stdout.strip().split("\n")
    folder_basename = os.path.basename(folder)
    folder_line = next((l for l in lines if l.endswith(folder_basename)), None)
    if folder_line:
        return folder_line.split()[1]
    else:
        print("❌ No matching folder line found in IPFS output.")
        return None

# Load node metadata from config
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

# Pull latest CID and fetch blockchain.json
if os.path.exists(CURRENT_CID_PATH):
    cid = get_current_cid()
    fetch_blockchain(cid, FOLDER_NAME)

# Read or initialize blockchain
if os.path.exists(f"{FOLDER_NAME}/{BLOCKCHAIN_PATH}"):
    with open(f"{FOLDER_NAME}/{BLOCKCHAIN_PATH}", "r") as f:
        blockchain = json.load(f)
else:
    blockchain = []

# Remove outdated entry for this node
blockchain = [n for n in blockchain if not (n["host"] == node_entry["host"] and n["port"] == node_entry["port"])]

# Add current node
blockchain.append(node_entry)

# Save updated blockchain
if not os.path.exists(FOLDER_NAME):
    os.makedirs(FOLDER_NAME)
with open(f"{FOLDER_NAME}/{BLOCKCHAIN_PATH}", "w") as f:
    json.dump(blockchain, f, indent=2)

# Re-add to IPFS
new_cid = publish_blockchain(FOLDER_NAME)
if new_cid:
    with open(CURRENT_CID_PATH, "w") as cid_file:
        cid_file.write(new_cid)
    print(f"📡 Node registered to IPFS with CID: {new_cid}")
else:
    print("❌ Failed to register node to IPFS.")
