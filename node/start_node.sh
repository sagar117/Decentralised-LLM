#!/bin/bash

# Ensure IPFS daemon is running
if ! pgrep -f "ipfs daemon" > /dev/null; then
  echo "🚀 Starting IPFS daemon..."
  ipfs daemon &
  sleep 5
else
  echo "✅ IPFS daemon already running."
fi

# Register node with latest IPFS blockchain
echo "🔄 Registering node to IPFS..."
python3 node/ipfs_blockchain.py

# Start the FastAPI app
if command -v uvicorn &> /dev/null; then
  echo "🧠 Launching LLM node with uvicorn..."
  uvicorn node.node:app --host 0.0.0.0 --port 8001
else
  echo "❌ 'uvicorn' not found in PATH. Trying fallback via python module..."
  python3 -m uvicorn node.node:app --host 0.0.0.0 --port 8001
fi
