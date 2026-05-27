# Codebase Inefficiencies and Optimizations

This document outlines identified inefficiencies in the DRC-Team-1 vision system and provides recommendations for improvement.

## 1. Repeated Attribute Creation in Loops (Numpy Arrays)
- **Issue:** In `HSVFilterInterface.py`, `Get_Min_Vals_Arr()` and `Get_Max_Vals_Arr()` (in subclasses like `ObstacleHSVFilter`) create new `numpy` arrays on every call.
- **Impact:** High-frequency memory allocation and garbage collection.
- **Fix:** Store the numpy arrays as class attributes (`self.min_vals_arr`, `self.max_vals_arr`) and only update them when the HSV values change (e.g., in `Update_HSV_Filter_From_GUI`).

## 2. Full-Frame Processing (Missing Region of Interest)
- **Issue:** `cv2.inRange` and `cv2.findContours` process the entire `hsvFrame`, including pixels that likely represent the ceiling or spectators.
- **Impact:** Wasted CPU cycles processing irrelevant background data.
- **Fix:** Crop the `hsvFrame` to a specific Region of Interest (ROI), such as the bottom 60% of the screen, before running `inRange`.

## 3. Configuration Inconsistency (HSV Space)
- **Issue:** In `Vision/config.py`, a comment suggests using `cv2.COLOR_BGR2HSV` to save power, but the code actually uses `cv2.COLOR_BGR2HSV_FULL`.
- **Impact:** While the performance difference may be minor, it indicates a mismatch between documented intent and implementation. `COLOR_BGR2HSV` maps Hue to 0-179, while `FULL` maps it to 0-255.
- **Fix:** Align the code with the desired performance/accuracy trade-off and update the comment or code accordingly.

## 4. Blocking Configuration GUI
- **Issue:** The `Save_HSV_Filter` method in `HSVFilterInterface.py` contains a `while True` loop that blocks the main vision pipeline until the 's' key is pressed.
- **Impact:** This prevents the robot from performing any other tasks (like driving or obstacle detection) while a filter is being adjusted.
- **Fix:** Implement the HSV adjustment GUI as a non-blocking process or a separate mode that doesn't halt the main loop, allowing for real-time adjustments while the system is running (if safe).

## 5. Inefficient Singleton Initialization
- **Issue:** `VisionInput` uses a `__new__` method to enforce a singleton, but it imports `config` and `cv2` inside the `__new__` method every time it is checked (even if the instance exists).
- **Impact:** While Python caches imports, this is an unconventional and slightly slower pattern than importing at the top of the file. More importantly, it hides dependencies.
- **Fix:** Move imports to the top of the file.

## 6. Risky Pickle Usage
- **Issue:** HSV filters are saved and loaded using `pickle`.
- **Impact:** Pickle is not secure against erroneous or maliciously constructed data. Furthermore, it is version-dependent; if you change the class structure of a filter, old `.pkl` files will fail to load or cause attribute errors.
- **Fix:** Use a more robust and human-readable format like JSON or YAML for storing HSV parameters.

## 7. Lack of Perspective Correction
- **Issue:** Centroids (`cx`, `cy`) are calculated in camera/screen space.
- **Impact:** Distances and angles will be distorted. A line curve on the left side of the screen won't have the same coordinate scale as a line directly in front.
- **Fix:** Implement the `cv2.getPerspectiveTransform` and `cv2.warpPerspective` as planned in the technical architecture to translate to a Bird's Eye View.
