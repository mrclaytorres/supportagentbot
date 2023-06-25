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

from weaviate_store import store

app = FastAPI()

document_folder = './files/'

@app.get("/")
async def root():
  return {"message": "Hello World"}

# Upload PDF
@app.post("/upload")
async def upload(file: UploadFile = File(...)):

  with open(os.path.join(document_folder, file.filename), "wb") as buffer:
    shutil.copyfileobj(file.file, buffer)

  # Extract PDF Text
  loader = UnstructuredFileLoader(os.path.join(document_folder, file.filename))
  documents = loader.load()
  len(documents)

  # Convert and Store Vector Embeddings
  # store(file)
  
  return {"file_name": file.filename}

# Convert PDF Data into Vector Embedding and Store in Vector DB
# Create Embedding query