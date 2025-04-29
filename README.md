# 🧐 Decentralized LLM Network

An open-source, decentralized network for running and querying Large Language Models (LLMs) across multiple peer nodes. Built using FastAPI, IPFS, and Transformers, this project enables serverless AI inference powered by IPFS-based node discovery.

No central coordinator. No cloud lock-in. Just distributed AI.

---

## 🚀 Key Features

- **Peer-to-peer LLM serving**: Each node runs an LLM and registers itself into a blockchain-style registry.
- **IPFS-based node discovery**: Nodes update and sync through `blockchain.json` published on IPFS.
- **Frontend queries via IPFS lookup**: Simple HTML interface queries any random live node.
- **FastAPI + Transformers backend**: Easy to run, extend, or modify.
- **Fully open-source and hackable** 💥

---

## 📁 Project Structure


decentralized-llm-network/
├── node/                  # Backend node implementation
│   ├── node.py
│   ├── ipfs_blockchain.py
│   ├── current_cid.txt    # Contains latest folder CID from IPFS
│   └── blockchain.json     # Node registry (managed via IPFS)
│
├── frontend/              # Minimalistic frontend
│   └── index.html         # Query UI
│
├── README.md              # You're here!
├── LICENSE                # MIT License
├── requirements.txt       # Python dependencies
└── .gitignore             # Files to ignore

## 🧑‍💻 Getting Started

## 📦 Prerequisites

Python 3.10+

IPFS installed and running:

ipfs init
ipfs daemon

🔧 Installation

git clone https://github.com/yourusername/decentralized-llm-network.git
cd decentralized-llm-network
pip install -r requirements.txt

## 🚀 Start a Node

cd node/
uvicorn node:app --host 0.0.0.0 --port 8001

This will:

Fetch latest blockchain.json from IPFS (via current_cid.txt)

Add the node's info to it

Re-upload new version to IPFS

Save updated CID to current_cid.txt

## 🌐 Open Frontend

cd frontend/
open index.html  # or just drag it into a browser

Make sure to update the CID in index.html to the latest IPFS folder CID that includes blockchain.json

## 🛠️ Configuration

In node.py:

Set your NODE_HOST and NODE_PORT

GPT-2 is the default model (you can change it)

## 🔗 IPFS Notes

Always upload blockchain.json inside a folder using ipfs add -r blockchain_folder

Use the folder CID in frontend: https://ipfs.io/ipfs/<folder-cid>/blockchain.json

## 🛁 Roadmap

🚀 Upcoming Features

 🔄 Node heartbeat to mark active/inactive nodes

 🌐 IPNS support for live updating blockchain CID

 ⚙️ CLI tool to register, monitor, and remove nodes easily

 💬 Frontend improvements for query logs and error display

 📱 Mobile-friendly frontend UI

 🧠 Multi-model support (GPT-2, Mistral, LLaMA, etc.)

 🔐 Node authentication and signed registration

 💰 Token-based economy for incentivizing node participation

 📊 Node explorer dashboard (uptime, performance, metadata)

 🚦 Reputation system for ranking reliable nodes

⏳ Pending Development
 Node heartbeat implementation (scheduled self-update)

 Auto-node expiry or status toggling for offline peers

 IPNS name pinning with periodic publishing

 CID auto-update relay (push to GitHub or public DB)


## 📜 License

MIT License. Feel free to use, modify, and build on top of it.

## 🤝 Contributing

PRs are welcome! Please create issues if you find bugs or want to suggest enhancements.

## 🙌 Acknowledgments

Hugging Face Transformers

FastAPI

IPFS

Built with ❤️ for decentralizing intelligence.

