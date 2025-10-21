import os
from dotenv import find_dotenv
from dotenv import load_dotenv

# load env variables from the .env file
load_dotenv(find_dotenv())

# Initialize Qdrant client
# Note: make sure you have Qdrant running in your Kubernetes cluster and port-forwarded to localhost:6334
# kubectl -n qdrant port-forward svc/qdrant 6334:6334
import qdrant_client

qdrant_host = os.getenv("QDRANT_HOST", "127.0.0.1")
client = qdrant_client.QdrantClient(
    host=qdrant_host,
    prefer_grpc=True,
)

print(client.get_collections())

# Initialize OpenAI client
from openai import AzureOpenAI
openai_client = AzureOpenAI()

def get_embedding(text, model="text-embedding-3-large"):
    res = openai_client.embeddings.create(
        model=model,
        input=[text]
    )
    return res.data[0].embedding

def query_docs(query, collection_name="rag", model="text-embedding-3-large" , top_k=5):
    query_vect = get_embedding(query, model)
    results = client.query_points(
        collection_name=collection_name,
        query=query_vect,
        limit=5,
        with_payload=True,
        using="question"
    )
    payloads = [point.payload["answer"] for point in results.points]
    return payloads

def generate_answer(query, docs, model="gpt-4o-mini"):
    context = "\n\n".join(docs)
    prompt = query + "\n\n" + context
    res = openai_client.chat.completions.create(
        model=model,  # 或你的 Azure 模型名稱
        messages=[
            {"role": "system", "content": "You're a helpful AI assistant provide solution to k8sgpt on Kubernetes."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )
    return res.choices[0].message.content.strip()

def run_qa():
    """Run a simple QA example"""
    query = "是否可以改動 poor namespace 中的內容?"
    docs = query_docs(
        query=query,
        collection_name="rag",
        model="text-embedding-3-large")
    answer = generate_answer(
        query=query,
        docs=docs,
        model="gpt-4o-mini")
    print("\n🧠 回答：")
    print(answer)
# run_qa() # uncomment to run the QA example

# Build k8sgpt custom rest backend: https://docs.k8sgpt.ai/tutorials/custom-rest-backend/

from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel
class CustomRestRequest(BaseModel):
    """
    Represents a custom request to a REST API.
    """
    model: str
    # Prompt is the textual prompt to send to the model.
    prompt: str
    # Options lists model-specific options. For example, temperature can be
    # set through this field, if the model supports it.
    options: Dict[str, Any]

class CustomRestResponse(BaseModel):
    """
    Represents a custom response from a REST API.
    """
    # Model is the model name that generated the response.
    model: str
    # CreatedAt is the timestamp of the response.
    # example "2006-01-02T15:04:05Z07:00"
    created_at: str
    # Response is the textual response itself.
    response: str

# API with FastAPI
import asyncio
from typing import Union
from fastapi import FastAPI

app = FastAPI()
model=os.getenv("MODEL_NAME", "gpt-4o-mini")

@app.post("/completions")
async def completions(req: CustomRestRequest) -> CustomRestResponse:

    message = req.options["message"] if "message" in req.options else "No message provided"
    print("Received promt: ", req.prompt)
    print("Received message: ", message)
    docs = query_docs(
        #query=message,
        query=req.prompt,
        collection_name="rag",
        model="text-embedding-3-large")

    answer = generate_answer(
        query=message,
        #query=req.prompt,
        docs=docs,
        model="gpt-4o-mini")

    return CustomRestResponse(
        model=model,
        created_at=datetime.utcnow().isoformat() + "Z",
        response=answer
    )
