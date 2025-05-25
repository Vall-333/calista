import time
import os
import subprocess

class Timer:
    def __init__(self):
        self.old_time = 0
        self.minutes_passed = 0
        self.current_timer_duration = 0
        self.current_cycles = 0
        self.current_break_duration = 0
        self.timer_running = False
        self.timer_paused = False
        self.timer_on_break = False
        self.file_name = ".config/calista/calista_log.txt"

        os.makedirs(os.path.dirname(self.file_name), exist_ok=True)

    def pause_timer(self):
        """Pause the timer and save current progress"""
        self.timer_paused = True
        if(self.timer_running):

            try:
                with open(self.file_name, "w") as file:
                    file.write(str(self.minutes_passed))
                self.timer_running = False
                print("timer paused")
                self.send_notification("Timer Paused")
            except IOError as e:
                print(f"Error saving timer state: {e}")

        else:
            print("No timer is running")
            return

    def resume_timer(self):
        """Resume the timer from saved state"""
        try:
            with open(self.file_name, 'r') as file:
                self.minutes_passed = int(file.read().strip())
            self.timer_paused = False
            self.timer_running = True
            self.old_time = time.time()  # Reset the time reference
            print("timer Started")
            self.send_notification("Timer Started")
            return True
        except (IOError, ValueError) as e:
            print(f"Error loading timer state: {e}")
            return False

    def start_timer(self, timer_duration,rest_duration , cycles):
        """Start or resume the timer"""
        try:
            self.current_timer_duration = int(timer_duration)
            self.current_break_duration = int(rest_duration)
            self.current_cycles = int(cycles)
        except ValueError:
            print("Error: Values must numbers")
            return

        if any(x < 1 for x in [self.current_timer_duration, self.current_break_duration,]):
            print("Work Time and Break Time should be one minute or more")
            self.reset_timer()
            return

        if self.current_cycles < 0:
            print("Values must be positive")
            return

        print("Timer Started")
        self.send_notification("Timer Started")
        self.timer_running = True
        self.old_time = time.time()  # Initialize time reference

        #Starts timer
        if self.current_cycles <= 1:
            self.simple_timer()

        else:
            self.default_timer()



    def default_timer(self):
        loops = self.current_cycles

        while loops != 0:
              while self.minutes_passed < self.current_timer_duration:
                  if self.timer_paused:
                      time.sleep(1)
                      continue

                  if time.time() - self.old_time >= 60:
                      self.minutes_passed += 1
                      time_left = self.current_timer_duration - self.minutes_passed
                      print(f"Work time left: {time_left} minutes")
                      self.old_time = time.time()
                      time.sleep(0.1)

              print("Work session is done!! Take a break")
              self.send_notification("Work session is done!! Take a break")
              self.minutes_passed = 0
              self.timer_on_break = True
              self.old_time = time.time()

              while self.minutes_passed < self.current_break_duration:
                  if self.timer_paused:
                      time.sleep(1)
                      continue

                  if time.time() - self.old_time >= 60:
                      self.minutes_passed += 1
                      time_left = self.current_break_duration - self.minutes_passed
                      print(f"Break time left: {time_left} minutes")
                      self.old_time = time.time()
                      time.sleep(0.1)



              self.send_notification("Break session is done!! back to work")
              print("Break session is done!! back to work")
              self.minutes_passed = 0
              self.old_time = time.time()
              self.timer_on_break = False
              loops -= 1

        print("Timer Completed!")
        self.send_notification("Timer Complete")
        self.reset_timer()


    def simple_timer(self):
        while self.minutes_passed < self.current_timer_duration:
            if self.timer_paused:
                time.sleep(1)
                continue

            # Checks if a minute has passed
            if time.time() - self.old_time >= 60:
                self.minutes_passed += 1
                time_left = self.current_timer_duration - self.minutes_passed
                print(f"Time left: {time_left} minutes")
                self.old_time = time.time()  # Reset the timer

                time.sleep(0.1)


        print("Work session is done!! Take a break")
        self.send_notification("Work session is done!! Take a break")
        self.minutes_passed = 0
        self.timer_on_break = True
        self.old_time = time.time()

        while self.minutes_passed < self.current_break_duration:
            if self.timer_paused:
                time.sleep(1)
                continue

            if time.time() - self.old_time >= 60:
                self.minutes_passed += 1
                time_left = self.current_break_duration - self.minutes_passed
                print(f"Break time left: {time_left} minutes")
                self.old_time = time.time()
                time.sleep(0.1)

        self.send_notification("Timer Complete")
        print("Timer Complete")
        self.reset_timer()

    def timer_status(self):
        if self.timer_running  and self.timer_on_break:
            print(f"Break, minutes left: {self.current_break_duration - self.minutes_passed} ")
        elif self.timer_running:
            print(f"Work, minutes left: {self.current_timer_duration - self.minutes_passed} ")
        elif self.timer_paused:
            print("timer is currently paused")
        else:
            print("no timer is running")


    def send_notification(self, message):
        subprocess.run(['notify-send', "Calista", message])



    def reset_timer(self):
        """Reset timer state after completion"""
        self.minutes_passed = 0
        self.old_time = 0
        self.timer_paused = False
        self.timer_running = False
        self.timer_on_break = False
        self.current_timer_duration = 0
        self.current_cycles = 0
        self.current_break_duration = 0
        try:
            os.remove(self.file_name)
        except OSError:
            pass
