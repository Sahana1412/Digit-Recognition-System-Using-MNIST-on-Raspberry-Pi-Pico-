# MNIST Digit Recognition – Edge AI Deployment

## 1. Requirements / Before Running

### Software

* Windows 10/11
* Python 3.11
* VS Code
* Wokwi VS Code extension
* Raspberry Pi Pico SDK
* ARM GCC toolchain
* CMake + Ninja

### Python packages

The virtual environment should contain:

```text
tensorflow
numpy
opencv-python
pyserial
```

If needed:

```powershell
.\venv\Scripts\python.exe -m pip install tensorflow numpy opencv-python pyserial
```

### Project requirements

Before running:

1. Ensure the project folder is present.
2. Ensure `venv` is available.
3. Ensure the trained/quantized model is available.
4. Ensure the Pico firmware has been built.
5. Ensure `wokwi.toml` contains:

```toml
rfc2217ServerPort = 4000
```

6. Start the **Wokwi Raspberry Pi Pico simulation** before running the webcam program.
7. Allow access to the laptop webcam.
8. Place a handwritten/displayed digit clearly inside the green box.

---

# 2. How to Run

Open PowerShell in:

```text
D:\AMRITA\SEMESTER 5\EOCandelectronics\Assignment\MNIST_PICO
```

Run:

```powershell
.\venv\Scripts\python.exe webcam_to_pico.py
```

Then:

* Place a digit inside the green box.
* Press **SPACE** to classify.
* Press **Q** to exit.

---

# 3. Project Overview

* Lightweight CNN trained on MNIST digits **0–9**.
* Model converted to TensorFlow Lite.
* Full INT8 quantization applied for edge deployment.
* Quantized model deployed on **Raspberry Pi Pico** using TensorFlow Lite Micro.
* Laptop webcam provides real-world input.
* OpenCV converts the image to **28×28 INT8** format.
* Pico performs local inference without cloud services.

---

# 4. System Pipeline

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
OpenCV
  ↓
28×28 INT8
  ↓
Serial Transfer
  ↓
Pico Inference
  ↓
Prediction
```

---

# 5. Model Architecture

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

# 6. Training Setup

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

# 7. Optimization and Quantization

The trained model is converted to TensorFlow Lite and optimized using **full integer INT8 post-training quantization**.

```text
Input type       : INT8
Input scale      : 0.0039215689
Input zero point : -128
Input shape      : 1 × 28 × 28 × 1
```

Quantization:

```text
q = round(x / scale) + zero_point
```

---

# 8. Webcam Preprocessing

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

---

# 9. Edge Deployment

The INT8 model is embedded into the Pico firmware and executed using **TensorFlow Lite Micro**.

The Pico:

1. Receives the image.
2. Loads it into the input tensor.
3. Runs inference.
4. Determines the predicted digit.
5. Measures inference latency.
6. Sends the result to the laptop.

---

# 10. Communication

```text
Laptop → PING
Pico   → READY
```

The image is transferred as:

```text
28 rows × 28 INT8 values
```

Each row is acknowledged before the next row is sent.

---

# 11. Full-Precision vs INT8 Comparison

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

---

