from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import random

app = FastAPI()

# Dynamic node list
nodes = []

# Allow all origins for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register_node")
async def register_node(request: Request):
    data = await request.json()
    node_url = f"http://{data['host']}:{data['port']}"
    if node_url not in nodes:
        nodes.append(node_url)
    print(f"Registered Node: {node_url}")
    return {"message": "Node registered", "total_nodes": len(nodes)}

@app.post("/submit_query/")
async def submit_query(request: Request):
    data = await request.json()
    query = data['query']

    if not nodes:
        return {"error": "No available nodes"}

    random.shuffle(nodes)

    for node in nodes:
        try:
            res = requests.post(f"{node}/process_query", json={"query": query})
            if res.status_code == 200:
                return {"result": res.json()["result"], "node": node}
        except Exception as e:
            print(f"Failed node: {node}, Error: {e}")
            continue
    return {"error": "All nodes failed"}
