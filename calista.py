import click
import threading
from Timer import Timer

@click.command()
def timer():
    """Start the timer"""
    exit_flag = False
    timer = Timer()  # Create one timer instance

    while not exit_flag:
        command = input("Enter Command: ")

        if command == "start":
            minutes = input("Minutes: ")
            # Pass the function as target, don't call it here
            timer_thread = threading.Thread(target=timer.start_timer, args=(minutes,), daemon=True)
            timer_thread.start()
        elif command == "pause":
            timer.pause_timer()
        elif command == "resume":
            timer.resume_timer()
        elif command == "exit":
            exit_flag = True

if __name__ == '__main__':
    timer()
