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

# Extract PDF Text
def extract_file(file):
  
  loader = UnstructuredFileLoader(file)
  documents = loader.load()
  return documents

# Create chucks
def splitter(documents):

  text_splitter = CharacterTextSplitter(chuck_size=800,  chuck_overlap=0)
  texts = text_splitter.split_documents(documents)

@app.get("/")
async def root():
  return {"message": "Hello World"}

# Upload PDF
@app.post("/upload")
async def upload(file: UploadFile = File(...)):

  with open(os.path.join(document_folder, file.filename), "wb") as buffer:
    shutil.copyfileobj(file.file, buffer)

  # Extract PDF Text
  documents = extract_file(os.path.join(document_folder, file.filename))

  # Create chunks using textsplitter
  splitter(documents)

  # Convert and Store Vector Embeddings
  

  # store(file)
  
  return {"file_name": file.filename, 
          "len":len(documents)}

# Convert PDF Data into Vector Embedding and Store in Vector DB
# Create Embedding query