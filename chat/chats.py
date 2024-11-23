import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
import uvicorn
import asyncio

# Load environment variables
load_dotenv(dotenv_path="key.env")

# Initialize FastAPI app
app = FastAPI(title="Groq Chatbot API")

# Allow CORS for specific origins (frontend URL)
origins = [
    "http://127.0.0.1:5500",  # Frontend origin
    "http://localhost:5500",  # Alternative localhost URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Groq and LangChain Configuration
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is not set in the environment variables.")

client = Groq(api_key=api_key)
model = "llama3-8b-8192"
system_prompt = "You are a friendly conversational chatbot"
conversational_memory_length = 5

# Initialize the Groq Chat object
groq_chat = ChatGroq(groq_api_key=api_key, model_name=model)

# Initialize conversational memory
memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history", return_messages=True)

# Prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content=system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{human_input}"),
    ]
)

# Define input model for FastAPI
class UserQuery(BaseModel):
    question: str

@app.post("/chat")
async def chat(query: UserQuery):
    """
    Chat with the Groq chatbot.
    """
    try:
        conversation = LLMChain(
            llm=groq_chat,
            prompt=prompt,
            verbose=False,
            memory=memory,
        )

        await asyncio.sleep(3)
        response = conversation.predict(human_input=query.question)
        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/")
def root():
    return {"message": "Welcome to the Groq Chatbot API!"}

# Uvicorn entry point
if __name__ == "__main__":
    uvicorn.run("chats:app", port=8002, reload=True)
