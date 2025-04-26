import click
import time

@click.command()
@click.argument('timer_length')
def start_time(timer_length):
    """Starts Timer"""

    if(timer_length.isnumeric()):
       message = ("Timer Started")
       click.echo(message)
       old_time = time.time()
       minutes_passed = 0
       while minutes_passed < int(timer_length):
        # Checks if a minute have passed
            if time.time() - old_time >= 60:
                       minutes_passed += 1
                       time_left = int(timer_length) - minutes_passed
                       click.echo(f"Time left: {time_left} minutes")
                       old_time = time.time()  # Reset the timer
            time.sleep(1)  # Sleep briefly to avoid busy waiting


if __name__ == '__main__':
    start_time()
