import os
from dotenv import load_dotenv

import weaviate
import json

def store(document):
  # Connect to Weaviate
  client = weaviate.Client(
      url = 'https://' + os.getenv("WEAVIATE_HOST"),  # Replace with your endpoint
      auth_client_secret=weaviate.AuthApiKey(api_key=os.getenv("WEAVIATE_KEY")),  # Replace w/ your Weaviate instance API key
      additional_headers = {
          "X-HuggingFace-Api-Key": os.getenv("WEAVIATE_KEY")  # Replace with your inference API key
      }
  )

  # Define a data collection (a "class" in Weaviate) to store objects in.
  class_obj = {
      "class": "Brain",
      "vectorizer": "text2vec-huggingface",  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
      "moduleConfig": {
          "text2vec-huggingface": {
              "model": "sentence-transformers/all-MiniLM-L6-v2",  # Can be any public or private Hugging Face model.
              "options": {
                  "waitForModel": True
              }
          }
      }
  }

  client.schema.create_class(class_obj)