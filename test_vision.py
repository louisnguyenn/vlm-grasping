import os

from google import genai
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

image_path = "data/cornell/01/pcd0164r.png"

image = Image.open(image_path).convert("RGB")

prompt = """
Identify the object in this image.

Determine where a top-down parallel-jaw
robotic gripper should grasp the object
to achieve a stable grasp.

Describe the grasp location and orientation.
"""

response = client.models.generate_content(
    model=os.environ["GEMINI_MODEL"],
    contents=[image, prompt]
)

print("Image dimensions:", image.size)
print("Model response:")
print(response.text)
