# Technical Architecture: 2025 QUT Droid Racing Challenge (DRC)
## Autonomous Navigation via Computer Vision and Python

This document outlines the high-level software architecture and technical implementation details for an autonomous racing droid designed to compete in the 2025 QUT Droid Racing Challenge. The system is built using **Python 3.10+** and **OpenCV 4.x**, prioritizing low-latency processing and robust feature extraction in non-ideal indoor environments.

---
## 1. System Architecture Overview (Status)

### 1.1 Concurrency Model
- **Status:** **PARTIALLY IMPLEMENTED**.
- **Current implementation:** The vision pipeline uses `threading` in `VisionInput.py` for background frame ingestion and HSV conversion (`Frame_Ingestion` method). However, the Control and Communication threads are not yet implemented.
- **Recommendation:** Implement the remaining threads to decouple the PID motor control from the main vision loop.

### 1.2 Global State Machine
- **Status:** **NOT IMPLEMENTED**.
- **Current implementation:** The system currently only has a basic "Racing" loop with an "Edit HSV" mode interrupt.
- **Recommendation:** Implement a proper state machine class to handle `IDLE`, `RACING`, and `FINISHED` states.

---

## 2. Computer Vision Pipeline (Status)

### 2.1 Color Space Optimization
- **Status:** **IMPLEMENTED**.
- **Details:** HSV filtering is implemented via an interface (`HSVFilterInterface`). HSV conversion happens centrally in the `VisionInput` thread to save CPU cycles.
- **Correction:** The code currently uses `cv2.COLOR_BGR2HSV_FULL` instead of the standard `cv2.COLOR_BGR2HSV`.

### 2.2 Image Preprocessing & Bird's Eye View (BEV)
- **Status:** **NOT IMPLEMENTED**.
- **Details:** Frames are processed raw before HSV conversion. Gaussian Blur and Perspective Transforms (BEV) are missing.

### 2.3 Feature Extraction: Sliding Window Algorithm
- **Status:** **NOT IMPLEMENTED**.
- **Details:** The code produces masks but does not yet extract lane lines or centerline coordinates.

---

## 3. Autonomous Navigation & Path Planning (Status)
- **Status:** **NOT IMPLEMENTED**.
- **Details:** No PID controller or trajectory calculation logic exists in the codebase yet.

---

## 4. Obstacle & Entity Recognition (Status)
- **Status:** **PARTIALLY IMPLEMENTED (Filters Only)**.
- **Details:** HSV filters for Purple (Obstacles) and Red (Rival Bots) exist, but no contour analysis or bounding box logic is implemented.

---

## 5. Wireless State & Motor Interface (Status)
- **Status:** **NOT IMPLEMENTED**.
- **Details:** No serial communication or motor driver code is present.

---

## 6. Optimization & Performance

### 6.1 Bottleneck Analysis
- **Resolution:** Processing at **320x240** or **640x480** is sufficient for line detection and maintains >30 FPS on a Raspberry Pi 4 or Jetson Nano.
- **Numba JIT:** Use the `@jit` decorator on the sliding window functions to compile Python to machine code for a 10x speedup in pixel traversal.
- **ROI Cropping:** Only process the bottom 60% of the frame for line following to ignore spectators and ceiling lights.

---

## 7. Compliance & Scoring Strategy

| Objective | Technical Approach |
| :--- | :--- |
| **Avoid Penalties** | High-frequency PID ($K_d$ tuning) to keep wheels away from tape (+2s penalty). |
| **Autonomous Stop** | Green mask at start/finish line + Lap Counter logic (-5s bonus). |
| **Turning Challenge** | Robust arrow detection (Template Matching) for correct fork selection (-5s bonus). |
| **Budget Management** | Use consumer-grade webcams and hobbyist motor drivers to stay under $1500 AUD limit. |

---
*Created for the DRC 2025 Development Team.*
