import click
import threading
from .Timer import Timer

@click.command()
def timer():
    """Commands:

       start: begins the timer

       pause: stops the timer

       resume: starts the timer again

       status: shows whether the timer is in work mode or break mode and how many minutes are left

       exit: closes the application
    """
    exit_flag = False
    timer = Timer()

    while not exit_flag:
        command = input("Enter Command: ")

        if command == "start":
            minutes = input("Work Duration: ")
            rest_duration = input("Break Duration: ")
            cycles = input("Number of Cycles: ")
            timer_thread = threading.Thread(target=timer.start_timer, args=(minutes,rest_duration, cycles)
            , daemon=True)
            timer_thread.start()
        elif command == "pause":
            timer.pause_timer()
        elif command == "resume":
            timer.resume_timer()
        elif command == "status":
            timer.timer_status()
        elif command == "exit":
            exit_flag = True


if __name__ == '__main__':
    timer()
