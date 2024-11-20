#set GROQ_API_KEY in the secrets
import os
from groq import Groq
from dotenv import load_dotenv

# Create the Groq client
load_dotenv(dotenv_path="key.env")

api_key = os.environ.get("GROQ_API_KEY") 
client = Groq(api_key=api_key)
model = 'llama3-8b-8192'
token_count = 1000
temperature = 1.2