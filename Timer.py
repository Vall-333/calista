import time
import os

class Timer:
    def __init__(self):
        self.old_time = 0
        self.minutes_passed = 0
        self.current_timer_length = 0
        self.current_cycles = 0
        self.current_rest_lenght = 0
        self.timer_paused = False
        self.file_name = ".config/calista/calista_log.txt"
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.file_name), exist_ok=True)

    def pause_timer(self):
        """Pause the timer and save current progress"""
        self.timer_paused = True
        try:
            with open(self.file_name, "w") as file:
                file.write(str(self.minutes_passed))
        except IOError as e:
            print(f"Error saving timer state: {e}")

    def resume_timer(self):
        """Resume the timer from saved state"""
        try:
            with open(self.file_name, 'r') as file:
                self.minutes_passed = int(file.read().strip())
            self.timer_paused = False
            self.old_time = time.time()  # Reset the time reference
            return True
        except (IOError, ValueError) as e:
            print(f"Error loading timer state: {e}")
            return False

    def start_timer(self, timer_length,rest_length = 0 , cycles = 0):
        """Start or resume the timer"""
        try:
            self.current_timer_length = int(timer_length)
        except ValueError:
            print("Error: Timer length must be a number")
            return

        try:
            self.current_sets = int(rest_length)
        except ValueError:
            print("Error: The length of the rests  must be a number")
            return

        try:
            self.current_sets = int(cycles)
        except ValueError:
            print("Error: The number of cycles must be a number")
            return

        print("Timer Started")
        self.old_time = time.time()  # Initialize time reference

        #Starts timer
        self.default_timer(cycles)


    def default_timer(self, repetitions = 0 ):

        while self.minutes_passed < self.current_timer_length:
            if self.timer_paused:
                time.sleep(1)
                continue

            # Checks if a minute has passed
            if time.time() - self.old_time >= 60:
                self.minutes_passed += 1
                time_left = self.current_timer_length - self.minutes_passed
                print(f"Time left: {time_left} minutes")
                self.old_time = time.time()  # Reset the timer

            time.sleep(0.1)

        print("Timer Completed!")
        self._reset_timer()



    def _reset_timer(self):
        """Reset timer state after completion"""
        self.minutes_passed = 0
        self.old_time = 0
        self.timer_paused = False
        try:
            os.remove(self.file_name)
        except OSError:
            pass
