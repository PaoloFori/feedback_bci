#!/usr/bin/env python3
import rospy
import csv
import datetime
import os
from rosneuro_msgs.msg import NeuroEvent
from pynput import keyboard

class ReactionTimeLogger:
    def __init__(self):
        rospy.init_node('reaction_logger', anonymous=True)

        self.EVENT_OFFSET_OFF = 32768 
        self.BOOM_START_CODES = [897, 898, 899]
        self.BOOM_END_CODES = [code + self.EVENT_OFFSET_OFF for code in self.BOOM_START_CODES]
        self.trial = 0

        # --- SETUP CSV ---
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = f"reaction_time_{timestamp_str}.csv"
        default_path = os.path.expanduser("~")
        self.base_path = rospy.get_param('~filepath', default_path)
        self.filepath = os.path.join(self.base_path, self.filename)
        
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

        # header
        with open(self.filepath, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["trial", "Reaction_Time_Sec"])

        rospy.loginfo(f"Reaction Logger started. File: {self.filepath}")

        # --- VARIABLES ---
        self.is_boom_active = False
        self.boom_start_time = None
        self.current_boom_code = None
        self.reaction_recorded = False

        # --- SUB ---
        self.sub_bus = rospy.Subscriber('/events/bus', NeuroEvent, self.bus_callback)
        
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

    def bus_callback(self, msg):
        event_code = msg.event 
        
        if event_code in self.BOOM_START_CODES:
            if self.is_boom_active and not self.reaction_recorded:
                self.log_to_csv(0.0) 

            self.is_boom_active = True
            self.reaction_recorded = False
            self.current_boom_code = event_code
            self.boom_start_time = rospy.Time.now()
            self.trial += 1

        elif event_code in self.BOOM_END_CODES:
            base_code = event_code - self.EVENT_OFFSET_OFF
            
            if self.is_boom_active and base_code == self.current_boom_code:
                if not self.reaction_recorded:
                    duration = (rospy.Time.now() - self.boom_start_time).to_sec()
                    self.log_to_csv(self.trial, duration)
                
                self.is_boom_active = False
                self.boom_start_time = None
                self.current_boom_code = None

    def on_key_press(self, key):
        try:
            if key == keyboard.Key.space:
                if self.is_boom_active and not self.reaction_recorded:
                    rt = (rospy.Time.now() - self.boom_start_time).to_sec()
                    
                    self.log_to_csv(self.trial, rt)
                    self.reaction_recorded = True 
        except AttributeError:
            pass

    def log_to_csv(self, trial, rt_value):
        try:
            with open(self.filepath, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([trial, f"{rt_value:.6f}"])
        except Exception as e:
            rospy.logerr(f"Errore scrittura CSV: {e}")

if __name__ == '__main__':
    try:
        ReactionTimeLogger()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass