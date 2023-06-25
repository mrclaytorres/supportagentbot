import os
import os.path
import shutil
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
import openai
import langchain
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain import OpenAI, VectorDBQA
import nltk
nltk.download("punkt")
from dotenv import load_dotenv

import weaviate
from weaviate_store import store
from weaviate_query import create_query

app = FastAPI()

load_dotenv()

document_folder = './files/'

# Extract PDF Text
def extract_file(file):
  
  loader = UnstructuredFileLoader(file)
  documents = loader.load()
  return documents

# Create chucks
def create_splitter(documents):

  text_splitter = CharacterTextSplitter(separator="\n", chunk_size=800,  chunk_overlap=100)
  texts = text_splitter.split_documents(documents)

  return texts

def create_embeddings():

  embeddings = OpenAIEmbeddings(openai_api_key = os.getenv("OPENAI_APIKEY"))
  return embeddings

@app.get("/")
async def root():
  return {"message": "Hello World"}

# Upload PDF
@app.post("/upload")
async def upload(file: UploadFile = File(...)):

  with open(os.path.join(document_folder, file.filename), "wb") as buffer:
    shutil.copyfileobj(file.file, buffer)

  document_name = file.filename

  # Extract PDF Text
  documents = extract_file(os.path.join(document_folder, file.filename))

  # Create chunks using textsplitter
  texts = create_splitter(documents)

  # Convert and Store Vector Embeddings
  embeddings = create_embeddings()

  # store(texts, document_name)
  
  return {"file_name": file.filename, 
          "texts":texts}

# Create search query
@app.get("/chat")
async def chat(concept: str, question: str):
  response = create_query(concept, question)

  return response

# Check Weaviate Classes
@app.get("/schema")
async def schema():
  client = weaviate.Client(
      url = 'https://' + os.getenv("WEAVIATE_HOST"),  # Replace with your endpoint
      auth_client_secret=weaviate.AuthApiKey(api_key=os.getenv("WEAVIATE_KEY")),  # Replace w/ your Weaviate instance API key
      additional_headers = {
          "X-HuggingFace-Api-Key": os.getenv("WEAVIATE_KEY")  # Replace with your inference API key
      }
  )

  schema = client.schema.get()
  return schema