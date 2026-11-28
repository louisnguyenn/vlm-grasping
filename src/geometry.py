import math


def normalized_to_pixel(point, image_width, image_height):
    """Convert normalized coordinates to image coordinates."""

    return {
        "x": point["x"] / 1000 * image_width,
        "y": point["y"] / 1000 * image_height
    }


def calculate_grasp(contact_1, contact_2):
    """Calculate grasp geometry from opposing contact points."""

    x1, y1 = contact_1["x"], contact_1["y"]
    x2, y2 = contact_2["x"], contact_2["y"]

    # Calculate grasp centre
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2

    # Calculate contact separation
    width = math.hypot(x2 - x1, y2 - y1)

    if width == 0:
        raise ValueError("Contact points must be distinct")

    # Calculate gripper closing angle
    angle = math.degrees(
        math.atan2(y2 - y1, x2 - x1)
    )

    # Normalize parallel-jaw angle to [-90, 90)
    angle = (angle + 90) % 180 - 90

    return {
        "x": center_x,
        "y": center_y,
        "angle_deg": angle,
        "width_px": width
    }
