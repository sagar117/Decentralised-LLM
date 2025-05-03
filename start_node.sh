#!/bin/bash

# Ensure IPFS daemon is running
if ! pgrep -f "ipfs daemon" > /dev/null; then
  echo "🚀 Starting IPFS daemon..."
  ipfs daemon &
  sleep 5
else
  echo "✅ IPFS daemon already running."
fi

# Clean up blockchain folder if it already exists
BLOCKCHAIN_DIR="node/blockchain_folder"
if [ -d "$BLOCKCHAIN_DIR" ]; then
  echo "⚠️ Removing existing blockchain folder..."
  rm -rf "$BLOCKCHAIN_DIR"
fi

# Register node with latest IPFS blockchain
echo "🔄 Registering node to IPFS..."
CID_OUTPUT=$(python3 node/ipfs_blockchain.py 2>&1)
CID_LINE=$(echo "$CID_OUTPUT" | grep "📡 Node registered to IPFS with CID")

if [ -z "$CID_LINE" ]; then
  echo "❌ Failed to register node to IPFS."
  echo "$CID_OUTPUT"
  exit 1
fi

# Start the FastAPI app
if command -v uvicorn &> /dev/null; then
  echo "🧠 Launching LLM node with uvicorn..."
  uvicorn node.node:app --host 0.0.0.0 --port 8001
else
  echo "❌ 'uvicorn' not found in PATH. Trying fallback via python module..."
  python3 -m uvicorn node.node:app --host 0.0.0.0 --port 8001
fi
