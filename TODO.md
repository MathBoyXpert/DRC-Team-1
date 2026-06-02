# DRC Project TODO List

This list is prioritized based on the dependency chain required to get the droid racing.

## Phase 1: Immediate Structural & Performance Fixes
- [x] **Refactor Vision Pipeline:** 
    - [x] Capture frame once in `Frame_Ingestion` thread.
    - [x] Convert to HSV once and pass to filters.
    - [x] Implement frame caching and frame number synchronization.
    - [x] Calculate object Centroids (moments).
- [ ] **Optimize HSV Filters:**
    - [ ] Add Gaussian Blur for noise reduction before HSV conversion.
    - [ ] Implement ROI (Region of Interest) to only process the bottom 60% of the screen.
    - [ ] Cache `numpy` min/max arrays instead of creating them in every loop.
- [ ] **Replace Pickle:** Switch to JSON for saving HSV filter settings to prevent versioning issues.

## Phase 2: Core Vision Algorithms (The "Brain")
- [ ] **Implement Perspective Transform:** Create the Bird's Eye View (BEV) mapping.
- [ ] **Lane Detection:** Implement the Sliding Window algorithm to find yellow and blue line coordinates in the BEV.
- [ ] **Path Planning:** Calculate the centerline and the steering error ($e$).

## Phase 3: Control & Hardware Integration
- [ ] **PID Controller:** Implement the PID class to convert error into steering angles.
- [ ] **Motor Interface:** Create the bridge between Python and the hardware (e.g., PCA9685 or direct GPIO PWM).
- [ ] **Threading:** Complete the Control thread to run the motor loop at a consistent frequency (Vision thread is already done).

## Phase 4: Advanced Features & Rules Compliance
- [ ] **Obstacle Avoidance:** Implement "virtual boundaries" for purple obstacles based on centroids.
- [ ] **Rival Bot Detection:** Add safety logic to slow down when red objects are detected.
- [ ] **Turning Challenge:** Implement arrow sign detection (CNN-based) for fork selection.
- [ ] **Finish Line Logic:** Add Green color detection to trigger the `FINISHED` state.

## Phase 5: Testing & Tuning
- [ ] **Field Testing:** Calibrate HSV filters under actual track lighting.
- [ ] **PID Tuning:** Optimize $K_p$, $K_i$, and $K_d$ on the real track.
- [ ] **Wireless Remote:** Integrate the wireless start/stop interrupt signals.
