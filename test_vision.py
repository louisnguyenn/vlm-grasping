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
Identify the object in this image.

Determine where a top-down parallel-jaw
robotic gripper should grasp the object
to achieve a stable grasp.

Describe the grasp location and orientation,
and explain why the proposed grasp is suitable.
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
