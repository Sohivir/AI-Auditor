from groq import Groq

from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

def get_llm():
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    return client



#print(chat_completion.choices[0].message.content)

