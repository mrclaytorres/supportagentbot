import weaviate
import json
import os
from dotenv import load_dotenv

load_dotenv()

def create_query(concept, query):
  client = weaviate.Client(
      url = 'https://' + os.getenv("WEAVIATE_HOST"),  # Replace with your endpoint
      auth_client_secret=weaviate.AuthApiKey(api_key=os.getenv("WEAVIATE_KEY")),  # Replace w/ your Weaviate instance API key
      additional_headers = {
          "X-HuggingFace-Api-Key": os.getenv("WEAVIATE_KEY")  # Replace with your inference API key
      }
  )

  nearText = {"concepts": [concept],
              "question": query}

  response = (
      client.query
      .get("Brain", ['question', 'answer'])
      .with_near_text(nearText)
      .with_limit(2)
      .do()
  )

  # print(json.dumps(response, indent=4))
  return response