# Technical Architecture: 2025 QUT Droid Racing Challenge (DRC)
## Autonomous Navigation via Computer Vision and Python

This document outlines the high-level software architecture and technical implementation details for an autonomous racing droid designed to compete in the 2025 QUT Droid Racing Challenge. The system is built using **Python 3.10+** and **OpenCV 4.x**, prioritizing low-latency processing and robust feature extraction in non-ideal indoor environments.

---

## 1. System Architecture Overview

The software stack follows a modular, asynchronous design to ensure that the Computer Vision (CV) pipeline does not block the Motor Control Interface.

### 1.1 Concurrency Model
- **CV Thread:** Captures frames from the CSI/USB camera, performs preprocessing, feature extraction, and path calculation.
- **Control Thread:** Executes the PID control loop and sends PWM signals to the motor drivers at a fixed frequency (e.g., 50Hz).
- **Communication Thread:** Listens for wireless interrupts (Start/Stop/Finish) via a 2.4GHz/LoRa/WiFi handheld remote.

### 1.2 Global State Machine
The robot operates in four primary states:
1. `IDLE`: Waiting for wireless start signal.
2. `RACING`: Active CV pipeline and motor actuation.
3. `TURNING_CHALLENGE`: Specialized state for fork detection and arrow interpretation.
4. `FINISHED`: Autonomous stop at the green line, disabling motors.

---

## 2. Computer Vision Pipeline

The CV Engine is the "retina" of the droid. It must distinguish between the track boundaries, obstacles, and environmental noise.

### 2.1 Color Space Optimization
While RGB is intuitive, the **HSV (Hue, Saturation, Value)** color space is used for robustness against varying indoor lighting conditions at QUT Gardens Point.

| Target Feature | Color | Recommended HSV Range (Approx.) |
| :--- | :--- | :--- |
| Left Boundary | Yellow | `[20, 100, 100]` to `[30, 255, 255]` |
| Right Boundary | Blue | `[100, 150, 50]` to `[140, 255, 255]` |
| Markers/Finish | Green | `[40, 70, 70]` to `[80, 255, 255]` |
| Obstacles | Purple | `[130, 50, 50]` to `[160, 255, 255]` |

### 2.2 Image Preprocessing & Bird's Eye View (BEV)
To calculate real-world trajectories, the perspective distortion from the camera's mounting angle must be removed.

1. **Gaussian Blur:** `cv2.GaussianBlur(frame, (5, 5), 0)` to reduce high-frequency noise.
2. **Perspective Transform:** A 4-point ROI (Region of Interest) is mapped to a top-down rectangle using `cv2.getPerspectiveTransform` and `cv2.warpPerspective`. This allows for distance calculations in pixels-to-centimeters.

### 2.3 Feature Extraction: Sliding Window Algorithm
For line following, we implement a sliding window search to detect the curvature of the yellow and blue tapes.

```python
def find_lane_pixels(binary_warped):
    # 1. Take a histogram of the bottom half of the image
    histogram = np.sum(binary_warped[binary_warped.shape[0]//2:, :], axis=0)
    # 2. Find the peak of the left and right halves of the histogram
    midpoint = int(histogram.shape[0]//2)
    leftx_base = np.argmax(histogram[:midpoint])
    rightx_base = np.argmax(histogram[midpoint:]) + midpoint
    
    # 3. Step through windows to track the line upward
    # ... (iterative window shifts based on mean pixel density)
```

---

## 3. Autonomous Navigation & Path Planning

### 3.1 Trajectory Calculation
The "optimal path" is defined as the centerline between the detected yellow and blue boundaries. 
- **Centerline:** $C(y) = \frac{L(y) + R(y)}{2}$
- **Error Term ($e$):** The horizontal offset between the droid's current position and the calculated centerline at a "look-ahead" distance.

### 3.2 Control Theory: PID Implementation
A Proportional-Integral-Derivative controller manages the steering angle.

$$u(t) = K_p e(t) + K_i \int e(t) dt + K_d \frac{de(t)}{dt}$$

- **Proportional ($K_p$):** Reacts to the current error. High $K_p$ causes oscillation.
- **Derivative ($K_d$):** Counteracts the $K_p$ momentum to prevent overshoot. Crucial for the 1-2m track width.
- **Integral ($K_i$):** Corrects steady-state error (e.g., if one motor is slightly weaker than the other).

### 3.3 Turning Challenge Logic
Upon detecting the fork (Figure 3 in Rules), the droid must:
1. Identify the **Black Arrow Sign** (28x20cm).
2. Use **Template Matching** or a **Linear SVM** classifier to determine direction (Left vs. Right).
3. Override the default line-following logic to ignore the "wrong" boundary until the fork is cleared.

---

## 4. Obstacle & Entity Recognition

### 4.1 Purple Obstacle Avoidance (Opens Category)
Obstacles (max 400x400x500mm) are detected via color masking and contour analysis.
- **Contour Filtering:** `cv2.findContours` followed by `cv2.contourArea` to ignore small noise.
- **Bounding Box:** `cv2.boundingRect(c)` provides the obstacle's width and height in the BEV.
- **Vector Field Histogram (VFH):** If an obstacle is detected in the centerline, the path planner generates a temporary "virtual boundary" to push the droid toward the available space.

### 4.2 Dynamic Droid Detection
Since other droids are predominantly **Red** (80% coverage rule), a red color mask is used to detect competitors.
- **Safety Margin:** If a red cluster is within $X$ cm of the droid's nose, the throttle is modulated to avoid a +20s collision penalty.

---

## 5. Wireless State & Motor Interface

### 5.1 Communication Protocol
The handheld remote sends a single-byte command via a serial bridge (e.g., `PySerial` over RF):
- `0x01`: START (Transition IDLE -> RACING)
- `0x02`: STOP (Emergency kill-switch)
- `0x03`: FINISH (Force FINISHED state)

### 5.2 Traction & Surface Handling
The Turning Challenge sign is a <5mm raised area. To prevent wheel spin or loss of control:
- **IMU Integration:** A 6-axis IMU (MPU6050) detects sudden pitch/roll changes.
- **Adaptive Throttle:** Reduce torque momentarily when the IMU detects a vertical jolt, ensuring wheels remain "on the ground at all times" (Rule 5.9).

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
