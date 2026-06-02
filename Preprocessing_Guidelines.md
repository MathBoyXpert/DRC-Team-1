# Frame Preprocessing Recommendations for Computer Vision

To improve the robustness and accuracy of your vision system (especially for track following and arrow detection), applying preprocessing to each frame before HSV filtering or CNN inference is highly recommended.

## 1. Gaussian Blur (Noise Reduction)
**Why:** Reduces high-frequency noise and small artifacts that can cause "jittery" masks in HSV filtering.
- **Recommended Values:** Kernel size `(5, 5)` or `(7, 7)`.
- **Snippet:**
```python
import cv2

# Apply Gaussian Blur to smooth out noise
blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
```

## 2. CLAHE (Contrast Limited Adaptive Histogram Equalization)
**Why:** Improves contrast in local regions. This is vital for outdoor or variable lighting conditions where shadows might hide track lines.
- **Recommended Values:** `clipLimit=2.0`, `tileGridSize=(8, 8)`.
- **Snippet:**
```python
# Convert to Lab color space to apply CLAHE on the Lightness channel
lab = cv2.cvtColor(frame, cv2.COLOR_BGR2Lab)
l, a, b = cv2.split(lab)

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
cl = clahe.apply(l)

# Merge back and convert to BGR
limg = cv2.merge((cl, a, b))
enhanced_frame = cv2.cvtColor(limg, cv2.COLOR_Lab2BGR)
```

## 3. Resizing (Downscaling)
**Why:** Processing 1080p or 4K frames is CPU intensive and unnecessary for track detection. Downscaling to a lower resolution (e.g., 640x480 or 480x320) significantly increases your FPS.
- **Recommended Values:** Width `640` or `480`.
- **Snippet:**
```python
# Resize to 640x480 for faster processing
width = 640
height = 480
resized_frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
```

## 4. Region of Interest (ROI) Cropping
**Why:** The top half of the camera frame often contains the horizon, ceiling, or background objects that are irrelevant to the track and may cause false positives.
- **Recommended Values:** Keep the bottom 50% to 70% of the frame.
- **Snippet:**
```python
height, width = frame.shape[:2]
# Define the ROI (e.g., only the bottom 60% of the image)
roi_start_row = int(height * 0.4)
roi_frame = frame[roi_start_row:height, 0:width]
```

## 5. Bilateral Filtering (Edge-Preserving Smooth)
**Why:** Similar to Gaussian blur but keeps edges sharp. Excellent for preserving the crisp lines of the track while smoothing the textures within the lines.
- **Recommended Values:** `d=9`, `sigmaColor=75`, `sigmaSpace=75`.
- **Snippet:**
```python
# d: Diameter of each pixel neighborhood
# sigmaColor: Filter sigma in the color space
# sigmaSpace: Filter sigma in the coordinate space
smoothed_frame = cv2.bilateralFilter(frame, 9, 75, 75)
```

## 6. Morphological Operations (Opening/Closing)
**Why:** Applied to the **mask** (after HSV filtering) to remove small noise (Opening) or fill small holes in detected objects (Closing).
- **Recommended Values:** `(5, 5)` or `(3, 3)` kernel.
- **Snippet:**
```python
kernel = np.ones((5, 5), np.uint8)

# Opening: Remove small noise from the background
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# Closing: Fill small holes within the detected object
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
```

## 7. Gamma Correction (Brightness Adjustment)
**Why:** If the camera feed is too dark or too washed out, gamma correction can adjust the brightness non-linearly.
- **Recommended Values:** `gamma=1.2` (to brighten) or `gamma=0.8` (to darken).
- **Snippet:**
```python
def adjust_gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

brightened_frame = adjust_gamma(frame, gamma=1.2)
```

## Summary Recommendation Table

| Technique | Order | Recommended Value | Impact |
| :--- | :--- | :--- | :--- |
| **ROI Cropping** | 1st | Bottom 60% | Massive performance boost & noise reduction. |
| **CLAHE** | 2nd | `clipLimit=2.0` | Stabilizes detection in different lighting. |
| **Gaussian Blur** | 3rd | `(5, 5)` | Smoother masks, less jitter. |
| **Morphological Ops** | 4th (on mask) | `(5, 5)` Kernel | Clean, solid detection blobs. |
