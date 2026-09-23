# MNIST Digit Recognition – Edge AI Deployment

## 1. How to Run

### Step 1: Open the project

Open PowerShell in:

```text
D:\AMRITA\SEMESTER 5\EOCandelectronics\Assignment\MNIST_PICO
```

### Step 2: Activate the Python environment

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Start the Wokwi Pico simulation

Open the `pico\mnist_pico` project in VS Code and start the Wokwi simulation.

The Pico should display:

```text
Model loaded successfully.
Tensor allocation successful.
READY
```

### Step 4: Run the webcam application

In another PowerShell terminal:

```powershell
cd "D:\AMRITA\SEMESTER 5\EOCandelectronics\Assignment\MNIST_PICO"
.\venv\Scripts\python.exe webcam_to_pico.py
```

A webcam window will open.

* Place a handwritten/displayed digit inside the green box.
* Press **SPACE** to classify.
* Press **Q** to exit.

The prediction and Pico inference latency will be displayed.

---

# 2. Project Overview

This project implements a lightweight **MNIST digit recognition system** and deploys the quantized model on a **Raspberry Pi Pico** using TensorFlow Lite Micro.

The laptop webcam captures a digit, OpenCV preprocesses it into a 28×28 image, and the INT8 image is sent to the Pico for local inference.

---

# 3. System Pipeline

```text
MNIST
  ↓
CNN Training
  ↓
TensorFlow Lite
  ↓
INT8 Quantization
  ↓
Raspberry Pi Pico
  ↑
Webcam
  ↓
OpenCV Preprocessing
  ↓
28×28 INT8 Image
  ↓
Serial Transfer
  ↓
Pico Inference
  ↓
Prediction
```

---

# 4. Model Architecture

```text
Input: 28 × 28 × 1
        ↓
Conv2D: 8 filters, 3×3, ReLU
        ↓
MaxPooling: 2×2
        ↓
Conv2D: 16 filters, 3×3, ReLU
        ↓
MaxPooling: 2×2
        ↓
Flatten
        ↓
Dense: 32, ReLU
        ↓
Dense: 10, Softmax
        ↓
Digit 0–9
```

---

# 5. Training Setup

| Parameter       | Value                           |
| --------------- | ------------------------------- |
| Dataset         | MNIST                           |
| Training images | 60,000                          |
| Test images     | 10,000                          |
| Image size      | 28×28                           |
| Classes         | 10                              |
| Optimizer       | Adam                            |
| Learning rate   | 0.001                           |
| Loss            | Sparse Categorical Crossentropy |
| Batch size      | 128                             |
| Epochs          | 5                               |

---

# 6. Optimization and Quantization

The trained model is converted to TensorFlow Lite and optimized using **full integer INT8 post-training quantization**.

A representative dataset is used for quantization calibration.

The deployed input uses:

```text
Type       : INT8
Scale      : 0.0039215689
Zero point : -128
Shape      : 1 × 28 × 28 × 1
```

Quantization:

```text
q = round(x / scale) + zero_point
```

---

# 7. Webcam Preprocessing

OpenCV performs:

```text
Webcam Frame
     ↓
Flip
     ↓
Center ROI
     ↓
Grayscale
     ↓
Threshold
     ↓
Resize
     ↓
28 × 28
     ↓
INT8
```

The processed image is designed to match the MNIST model input.

---

# 8. Edge Deployment

The INT8 model is embedded into the Raspberry Pi Pico firmware and executed using **TensorFlow Lite Micro**.

The Pico:

1. Receives the 28×28 INT8 image.
2. Loads it into the input tensor.
3. Runs inference.
4. Finds the predicted digit.
5. Measures inference latency.
6. Sends the result back to the laptop.

Required operators include:

```text
CONV_2D
MAX_POOL_2D
SHAPE
STRIDED_SLICE
PACK
RESHAPE
FULLY_CONNECTED
SOFTMAX
```

---

# 9. Communication

The laptop first synchronizes with the Pico:

```text
Laptop → PING
Pico   → READY
```

The image is then transferred as **28 rows of 28 INT8 values**.

```text
ROW 0  → ACK:0
ROW 1  → ACK:1
...
ROW 27 → ACK:27
```

After receiving all rows, the Pico performs inference.

---

# 10. Full-Precision vs INT8 Comparison

The models are compared using:

* Classification accuracy
* Model size
* Inference latency
* Memory consumption

| Metric             | FP32 | INT8 |
| ------------------ | ---: | ---: |
| Accuracy           |    — |    — |
| Model size         |    — |    — |
| Inference latency  |    — |    — |
| Memory consumption |    — |    — |

The final values are obtained experimentally and reported in the results section.

---

# 11. Real-World Webcam Testing

Ten real-world digits are tested using the webcam:

```text
0, 1, 2, 3, 4, 5, 6, 7, 8, 9
```

| Test | Actual | Predicted | Correct? | Latency |
| ---: | -----: | --------: | :------: | ------: |
|    1 |      0 |           |          |         |
|    2 |      1 |           |          |         |
|    3 |      2 |           |          |         |
|    4 |      3 |           |          |         |
|    5 |      4 |           |          |         |
|    6 |      5 |           |          |         |
|    7 |      6 |           |          |         |
|    8 |      7 |           |          |         |
|    9 |      8 |           |          |         |
|   10 |      9 |           |          |         |

### Accuracy

```text
Accuracy = (Correct predictions / 10) × 100
```

---

# 12. Example Result

A successful webcam test produced:

```text
Predicted digit : 3
Pico latency    : 30179 µs
                  30.18 ms
```

The displayed digit was correctly classified as **3**.
