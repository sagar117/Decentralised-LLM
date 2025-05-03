import json
import os
import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "node_config.json")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load config
with open(CONFIG_PATH) as f:
    config = json.load(f)

MODEL_NAME = config.get("model", "gpt2")
USE_INFERENCE_SERVER = config.get("inference_server", False)
INFERENCE_SERVER_URL = config.get("inference_server_url", "")

# Load model only if local inference
if not USE_INFERENCE_SERVER:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

@app.post("/process_query")
async def process_query(request: Request):
    data = await request.json()
    query = data.get("query", "")

    if not query:
        return {"error": "Query is required"}

    if USE_INFERENCE_SERVER:
        try:
            response = requests.post(INFERENCE_SERVER_URL, json={"inputs": query})
            response.raise_for_status()
            result = response.json()
            return {"response": result.get("generated_text", "")}
        except Exception as e:
            return {"error": str(e)}
    else:
        try:
            outputs = generator(query, max_length=100, do_sample=True)
            return {"response": outputs[0]['generated_text']}
        except Exception as e:
            return {"error": str(e)}

@app.get("/")
def root():
    return {"status": "Node is running with model: {}".format(MODEL_NAME)}
