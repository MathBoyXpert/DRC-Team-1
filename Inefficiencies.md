# Codebase Inefficiencies and Optimizations

This document outlines identified inefficiencies in the DRC-Team-1 vision system and provides recommendations for improvement.
<div style="text-decoration: line-through;">

## 1. Redundant Frame Capture
- **Issue:** The `VisionInput().Get_Frame()` method is called multiple times within a single iteration of the `mainLoop`. It is called once in `vision.mainLoop` and then again inside each HSV filter's `Display_Masked_Frame` method.
- **Impact:** Each call to `Get_Frame()` triggers a new `cv2.VideoCapture.read()` operation. This means different filters are potentially processing different frames, and valuable CPU/IO time is wasted on redundant captures.
- **Fix:** Capture the frame once at the beginning of the `mainLoop` in `computerVisionPreProcessing.py` and pass that single frame to the filters.

## 2. Redundant HSV Conversions
- **Issue:** Every HSV filter calls `cv2.cvtColor(frame, config.HSV_SPACE)` independently.
- **Impact:** Converting a high-resolution frame from BGR to HSV is a computationally expensive operation. Performing this 4+ times per frame significantly reduces the FPS (frames per second).
- **Fix:** Perform the HSV conversion once per loop iteration and pass the `hsv_frame` to all filters that require it.

## 3. Configuration Inconsistency (HSV Space)
- **Issue:** In `Vision/config.py`, a comment suggests using `cv2.COLOR_BGR2HSV` to save power, but the code actually uses `cv2.COLOR_BGR2HSV_FULL`.
- **Impact:** While the performance difference may be minor, it indicates a mismatch between documented intent and implementation. `COLOR_BGR2HSV` maps Hue to 0-179, while `FULL` maps it to 0-255.
- **Fix:** Align the code with the desired performance/accuracy trade-off and update the comment or code accordingly.

## 4. Blocking Configuration GUI
- **Issue:** The `Save_HSV_Filter` method in `HSVFilterInterface.py` contains a `while True` loop that blocks the entire vision pipeline until the 's' key is pressed.
- **Impact:** This prevents the robot from performing any other tasks (like driving or obstacle detection) while a filter is being adjusted.
- **Fix:** Implement the HSV adjustment GUI as a non-blocking process or a separate mode that doesn't halt the main loop, allowing for real-time adjustments while the system is running (if safe).
</div>

## 5. Serial Processing and Lack of Concurrency
- **Issue:** Filters and frame capture are processed sequentially in a single loop. The `DRC_Technical_Architecture.md` specifies a modular, asynchronous design with separate CV, Control, and Communication threads, but this is not yet reflected in the code.
- **Impact:** As more filters and control logic are added, the time taken for one loop iteration grows linearly, potentially dropping the frame rate below acceptable levels for real-time control.
- **Fix:** Implement the multi-threaded architecture described in the technical documentation. Use a dedicated thread for frame capture and pre-processing, and another for the control loop.

## 6. Lack of Pre-processing (Noise Reduction & Perspective)
- **Issue:** The code currently applies HSV filters directly to the raw frame without noise reduction (e.g., Gaussian Blur) or perspective correction (Bird's Eye View).
- **Impact:** Raw frames can be noisy, leading to "salt and pepper" noise in the masks. Lack of perspective correction makes it difficult to calculate accurate trajectories or distances.
- **Fix:** 
  - Add `cv2.GaussianBlur` before HSV filtering.
  - Implement the `cv2.getPerspectiveTransform` and `cv2.warpPerspective` as planned in the technical architecture.

## 7. Missing Feature Extraction Algorithms
- **Issue:** The architecture mentions a "Sliding Window Algorithm" for lane detection and "Template Matching/SVM" for arrow detection, but these are currently missing.
- **Impact:** The system only generates masks but doesn't yet derive control signals (steering/throttle) from them.
- **Fix:** Implement the sliding window pixel search and path planning logic described in the architecture document.

---

# Optimizing Multiple HSV Filters

Running multiple HSV filters can be significantly more efficient by following these strategies:

### 1. Centralized Pre-processing (The "Capture Once, Process Many" Pattern)
Instead of each filter fetching and converting its own data, the pipeline should follow this structure:
1. **Fetch:** `frame = camera.read()` (Once per loop)
2. **Pre-process:**
   - `blurred = cv2.GaussianBlur(frame, (5, 5), 0)`
   - `hsv_frame = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)`
3. **Distribute:** 
   - `mask1 = filter1.apply(hsv_frame)`
   - `mask2 = filter2.apply(hsv_frame)`
   - ...

### 2. Reuse Shared Masks
If multiple filters target similar color ranges (e.g., different shades of blue), create a base mask once and refine it using bitwise operations rather than re-running `cv2.inRange` with overlapping values.

### 3. Downscaling for Masking
Masking doesn't always require full resolution. You can:
1. Downscale the HSV frame (e.g., to 320x240).
2. Generate the mask on the smaller frame.
3. This significantly reduces the number of pixels `cv2.inRange` has to process (4x reduction if halving both dimensions).

### 4. Region of Interest (ROI)
If a filter only needs to look at a specific part of the screen (e.g., the bottom half for track lines), only pass that slice of the `hsv_frame` to the filter.
```python
# Look only at the bottom 60% of the frame as suggested in architecture
height, width = hsv_frame.shape[:2]
roi = hsv_frame[int(height*0.4):, :] 
mask = cv2.inRange(roi, min_vals, max_vals)
```

### 5. Hardware Acceleration
Use OpenCV's `cv2.UMat` for transparent API usage of OpenCL (GPU) if available on the deployment hardware (e.g., Jetson Nano).
