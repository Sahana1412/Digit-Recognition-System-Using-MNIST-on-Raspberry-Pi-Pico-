# MNIST Digit Recognition – Edge AI Deployment

## 1. Project Overview

This project implements a lightweight **MNIST digit recognition system (0–9)** and deploys the optimized INT8 model on a **Raspberry Pi Pico** using **TensorFlow Lite Micro**.

A laptop webcam is used to capture a handwritten or displayed digit. The image is processed using OpenCV, converted to a 28×28 grayscale image, quantized to INT8, and transferred to the Raspberry Pi Pico. The Pico performs local neural-network inference and returns the predicted digit and inference latency.

The complete pipeline works locally without cloud-based inference.

---

## 2. System Pipeline

```text
MNIST Dataset
      ↓
CNN Model Training
      ↓
Floating-Point Model
      ↓
TensorFlow Lite Conversion
      ↓
INT8 Quantization
      ↓
Optimized INT8 Model
      ↓
Model converted to C/C++
      ↓
Raspberry Pi Pico + TensorFlow Lite Micro
      ↑
      │
Laptop Webcam
      ↓
OpenCV Preprocessing
      ↓
28 × 28 Image
      ↓
INT8 Quantization
      ↓
Serial Transfer
      ↓
Pico Inference
      ↓
Predicted Digit
```

---

## 3. Model Architecture

The project uses a lightweight Convolutional Neural Network:

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
Dense: 32 neurons, ReLU
        ↓
Dense: 10 neurons, Softmax
        ↓
Digit 0–9
```

The architecture was selected to keep the model lightweight enough for microcontroller deployment.

---

## 4. Training

The model is trained using the MNIST dataset.

### Training configuration

* Dataset: MNIST
* Training samples: 60,000
* Test samples: 10,000
* Image size: 28×28
* Number of classes: 10
* Optimizer: Adam
* Learning rate: 0.001
* Loss: Sparse Categorical Crossentropy
* Batch size: 128
* Epochs: 5

The input images are normalized before training.

---

## 5. Optimization and Quantization

The trained floating-point model is converted to TensorFlow Lite format.

Full integer **INT8 post-training quantization** is then applied using a representative dataset.

The deployed model uses:

```text
Input type       : INT8
Input scale      : 0.0039215689
Input zero point : -128
Input shape      : 1 × 28 × 28 × 1
```

Quantization reduces model storage and computational requirements, making the model suitable for deployment on the Raspberry Pi Pico.

The quantization relationship is:

```text
quantized_value =
    round(float_value / scale) + zero_point
```

## 6. Webcam Preprocessing

The webcam image is processed using OpenCV.

The preprocessing pipeline is:

```text
Webcam Frame
     ↓
Horizontal Flip
     ↓
Center Region of Interest
     ↓
Grayscale Conversion
     ↓
Thresholding
     ↓
Background Inversion
     ↓
Resize to 28×28
     ↓
INT8 Quantization
```

The processed image is designed to match the input format expected by the MNIST CNN.

---

## 7. Communication Between Laptop and Pico

A reliable row-based serial protocol is used.

The laptop first sends:

```text
PING
```

The Pico responds:

```text
READY
```

The 28×28 image is then transmitted as 28 separate rows.

```text
ROW 0  <28 INT8 values>
ACK:0

ROW 1  <28 INT8 values>
ACK:1

...

ROW 27 <28 INT8 values>
ACK:27
```

After receiving all rows, the Pico performs inference.

The Pico returns information such as:

```text
PREDICTION:3
LATENCY_US:30179
```

---

## 8. Edge Deployment

The quantized TensorFlow Lite model is converted into a C/C++ array and embedded into the Raspberry Pi Pico firmware.

The Pico uses **TensorFlow Lite Micro** to perform inference locally.

Required operators include:

* Conv2D
* MaxPool2D
* Shape
* StridedSlice
* Pack
* Reshape
* FullyConnected
* Softmax

The tensor arena used by the firmware is statically allocated.

---

## 9. Real-World Webcam Testing

The system is designed to test 10 real-world handwritten or displayed digits:

```text
0
1
2
3
4
5
6
7
8
9
```

For each digit, the webcam captures the input and the Raspberry Pi Pico performs the final prediction.

The results are recorded in the report using:

| Test | Actual | Predicted | Correct? | Pico Latency |
| ---: | -----: | --------: | :------: | -----------: |
|    1 |      0 |           |          |              |
|    2 |      1 |           |          |              |
|    3 |      2 |           |          |              |
|    4 |      3 |           |          |              |
|    5 |      4 |           |          |              |
|    6 |      5 |           |          |              |
|    7 |      6 |           |          |              |
|    8 |      7 |           |          |              |
|    9 |      8 |           |          |              |
|   10 |      9 |           |          |              |

Real-world webcam accuracy is calculated as:

```text
Accuracy = (Correct predictions / 10) × 100
```

---

## 10. Model Comparison

The full-precision and quantized models are compared using:

* Classification accuracy
* Model size
* Inference latency
* Memory consumption

The final values are reported in the project report based on the measured experimental results.

---

## 11. Example Edge Inference Result

A successful real-world webcam test produced:

```text
Predicted digit: 3
Pico latency   : 30179 us
                 30.18 ms
```

The displayed digit was correctly classified as `3`.

---

## 12. Technologies Used

* Python
* TensorFlow / Keras
* TensorFlow Lite
* TensorFlow Lite Micro
* OpenCV
* NumPy
* PySerial
* Raspberry Pi Pico / RP2040
* Raspberry Pi Pico SDK
* C/C++
* Wokwi

## 13. Conclusion

```text
Training → Optimization → Quantization → Deployment
       → Webcam Capture → Preprocessing
       → INT8 Transfer → Pico Inference → Prediction
```

No cloud inference is required for the final prediction.
