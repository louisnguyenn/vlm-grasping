import os
import time

from google import genai
from dotenv import load_dotenv
from PIL import Image

from src.dataset import CornellDataset


load_dotenv()

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

model = os.environ["GEMINI_MODEL"]

dataset = CornellDataset("data/cornell")

sample = dataset[0]

image = Image.open(
    sample["image_path"]
).convert("RGB")

prompt = """
You are a robotic grasp planning system.

Analyze the provided RGB image and predict
one stable top-down parallel-jaw grasp.

Coordinate conventions:
- Use a normalized coordinate system from 0 to 1000.
- The origin is the top-left corner.
- Positive x points right.
- Positive y points down.
- The bottom-right image boundary is (1000, 1000).
- Do not convert coordinates into pixels.

Identify the following:
1. The grasp center.
2. The first gripper contact point.
3. The opposing gripper contact point.

The contact points should lie on opposing
surfaces of the target object.

Return only a JSON object in this format:

{
    "object": "object name",
    "grasp": {
        "center": {
            "x": 0,
            "y": 0
        },
        "contact_1": {
            "x": 0,
            "y": 0
        },
        "contact_2": {
            "x": 0,
            "y": 0
        }
    },
    "reasoning": "brief grasp justification"
}

All numerical values are placeholders.
Determine the actual coordinates from the image.
"""

print(f"Model: {model}")
print(f"Image ID: {sample['image_id']}")
print(f"Image path: {sample['image_path']}")
print(f"Image dimensions: {image.size}")

start_time = time.perf_counter()

response = client.models.generate_content(
    model=model,
    contents=[image, prompt]
)

elapsed_time = time.perf_counter() - start_time

print("\nModel response:")
print(response.text)

print(f"\nRequest latency: {elapsed_time:.2f} seconds")
