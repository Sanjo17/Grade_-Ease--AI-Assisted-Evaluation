import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
Api_key = os.environ.get('HUGGING_FACE_API_KEY')
API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"


class Grading():
    
    # word counting
    def count_words(text):
        if len(text)==0:
            return 0
        # Split the text into words based on spaces
        words = text.split()
        # Return the count of words
        return len(words)

    # fn for geting similarity score
    def marking(payload):
        headers = {"Authorization": f"Bearer {Api_key}"}
        response = requests.post(API_URL, headers=headers, json=payload)
        print(response)
        return response.json()


# data = query(
#     {
#         "inputs": {
#             "source_sentence": source_sentence,
#             "sentences":[sentence1]
#         }
#     })
# print(data)
## [0.605, 0.894]
