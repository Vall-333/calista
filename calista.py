import click
from Timer import Timer


@click.group()
@click.pass_context
def cli(ctx):
    """Timer application"""
    ctx.obj = Timer()

@cli.command()
@click.argument('minutes')
@click.pass_context
def start(ctx, minutes):
    """Start the timer"""
    timer = ctx.obj
    timer.start_timer(minutes)

@cli.command()
@click.pass_context
def pause(ctx):
    """Pause the timer"""
    timer = ctx.obj
    timer.pause_timer()
    click.echo("Timer paused")

@cli.command()
@click.pass_context
def resume(ctx):
    """Resume the timer"""
    timer = ctx.obj
    if timer.resume_timer():
        click.echo("Timer resumed")
    else:
        click.echo("Couldn't resume - start a new timer with 'start'")

@cli.command()
@click.pass_context
def status(ctx):
    """Check timer status"""
    timer = ctx.obj
    click.echo(f"Time passed: {timer.minutes_passed} minutes")
    click.echo(f"Paused: {timer.timer_paused}")

if __name__ == '__main__':
    cli()
