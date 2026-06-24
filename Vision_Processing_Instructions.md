# Guide: Handling Processed Vision Inputs for the 2025 QUT DRC

This guide outlines how to handle your processed vision inputs (contours, centroids, bounding boxes, and classified classes) to control your Ackermann steering droid according to the **2025 QUT Droid Racing Challenge (DRC)** rulebook.

---

## 1. Summary of Rules & Decision-Making Logic

The tournament rules dictate several high-stakes actions based on color-coded tape and visual cues:

| Visual Target | Raw Vision Output | Rule / Penalty / Bonus | Control Action Required |
| :--- | :--- | :--- | :--- |
| **Yellow Tape** | Left boundary contour/centroid | Track boundary crossing incurs a **2s, 5s, or 10s penalty**. | Guide the droid to keep yellow tape on the left. |
| **Blue Tape** | Right boundary contour/centroid | Track boundary crossing incurs a **2s, 5s, or 10s penalty**. | Guide the droid to keep blue tape on the right. |
| **Green Tape** | Start/Finish line contour/area | Stopping nose on finish line at race end yields a **5s bonus**. | Stop the robot autonomously once the finish line is reached after the final lap. |
| **Black Arrow Sign** | Contour bounding box + CNN/Template Match | Correct fork turn yields a **5s bonus**. Wrong turn = **5s penalty**. No turn = **10s penalty**. | Temporarily bias steering toward the classified direction (Left/Right). |
| **Purple Obstacle** | Obstacle contour/centroid/bounding box | Collision damage, course deviation. | Steer away from the obstacle centroid or trigger emergency braking if too close. |
| **Red Rival Bot** | Rival droid contour/centroid | Collision/Sportsmanship. | Reduce throttle (speed dampening) to prevent collision. |

---

## 2. Step-by-Step Vision Input Processing

### 2.1. Centerline & Error Calculation (Yellow/Blue Lanes)
To steer effectively, calculate a target **Centerline ($x_{center}$)** and compute the **Cross-Track Error (CTE)**.
* **Both Lines Detected:**
  $$x_{center} = \frac{cx_{yellow} + cx_{blue}}{2}$$
* **Single-Line Fallback:** If one line is obscured (e.g., on tight bends):
  * *Only Yellow (Left):* $x_{center} = cx_{yellow} + \text{offset}$
  * *Only Blue (Right):* $x_{center} = cx_{blue} - \text{offset}$
* **Cross-Track Error ($e$):**
  $$e = x_{target} - x_{center} \quad (\text{where } x_{target} = \text{width} / 2)$$

### 2.2. Turn Challenge Fork Bias (Black Arrow)
When the CNN/Template Matching detects an arrow direction (`"Left"` or `"Right"`):
1. Enter the turning zone state.
2. If `"Left"`, ignore the right (blue) line and use a left-biased single-line tracking behavior (or hard-offset the centerline to the left).
3. If `"Right"`, ignore the yellow line and track blue, biasing the centerline to the right.

### 2.3. Obstacle Avoidance (Purple Objects)
Create a **Virtual Bumper Zone** in the bottom-middle region of the camera frame.
* If a purple centroid falls inside this zone, calculate a steering offset away from the obstacle's horizontal position ($cx_{obstacle}$).
* If the obstacle is too close (very large contour area or high $cy$), reduce speed or stop.

### 2.4. Rival Avoidance (Red Bots)
If a red robot is detected directly in front:
* Dynamically scale down the throttle speed:
  $$\text{Throttle} = \text{Base Speed} \times (1.0 - \text{proximity\_factor})$$

### 2.5. Finish Line Stop (Green Tape)
When green tape is detected:
* If the droid is in the `RACING` state and the lap count equals the target laps, transition to `FINISHED`, apply motor braking, and center steering to secure the **5-second bonus**.

---

## 3. PID Controller Utilization (Steering Control)

The steering angle of the front wheels is continuously controlled by a Proportional-Integral-Derivative (PID) loop. The PID controller takes the **Cross-Track Error (CTE)** and outputs a correction value to center the droid on the track.

