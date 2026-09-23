import cv2
import numpy as np
import tensorflow as tf
import serial
import time


# ============================================================
# Configuration
# ============================================================

MODEL_PATH = r"venv\model_int8.tflite"

SERIAL_URL = "rfc2217://localhost:4000"

BAUD_RATE = 115200

CAMERA_INDEX = 0


# ============================================================
# Load INT8 model
# ============================================================

print("Loading INT8 model...")

interpreter = tf.lite.Interpreter(
    model_path=MODEL_PATH
)

interpreter.allocate_tensors()

input_details = interpreter.get_input_details()[0]

scale = input_details["quantization"][0]

zero_point = input_details["quantization"][1]

print("Input scale:", scale)

print("Input zero point:", zero_point)


# ============================================================
# Open webcam
# ============================================================

print("\nOpening webcam...")

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():

    print("ERROR: Could not open webcam.")

    raise SystemExit(1)


print("Webcam opened successfully.")


# ============================================================
# Connect to Pico
# ============================================================

print("\nConnecting to Wokwi Pico...")

ser = serial.serial_for_url(
    SERIAL_URL,
    baudrate=BAUD_RATE,
    timeout=2
)

time.sleep(1)

print("Connected to Pico.")


# ============================================================
# Handshake
# ============================================================

print("\nSynchronizing with Pico...")

ser.reset_input_buffer()

ser.write(b"PING\n")

ser.flush()


while True:

    line = (
        ser.readline()
        .decode(errors="ignore")
        .strip()
    )

    if line:
        print("Pico:", line)

    if line == "READY":
        break


print("Pico is READY.")


# ============================================================
# Webcam loop
# ============================================================

print("\n======================================")

print(" WEBCAM MNIST DIGIT RECOGNITION")

print("======================================")

print("Place a handwritten digit inside the")
print("green box.")

print()

print("Press SPACE to capture and classify.")

print("Press Q to quit.")

print("======================================\n")


while True:

    # --------------------------------------------------------
    # Capture frame
    # --------------------------------------------------------

    ret, frame = cap.read()

    if not ret:

        print("ERROR: Could not read webcam.")

        break


    # --------------------------------------------------------
    # Mirror image
    # --------------------------------------------------------

    frame = cv2.flip(frame, 1)


    # --------------------------------------------------------
    # Frame dimensions
    # --------------------------------------------------------

    height, width = frame.shape[:2]


    # --------------------------------------------------------
    # Create square region of interest
    # --------------------------------------------------------

    box_size = min(height, width) // 2


    x1 = width // 2 - box_size // 2

    y1 = height // 2 - box_size // 2

    x2 = x1 + box_size

    y2 = y1 + box_size


    # --------------------------------------------------------
    # Draw green box
    # --------------------------------------------------------

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        (0, 255, 0),
        2
    )


    # --------------------------------------------------------
    # Extract ROI
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
    # --------------------------------------------------------

    _, binary = cv2.threshold(
        gray,
        100,
        255,
        cv2.THRESH_BINARY_INV
    )


    # --------------------------------------------------------
    # Resize to 28 x 28
    # --------------------------------------------------------

    digit_28 = cv2.resize(
        binary,
        (28, 28),
        interpolation=cv2.INTER_AREA
    )


    # --------------------------------------------------------
    # Display processed digit
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
    # Keyboard
    # --------------------------------------------------------

    key = cv2.waitKey(1) & 0xFF


    # ========================================================
    # SPACE = classify digit
    # ========================================================

    if key == 32:

        print("\nCapturing digit...")


        # ----------------------------------------------------
        # Convert image to float
        # ----------------------------------------------------

        digit_float = digit_28.astype(
            np.float32
        )


        # ----------------------------------------------------
        # INT8 quantization
        # ----------------------------------------------------

        digit_int8 = np.round(
            digit_float / scale
            + zero_point
        )


        digit_int8 = np.clip(
            digit_int8,
            -128,
            127
        ).astype(np.int8)


        # ----------------------------------------------------
        # Display quantized range
        # ----------------------------------------------------

        print(
            "INT8 range:",
            int(digit_int8.min()),
            "to",
            int(digit_int8.max())
        )


        # ----------------------------------------------------
        # Send image row by row
        # ----------------------------------------------------

        print("Sending image to Pico...")


        success = True


        for row in range(28):

            row_pixels = digit_int8[row]


            values = " ".join(
                str(int(value))
                for value in row_pixels
            )


            message = (
                f"ROW {row} {values}\n"
            )


            ser.write(
                message.encode()
            )

            ser.flush()


            # ----------------------------------------------
            # Wait for ACK
            # ----------------------------------------------

            while True:

                response = (
                    ser.readline()
                    .decode(errors="ignore")
                    .strip()
                )


                if not response:

                    continue


                if response.startswith("ERROR"):

                    print(
                        "Pico:",
                        response
                    )

                    success = False

                    break


                if response == f"ACK:{row}":

                    break


            if not success:

                break


        # ----------------------------------------------------
        # If transfer failed
        # ----------------------------------------------------

        if not success:

            print("ERROR: Image transfer failed.")

            continue


        print("All 28 rows sent.")

        print("Waiting for Pico prediction...")


        # ----------------------------------------------------
        # Receive prediction
        # ----------------------------------------------------

        prediction = None

        latency = None


        while True:

            response = (
                ser.readline()
                .decode(errors="ignore")
                .strip()
            )


            if not response:

                continue


            print("Pico:", response)


            if response.startswith(
                "PREDICTION:"
            ):

                prediction = int(
                    response.split(":", 1)[1]
                )


            elif response.startswith(
                "LATENCY_US:"
            ):

                latency = int(
                    response.split(":", 1)[1]
                )


            elif response == "READY":

                break


        # ----------------------------------------------------
        # Display result
        # ----------------------------------------------------

        print()

        print("======================================")

        print("          PICO RESULT")

        print("======================================")


        print(
            "Predicted digit:",
            prediction
        )


        if latency is not None:

            print(
                "Pico latency   :",
                latency,
                "us",
                f"({latency / 1000:.2f} ms)"
            )


        print("======================================")

        print()


        # ----------------------------------------------------
        # Show prediction on webcam
        # ----------------------------------------------------

        if prediction is not None:

            cv2.putText(
                frame,
                f"Prediction: {prediction}",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 0),
                3
            )


            cv2.imshow(
                "Webcam - Place Digit Inside Green Box",
                frame
            )


    # ========================================================
    # Q = quit
    # ========================================================

    elif key == ord("q"):

        break


# ============================================================
# Cleanup
# ============================================================

cap.release()

cv2.destroyAllWindows()

ser.close()

print("\nProgram finished.")