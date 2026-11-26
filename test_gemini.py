import os

from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

response = client.models.generate_content(
    model=os.environ["GEMINI_MODEL"],
    contents="Explain robotic parallel-jaw grasping."
)

print(response.text)
