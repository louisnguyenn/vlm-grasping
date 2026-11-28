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

prompt = f"""
You are a robotic grasp planning system.

Analyze the provided RGB image and predict
one stable top-down parallel-jaw grasp.

Image width: {image.width} pixels.
Image height: {image.height} pixels.

Coordinate conventions:
- Origin is the top-left corner.
- Positive x points right.
- Positive y points down.
- All spatial measurements must be in pixels.
- Angle is measured clockwise from the positive
  x-axis to the gripper closing axis.
- Angle must be between -90 and 90 degrees.
- Width is the distance between the opposing jaws.
- Height is the length of the jaw contact region.

Return one numerical value for each parameter.
Do not return ranges.

Return only a JSON object in this format:

{{
    "object": "object name",
    "grasp": {{
        "x": 0.0,
        "y": 0.0,
        "angle_deg": 0.0,
        "width_px": 0.0,
        "height_px": 0.0
    }},
    "reasoning": "brief grasp justification"
}}

The numerical values above are placeholders.
Determine the actual values from the image.
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
