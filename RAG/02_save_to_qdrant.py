import os
from dotenv import find_dotenv
from dotenv import load_dotenv

# load env variables from the .env file
load_dotenv(find_dotenv())

# Note. alternatively you can set a temporary env variable like this:
#os.environ["OPENAI_API_KEY"] = ""
#os.environ["AZURE_OPENAI_API_KEY"]=""
#os.environ["AZURE_OPENAI_ENDPOINT"]=""
#os.environ["OPENAI_API_VERSION"]="2024-12-01-preview"
#os.environ["OPENAI_MODEL"]="text-embedding-3-large"

# load training data
import pandas as pd

qa_df = pd.read_csv('data/qa_embedded_text_embedding_3_large.csv')

# Read vectors from strings back into a list
from ast import literal_eval
qa_df["question_vector"] = qa_df.question_vector.apply(literal_eval)
qa_df["answer_vector"] = qa_df.answer_vector.apply(literal_eval)

qa_df.info()
print(qa_df.sample())

# Initialize OpenAI client
from openai import AzureOpenAI
openai_client = AzureOpenAI()

# Initialize Qdrant client
# Note: make sure you have Qdrant running in your Kubernetes cluster and port-forwarded to localhost:6334
# kubectl -n qdrant port-forward svc/qdrant 6334:6334

import qdrant_client
client = qdrant_client.QdrantClient(
    host="localhost",
    prefer_grpc=True,
)
client.get_collections()

# create collection
collection_name = "rag"

# delete collection before creating a new one
client.delete_collection(collection_name=collection_name)

# vector_size = 3072
print(len(qa_df.iloc[0]["question_vector"]))
vector_size = len(qa_df.iloc[0]["question_vector"])

from qdrant_client.http import models as rest
client.create_collection(
    collection_name=collection_name,
    vectors_config={
        "question": rest.VectorParams(
            distance=rest.Distance.COSINE,
            size=vector_size,
        ),
        "answer": rest.VectorParams(
            distance=rest.Distance.COSINE,
            size=vector_size,
        ),
    }
)

# upsert data to Qdrant
client.upsert(
    collection_name=collection_name,
    points=[
        rest.PointStruct(
            id=k,
            vector={
                "question": v["question_vector"],
                "answer": v["answer_vector"],
            },
            payload=v.to_dict(),
        )
        for k, v in qa_df.iterrows()
    ],
)

# Check the collection size to make sure all the points have been stored
print("Total points in collection:")
print(client.count(collection_name="rag"))
