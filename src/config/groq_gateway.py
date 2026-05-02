from langchain_groq import ChatGroq
import itertools
import time
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ========================
# API KEYS
# ========================
# API Keys are loaded from .env file (GROQ_KEYS environment variable)
# Format in .env: GROQ_KEYS=key1,key2,key3,...
_groq_keys_str = os.getenv("GROQ_KEYS", "")
GROQ_KEYS = [key.strip() for key in _groq_keys_str.split(",") if key.strip()] if _groq_keys_str else []

# ========================
# KEY ROTATION
# ========================
key_cycle = itertools.cycle(GROQ_KEYS) if GROQ_KEYS else None

def get_llm(model: str = "llama-3.1-8b-instant", temperature: float = 0):
    if not GROQ_KEYS:
        raise ValueError("Chưa cấu hình GROQ_KEYS trong groq_gateway.py")
    api_key = next(key_cycle)
    return ChatGroq(
        model=model,
        api_key=api_key,
        temperature=temperature
    )

# ========================
# SAFE INVOKE
# ========================
def invoke_llm(prompt, retries=3, model: str = "llama-3.1-8b-instant", temperature: float = 0):
    for _ in range(retries):
        try:
            llm = get_llm(model=model, temperature=temperature)
            response = llm.invoke(prompt)
            return response.content
        except Exception as e:
            print("Groq error, switching key:", e)
            time.sleep(1)
    return "I'm temporarily unable to answer."