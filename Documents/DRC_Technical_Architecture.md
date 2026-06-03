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

### 2.3 Feature Extraction: Sliding Window & Polynomial Fitting
- **Status:** **NOT IMPLEMENTED**.
- **Implementation Strategy:**
    1. **Histogram Base:** Calculate a column-wise histogram of the bottom half of the binary Bird's Eye View (BEV) image to identify the starting $x$-coordinates for the left (yellow) and right (blue) lines.
    2. **Iterative Search:** Use 9-12 sliding windows per line to track the path from bottom to top.
        - **Recenter:** If a window contains more than 50 pixels, the next window is centered on their mean $x$ position.
    3. **Polynomial Fit:** Fit a 2nd-order polynomial ($x = Ay^2 + By + C$) to the pixels identified in the windows. This allows the system to model both straight lines and complex curves.

---

## 3. Autonomous Navigation & Path Planning (Status)

### 3.1 Curve Estimation & Radius of Curvature
- **Status:** **NOT IMPLEMENTED**.
- **Methodology:** Use the coefficients from the 2nd-order polynomial fit to calculate the radius of curvature ($R_{curve}$) at the bottom of the image (closest to the droid).
- **Formula:** $R_{curve} = \frac{[1 + (2Ay + B)^2]^{1.5}}{|2A|}$
- **Speed Control:** The $R_{curve}$ value informs the "Throttle Manager." Large radii (straights) allow for max PWM, while small radii (sharp turns) trigger a reduction in speed to maintain traction.

### 3.2 Centerline & Error Calculation ($e$)
- **Status:** **NOT IMPLEMENTED**.
- **Details:** The target path is the midpoint between the left and right polynomials. 
- **Cross Track Error (CTE):** Measured as the horizontal offset between the droid's center and the calculated centerline.
- **Anticipatory Steering:** Evaluate the error at a "look-ahead" distance (e.g., 50 pixels up the frame) to prepare for upcoming turns.

### 3.3 PID Controller
- **Status:** **NOT IMPLEMENTED**.
- **Details:** A standard Proportional-Integral-Derivative controller will translate the CTE into a steering angle.
- **Tuning:** $K_p$ for responsiveness, $K_d$ to dampen oscillations, and $K_i$ to correct for mechanical bias in the steering rack.

---

## 4. Obstacle & Entity Recognition (Status)
- **Status:** **PARTIALLY IMPLEMENTED (Filters Only)**.
- **Details:** HSV filters for Purple (Obstacles) and Red (Rival Bots) exist.
- **Next Steps:** Implement contour area filtering to ignore noise and "Virtual Bumper" logic that triggers an emergency stop or bypass maneuver.

---

## 5. Wireless State & Motor Interface (Status)
- **Status:** **NOT IMPLEMENTED**.
- **Details:** Serial communication (UART) between the Python environment and the motor controller (Teensy/Arduino).
- **Watchdog:** Implement a heartbeat signal to stop the droid if the Python process hangs.

---

## 6. Optimization & Performance

### 6.1 Bottleneck Analysis
- **Resolution:** Processing at **320x240** is the "sweet spot" for balancing detail and latency.
- **Numba JIT:** Use the `@jit` decorator on the pixel-traversal loops in the sliding window function for a 10-20x speedup.
- **Zero-Copy Frames:** Minimize `cv2.copy()` operations; use slice views where possible.

### 6.2 Latency Reduction
- **Asynchronous I/O:** The `VisionInput` thread must remain isolated. 
- **Frame Skipping:** If the Control thread falls behind, it should discard the current frame and wait for the next `_frame_no` to ensure "Freshness."

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
