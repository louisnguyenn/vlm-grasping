import cv2
import numpy as np
from pathlib import Path

from src.geometry import normalized_to_pixel, calculate_grasp


image_path = "data/cornell/01/pcd0100r.png"

image = cv2.imread(image_path)

if image is None:
    raise FileNotFoundError(image_path)

height, width = image.shape[:2]

# Original Gemini prediction
contact_1 = normalized_to_pixel(
    {"x": 409, "y": 638},
    width,
    height
)

contact_2 = normalized_to_pixel(
    {"x": 471, "y": 638},
    width,
    height
)

grasp = calculate_grasp(contact_1, contact_2)

# Temporary rectangle height for visualization
grasp_height = 25.0

rectangle = (
    (grasp["x"], grasp["y"]),
    (grasp["width_px"], grasp_height),
    grasp["angle_deg"]
)

box = cv2.boxPoints(rectangle)
box = np.round(box).astype(np.int32)

# Draw grasp rectangle
cv2.drawContours(
    image, [box], 0, (0, 255, 0), 2
)

# Draw contact points
for point in (contact_1, contact_2):
    cv2.circle(
        image,
        (round(point["x"]), round(point["y"])),
        4,
        (255, 0, 0),
        -1
    )

# Draw grasp centre
cv2.circle(
    image,
    (round(grasp["x"]), round(grasp["y"])),
    4,
    (0, 0, 255),
    -1
)

Path("results").mkdir(exist_ok=True)

cv2.imwrite(
    "results/pcd0100_grasp.png",
    image
)

print("Grasp visualization saved.")
