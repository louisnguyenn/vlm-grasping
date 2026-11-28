import cv2
from pathlib import Path

image_path = "data/cornell/01/pcd0100r.png"

image = cv2.imread(image_path)

if image is None:
    raise FileNotFoundError(image_path)

height, width = image.shape[:2]

# Gemini's normalized prediction
y_norm = 638
x_norm = 442

# Convert to original image coordinates
x = round(x_norm / 1000 * width)
y = round(y_norm / 1000 * height)

# Draw predicted grasp centre
cv2.circle(image, (x, y), 6, (0, 0, 255), -1)

# Draw crosshair
cv2.drawMarker(
    image,
    (x, y),
    (0, 0, 255),
    cv2.MARKER_CROSS,
    25,
    2
)

# Add coordinate label
cv2.putText(
    image,
    f"Grasp center: ({x}, {y})",
    (x + 10, y - 10),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.5,
    (0, 0, 255),
    2
)

# Save visualization
Path("results").mkdir(exist_ok=True)

cv2.imwrite(
    "results/pcd0100_prediction.png",
    image
)

print(f"Predicted center: ({x}, {y})")
print("Visualization saved.")
