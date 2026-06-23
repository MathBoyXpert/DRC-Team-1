import numpy as np
import time
import sys
from typing import Dict

sys.path.insert(1, "/home/fast/DRC-Team-1/Vision/") # for the pi
sys.path.insert(1, "C:/Users/anshg/Downloads/University/DRC/DRC-Team-1/Vision/") # for local dev

sys.path.insert(1, "/home/fast/DRC-Team-1/Vision/Utils/") # for the pi
sys.path.insert(1, "C:/Users/anshg/Downloads/University/DRC/DRC-Team-1/Vision/Utils/") # for local dev
import config
from HSVFilters.HSVFilterInterface import HSVFilterInterface

# Mocking config/dependencies for presentation. 
# In production, import from Vision.Utils.config and Control.ControlThread.
class VisionControlBridge:
    def __init__(self, robot_controller):
        self.robot = robot_controller
        self.width = config.WIDTH
        self.height = config.HEIGHT 
        self.target_center = self.width // 2
        
        # Lane fallback offset (half of typical track width in pixels)
        # this is for when only one lane is detected!
        self.lane_offset = 180 
        
        # states and counters for the bot
        self.state = config.RACING # IDLE, RACING, FINISHED
        self.current_lap = 0
        self.total_laps = config.LAP_TOTAL
        self.finish_line_cooldown = time.time()
        
        # arrow challenge state
        self.arrow_override_start = 0
        self.active_direction = "None"
        
    # looks at the filters reciveved from the vision pipeline and then performs the logic
    def process_and_act(self, HSVManager: Dict[str, HSVFilterInterface], arrow_direction, arrow_confidence):
        # base case where the bot has finished driving and is done
        if self.state == "FINISHED":
            self.robot.stop()
            return
            
        # Initialise all of the filters
        yellow_line_filter = HSVManager[config.YELLOW_TRACK_LINES_HSV]
        blue_line_filter = HSVManager[config.BLUE_TRACK_LINES_HSV]
        obstacle_filter = HSVManager[config.OBSTACLE_HSV]
        rival_filter = HSVManager[config.RIVAL_BOT_HSV]
        track_completion_filter = HSVManager[config.TRACK_COMPLETION_HSV]
        
        # ################# TRACK COMPLETION TRACKING #################
        # # count the number of times youve seen the green the green line as you go around the track
        # if track_completion_filter.contour_status:
        #     # avoids double counting a single track completion line with a cooldown
        #     if time.time() - self.finish_line_cooldown > config.TRACK_COMPLETION_LINE_COOLDOWN:
        #         self.current_lap += 1
        #         self.finish_line_cooldown = time.time()
        #         print(f"Lap {self.current_lap}/{self.total_laps} completed!")
                
        #         if self.current_lap >= self.total_laps:
        #             print("Finished the final lap. Stopping for -5s bonus")
        #             self.state = config.FINISHED
        #             self.robot.stop()
        #             return
        
        # ################# ARROW DETECTION TRACKING #################
        # # this tracks the arrow HSV filter for a potential turning challenge
        # if arrow_direction in ["Left", "Right"] and arrow_confidence > config.ARROW_CONFIDENCE:
        #     self.active_direction = arrow_direction
        #     self.arrow_override_start = time.time()

        # # checks if the arrow overide should take place right now
        # in_arrow_zone = (time.time() - self.arrow_override_start < config.ARROW_OVER_RIDE_DURATION)
        
        ################# TRACK LINES TRACKING #################
        # gets the positions of the track lines
        # Yellow line position
        if (yellow_line_filter.contour_status):
            cx_yellow = yellow_line_filter.cx 
        else: 
            cx_yellow = None

        # Blue line position
        if (blue_line_filter.contour_status):
            cx_blue = blue_line_filter.cx 
        else:
            cx_blue = None
        
        # Calculating the center position that should be used for pid
        calculated_center = None
        ################################################################################################################################################################################################################
        in_arrow_zone = False #################################################### remove ########################################################################################################
        if in_arrow_zone:
            # follow only the inner boundary of the fork to stay on path
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
                
        # # 5. Obstacle Avoidance Overlay (Purple Hurdles)
        # obstacle_avoidance_bias = 0
        # if obstacle_filter and obstacle_filter.cx is not None and obstacle_filter.cy is not None:
        #     # Only trigger if the obstacle is in the bottom 60% of the frame (close)
        #     if obstacle_filter.cy > (self.height * 0.4):
        #         # Calculate how close the obstacle is
        #         proximity_scale = (obstacle_filter.cy - (self.height * 0.4)) / (self.height * 0.6)
                
        #         # If obstacle is on the left side, bias target centerline to the right
        #         if obstacle_filter.cx < self.target_center:
        #             obstacle_avoidance_bias = int(80 * proximity_scale) # steer right
        #         else:
        #             obstacle_avoidance_bias = -int(80 * proximity_scale) # steer left
                    
        #         # Emergency Stop if obstacle is critically close
        #         if obstacle_filter.cy > (self.height * 0.85):
        #             print("Emergency Stop: Purple obstacle detected within virtual bumper!")
        #             self.robot.drive(0)
        #             return
        
        # 6. Throttle Management (Base Speed & Speed Dampener)
        base_speed = 0.5 # Default speed
        
        # # Reduce speed if a rival bot (Red) is ahead
        # if rival_filter and rival_filter.cx is not None and rival_filter.cy is not None:
        #     # Proximity calculation based on how low (close) the robot centroid is
        #     if rival_filter.cy > (self.height * 0.3):
        #         proximity_factor = (rival_filter.cy - (self.height * 0.3)) / (self.height * 0.7)
        #         # Dampen throttle up to 70% reduction
        #         base_speed *= (1.0 - (proximity_factor * 0.7))
        
        #########################################################################################################################################################################################
        obstacle_avoidance_bias = 0 ########################################## remove ###############################################################################################################
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
