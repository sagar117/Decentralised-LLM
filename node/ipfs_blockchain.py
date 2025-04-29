import subprocess
import json
import os

IPFS_PATH = "blockchain.json"
CURRENT_CID_FILE = "current_cid.txt"

def get_current_cid():
    if not os.path.exists(CURRENT_CID_FILE):
        return None
    with open(CURRENT_CID_FILE, "r") as f:
        return f.read().strip()

def fetch_blockchain(cid):
    subprocess.run(["ipfs", "get", cid, "-o", IPFS_PATH])
    with open(IPFS_PATH, "r") as f:
        return json.load(f)

def publish_blockchain(registry):
    with open(IPFS_PATH, "w") as f:
        json.dump(registry, f, indent=2)
    result = subprocess.run(["ipfs", "add", "-q", IPFS_PATH], capture_output=True)
    cid = result.stdout.decode().strip()
    with open(CURRENT_CID_FILE, "w") as f:
        f.write(cid)
    return cid

