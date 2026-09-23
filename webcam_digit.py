import cv2
import numpy as np


# ============================================================
# Open webcam
# ============================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not open webcam.")
    raise SystemExit(1)


print("Webcam opened successfully.")
print("Write a digit on paper and place it inside the box.")
print("Press Q to quit.")


while True:

    ret, frame = cap.read()

    if not ret:
        print("ERROR: Could not read webcam frame.")
        break


    # --------------------------------------------------------
    # Flip image horizontally so it behaves like a mirror
    # --------------------------------------------------------

    frame = cv2.flip(frame, 1)


    # --------------------------------------------------------
    # Get frame dimensions
    # --------------------------------------------------------

    height, width = frame.shape[:2]


    # --------------------------------------------------------
    # Create a square region in the center
    # --------------------------------------------------------

    box_size = min(height, width) // 2

    x1 = width // 2 - box_size // 2
    y1 = height // 2 - box_size // 2

    x2 = x1 + box_size
    y2 = y1 + box_size


    # --------------------------------------------------------
    # Draw region of interest
    # --------------------------------------------------------

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        (0, 255, 0),
        2
    )


    # --------------------------------------------------------
    # Extract digit region
    # --------------------------------------------------------

    roi = frame[y1:y2, x1:x2]


    # --------------------------------------------------------
    # Convert to grayscale
    # --------------------------------------------------------

    gray = cv2.cvtColor(
        roi,
        cv2.COLOR_BGR2GRAY
    )


    # --------------------------------------------------------
    # Threshold
    #
    # MNIST uses:
    #   black background
    #   white digit
    #
    # So we invert the camera image.
    # --------------------------------------------------------

    _, binary = cv2.threshold(
        gray,
        100,
        255,
        cv2.THRESH_BINARY_INV
    )


    # --------------------------------------------------------
    # Resize to MNIST 28 x 28
    # --------------------------------------------------------

    digit_28 = cv2.resize(
        binary,
        (28, 28),
        interpolation=cv2.INTER_AREA
    )


    # --------------------------------------------------------
    # Display processed image enlarged
    # --------------------------------------------------------

    preview = cv2.resize(
        digit_28,
        (280, 280),
        interpolation=cv2.INTER_NEAREST
    )


    cv2.imshow(
        "Processed 28x28 Digit",
        preview
    )


    cv2.imshow(
        "Webcam - Place Digit Inside Green Box",
        frame
    )


    # --------------------------------------------------------
    # Press Q to quit
    # --------------------------------------------------------

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


# ============================================================
# Cleanup
# ============================================================

cap.release()

cv2.destroyAllWindows()

print("Webcam closed.")