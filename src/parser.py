import json
import math

# Extract and validate model predictions

def parse_response(response_text):
    """Extract JSON from a VLM response."""

    text = response_text.strip()

    if text.startswith("```"):
        lines = text.splitlines()

        if lines[-1].strip() != "```":
            raise ValueError("Incomplete Markdown code fence")

        text = "\n".join(lines[1:-1])

    return json.loads(text)


def validate_point(point):
    """Validate a normalized spatial coordinate."""

    for axis in ("x", "y"):
        value = point[axis]

        if isinstance(value, bool) or not isinstance(
            value, (int, float)
        ):
            raise ValueError(f"{axis} must be numeric")

        if not math.isfinite(value):
            raise ValueError(f"{axis} must be finite")

        if not 0 <= value <= 1000:
            raise ValueError(f"{axis} is out of bounds")


def validate_prediction(prediction):
    """Validate a contact-point-based grasp prediction."""

    grasp = prediction["grasp"]

    for key in ("center", "contact_1", "contact_2"):
        validate_point(grasp[key])

    if grasp["contact_1"] == grasp["contact_2"]:
        raise ValueError("Contact points must be distinct")

    return True
