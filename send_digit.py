import tensorflow as tf
import numpy as np
import serial
import time


# ============================================================
# Configuration
# ============================================================

MODEL_PATH = r"venv\model_int8.tflite"

TEST_INDEX = 0

SERIAL_URL = "rfc2217://localhost:4000"

BAUD_RATE = 115200


# ============================================================
# Load MNIST
# ============================================================

print("Loading MNIST...")

(_, _), (x_test, y_test) = tf.keras.datasets.mnist.load_data()


image = x_test[TEST_INDEX]

true_label = int(y_test[TEST_INDEX])


print("True digit:", true_label)


# ============================================================
# Load INT8 TensorFlow Lite model
# ============================================================

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
# Quantize MNIST image to INT8
# ============================================================

image_int8 = np.round(
    image.astype(np.float32) / scale
    + zero_point
)


image_int8 = np.clip(
    image_int8,
    -128,
    127
).astype(np.int8)


# Confirm 28 x 28 image
assert image_int8.shape == (28, 28)


print("Image shape:", image_int8.shape)

print("Number of pixels:", image_int8.size)

print(
    "INT8 range:",
    int(image_int8.min()),
    "to",
    int(image_int8.max())
)


# ============================================================
# Connect to Wokwi
# ============================================================

print("\nConnecting to Wokwi...")


ser = serial.serial_for_url(
    SERIAL_URL,
    baudrate=BAUD_RATE,
    timeout=2
)


time.sleep(1)


print("Connected to Wokwi.")


# ============================================================
# Handshake
# ============================================================

print("\nRequesting Pico READY...")


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


# ============================================================
# Send image row by row
# ============================================================

print("\nSending digit:", true_label)

print("Sending 28 rows...")


for row in range(28):

    # Get one row containing 28 pixels
    row_pixels = image_int8[row]


    # Convert INT8 values to text
    values = " ".join(
        str(int(value))
        for value in row_pixels
    )


    # Create command
    message = f"ROW {row} {values}\n"


    # Send row
    ser.write(message.encode())

    ser.flush()


    # Wait for ACK
    while True:

        line = (
            ser.readline()
            .decode(errors="ignore")
            .strip()
        )


        if not line:

            continue


        print("Pico:", line)


        if line == f"ACK:{row}":

            break


print("All 28 rows sent.")


# ============================================================
# Receive inference result
# ============================================================

prediction = None

latency = None

output_values = None


while True:

    line = (
        ser.readline()
        .decode(errors="ignore")
        .strip()
    )


    if not line:

        continue


    print("Pico:", line)


    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    if line.startswith("PREDICTION:"):

        prediction = int(
            line.split(":", 1)[1]
        )


    # --------------------------------------------------------
    # Latency
    # --------------------------------------------------------

    elif line.startswith("LATENCY_US:"):

        latency = int(
            line.split(":", 1)[1]
        )


    # --------------------------------------------------------
    # Output values
    # --------------------------------------------------------

    elif line.startswith("OUTPUT:"):

        values = line.split(":", 1)[1]

        output_values = [
            int(x)
            for x in values.split(",")
        ]


    # --------------------------------------------------------
    # READY means complete inference cycle
    # --------------------------------------------------------

    elif line == "READY":

        break


# ============================================================
# Display result
# ============================================================

print()

print("====================================")

print("          MNIST TEST RESULT")

print("====================================")


print("True digit :", true_label)

print("Prediction :", prediction)


if latency is not None:

    print(
        "Latency    :",
        latency,
        "us",
        f"({latency / 1000:.2f} ms)"
    )


if output_values is not None:

    print(
        "Output     :",
        output_values
    )


if prediction == true_label:

    print("Result     : CORRECT")

else:

    print("Result     : INCORRECT")


print("====================================")


ser.close()