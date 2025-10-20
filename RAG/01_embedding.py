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

qa_df = pd.read_csv('data/qa.csv')
qa_df.info()
print(qa_df.sample())

# Initialize OpenAI client
from openai import AzureOpenAI
openai_client = AzureOpenAI()
def embedding(input: str, model: str="text-embedding-3-large") -> str:
    response = openai_client.embeddings.create(
        input = input,
        model= model,
    )
    return response.data[0].embedding

# embedding with progress bar
from tqdm import tqdm

tqdm.pandas(desc="Generating question embeddings")
qa_df['question_vector'] = qa_df['question'].progress_apply(
    lambda x: embedding(x, model="text-embedding-3-large")
)

tqdm.pandas(desc="Generating answer embeddings")
qa_df['answer_vector'] = qa_df['answer'].progress_apply(
    lambda x: embedding(x, model="text-embedding-3-large")
)

# save to csv
qa_df.to_csv("data/qa_embedded_text_embedding_3_large.csv", index=False)