### 3.1. Mathematical Formula & Code Execution
In your codebase, the PID loop in [ControlThread.py](file:///C:/Users/anshg/Downloads/University/DRC/DRC-Team-1/Control/ControlThread.py#L10) calculates steering adjustments as follows:

$$\text{Output} = (K_p \times e) + (K_i \times \int e \, dt) + \left(K_d \times \frac{de}{dt}\right)$$

* **Proportional ($K_p$):** Corrects the immediate track error. If the error is large, the steer angle is proportional. Too high causes oscillation (weaving).
* **Integral ($K_i$):** Corrects for systemic mechanical bias (e.g. alignment drift). Too high causes sluggish wind-up and overshoot.
* **Derivative ($K_d$):** Opposes rapid change in error, damping oscillations and smoothing straight-away transitions.

### 3.2. Integration Example: Linking Vision Output to the PID Loop
When a frame is processed:
1. Calculate `target_x` (the desired track midpoint offset by any arrow or obstacle avoidance biases).
2. Call `set_steering(target_x)` on your [AckermannRobot](file:///C:/Users/anshg/Downloads/University/DRC/DRC-Team-1/Control/ControlThread.py#L36) instance:

```python
# Centering error is measured against the PID setpoint (usually frame width // 2)
# The PID update method receives the calculated target_x
correction = self.pid.update(target_x)

# Map the raw PID correction value to the servo control range [-1.0 (Left), 1.0 (Right)]
servo_value = config.STEERING_CENTER + (correction / (config.WIDTH / 2))

# Constrain the servo steering angle to safe mechanical limits to prevent binding
servo_value = max(config.STEERING_MAX_LEFT, min(config.STEERING_MAX_RIGHT, servo_value))
self.steering_servo.value = servo_value
```

---

## 4. Implementation Code Example

Here is a comprehensive integration script showing how to take processed filters from `computerVisionPreProcessing.py` and compute motor signals for `ControlThread.py`.

```python
import numpy as np
import time

# Mocking config/dependencies for presentation. 
# In production, import from Vision.Utils.config and Control.ControlThread.
class VisionControlBridge:
    def __init__(self, robot_controller, width=640, height=480):
        self.robot = robot_controller
        self.width = width
        self.height = height
        self.target_center = width // 2
        
        # Lane fallback offset (half of typical track width in pixels)
        self.lane_offset = 180 
        
        # State Machine
        self.state = "RACING" # IDLE, RACING, FINISHED
        self.current_lap = 0
        self.total_laps = 3
        self.finish_line_cooldown = time.time()
        
        # Turning challenge state
        self.arrow_override_start = 0
        self.active_direction = "None"
        
    def process_and_act(self, filters, arrow_direction, arrow_confidence):
        """
        Receives the filter dictionary from the vision pipeline and commands the motors.
        """
        if self.state == "FINISHED":
            self.robot.stop()
            return
            
        # 1. Extract Filter Centroids & Contours
        yellow_line = filters.get("Yellow Track Lines")
        blue_line = filters.get("Blue Track Lines")
        obstacle = filters.get("Obstacle")
        rival = filters.get("Rival Bot")
        finish_line = filters.get("Track Completion")
        
        # 2. Check Finish Line (Green Tape)
        if finish_line and finish_line.cx is not None:
            # Cooldown avoids double-counting a single crossing
            if time.time() - self.finish_line_cooldown > 10.0:
                self.current_lap += 1
                self.finish_line_cooldown = time.time()
                print(f"Lap {self.current_lap}/{self.total_laps} completed!")
                
                if self.current_lap >= self.total_laps:
                    print("Start/Finish line reached on final lap. Stopping for -5s bonus.")
                    self.state = "FINISHED"
                    self.robot.stop()
                    return
        
        # 3. Handle Arrow Turn Challenge Override
        if arrow_direction in ["Left", "Right"] and arrow_confidence > 0.8:
            self.active_direction = arrow_direction
            self.arrow_override_start = time.time()
            
        # Active override expires after 3 seconds to resume normal track following
        in_arrow_zone = (time.time() - self.arrow_override_start < 3.0)
        
        # 4. Calculate Lane Centerline
        cx_yellow = yellow_line.cx if (yellow_line and yellow_line.cx is not None) else None
        cx_blue = blue_line.cx if (blue_line and blue_line.cx is not None) else None
        
        calculated_center = None
        
        if in_arrow_zone:
            # Fork logic: follow only the inner boundary of the fork to stay on path
            if self.active_direction == "Left":
                if cx_yellow is not None:
                    # Steer strictly matching the left line path with offset bias
                    calculated_center = cx_yellow + (self.lane_offset * 0.7)
                else:
                    # Hard-steer left if we lost track of the line
                    calculated_center = self.target_center - 100
            elif self.active_direction == "Right":
                if cx_blue is not None:
                    # Steer strictly matching the right line path with offset bias
                    calculated_center = cx_blue - (self.lane_offset * 0.7)
                else:
                    # Hard-steer right
                    calculated_center = self.target_center + 100
        else:
            # Standard line following
            if cx_yellow is not None and cx_blue is not None:
                # Both boundaries visible
                calculated_center = (cx_yellow + cx_blue) // 2
            elif cx_yellow is not None:
                # Left line only (bend to the right)
                calculated_center = cx_yellow + self.lane_offset
            elif cx_blue is not None:
                # Right line only (bend to the left)
                calculated_center = cx_blue - self.lane_offset
                
        # 5. Obstacle Avoidance Overlay (Purple Hurdles)
        obstacle_avoidance_bias = 0
        if obstacle and obstacle.cx is not None and obstacle.cy is not None:
            # Only trigger if the obstacle is in the bottom 60% of the frame (close)
            if obstacle.cy > (self.height * 0.4):
                # Calculate how close the obstacle is
                proximity_scale = (obstacle.cy - (self.height * 0.4)) / (self.height * 0.6)
                
                # If obstacle is on the left side, bias target centerline to the right
                if obstacle.cx < self.target_center:
                    obstacle_avoidance_bias = int(80 * proximity_scale) # steer right
                else:
                    obstacle_avoidance_bias = -int(80 * proximity_scale) # steer left
                    
                # Emergency Stop if obstacle is critically close
                if obstacle.cy > (self.height * 0.85):
                    print("Emergency Stop: Purple obstacle detected within virtual bumper!")
                    self.robot.drive(0)
                    return
        
        # 6. Throttle Management (Base Speed & Speed Dampener)
        base_speed = 0.5 # Default speed
        
        # Reduce speed if a rival bot (Red) is ahead
        if rival and rival.cx is not None and rival.cy is not None:
            # Proximity calculation based on how low (close) the robot centroid is
            if rival.cy > (self.height * 0.3):
                proximity_factor = (rival.cy - (self.height * 0.3)) / (self.height * 0.7)
                # Dampen throttle up to 70% reduction
                base_speed *= (1.0 - (proximity_factor * 0.7))
                
        # Adjust target centerline with obstacle avoidance bias
        if calculated_center is not None:
            target_x = calculated_center + obstacle_avoidance_bias
            # Steer using the Ackermann steering controller
            self.robot.set_steering(target_x)
            self.robot.drive(base_speed)
        else:
            # Lane lost fallback: slow down and maintain steering center
            self.robot.set_steering(self.target_center)
            self.robot.drive(base_speed * 0.5)
```

---

## 5. Key Performance Optimizations

To ensure your robot runs at low latency (targeting >60 FPS on Raspberry Pi):

1. **Implement a Decoupled Control Loop:** Running motor outputs synchronously in the main CV frame loop causes jitter. Spawn a separate `ControlThread` running at 100Hz that pulls the latest `cx` target and commands the actuators.
2. **Region of Interest (ROI) Cropping:** Update your `preprocessing` script to crop out the top 40% of the screen. Specators and lighting changes on the walls will otherwise cause false positives.
3. **JSON Config Migration:** Replace `pickle` in [HSVFilterInterface.py](file:///C:/Users/anshg/Downloads/University/DRC/DRC-Team-1/Vision/HSVFilters/HSVFilterInterface.py) with standard Python JSON structures to avoid class definition mismatch issues across development machines.
