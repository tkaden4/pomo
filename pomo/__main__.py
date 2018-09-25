import click
import colorama
from colorama import Fore, Cursor
from termcolor import colored
from rx import Observable
from rx.concurrency import TimeoutScheduler
import cursor
from itertools import count
from datetime import datetime, timedelta

from .util import *

MESSAGE = """ _ __    ___   _ __ ___    ___  
| '_ \  / _ \ | '_ ` _ \  / _ \ 
| |_) || (_) || | | | | || (_) |
| .__/  \___/ |_| |_| |_| \___/ 
|_|                             
"""

# Colorama must be initialized
colorama.init()


def format_progress(now, diff, total):
    return " ".join(
        [
            "Elapsed:",
            colored(format_time(now), "green"),
            "| Remaining:",
            colored(format_time(diff), "green"),
            "| Total:",
            colored(format_time(total), "green"),
        ]
    )


def print_progress(now, diff, total):
    print(
        colorama.ansi.clear_line(),
        format_progress(now, diff, total),
        "\r",
        end="",
        sep="",
    )


def print_stats(long, short, work, rollover):
    print(
        "Long: {} | Short: {} | Work: {} | Rollover: {}".format(
            *[green(x) for x in [long, short, work, rollover]]
        )
    )


# TODO Create Pomo Observable
# def pomo(scheduler=None):
#     scheduler = scheduler if scheduler is not None else TimeoutScheduler()
#
#     def second_timer(scheduler):
#         return Observable.timer(datetime.now(), 1000, scheduler=scheduler)
#
#     timer = second_timer(scheduler)


def run_timer(length):
    # Start timer
    timer = Observable.timer(datetime.now(), 1000).take(length.seconds + 1)
    with cursor.HiddenCursor():
        for x in timer.to_blocking():
            now = seconds(x)
            diff = length - now
            print_progress(now, diff, length)


# TODO refactor
def run(long_rest, short_rest, work_period, rollover):
    print_stats(long_rest, short_rest, work_period, rollover)
    try:
        # Session Loop
        while True:
            do_start = prompt_yes_no("Ready to start session?")
            if not do_start:
                # leave the session loop
                break

            # Rollover Loop
            for x in range(rollover):
                run_timer(work_period)
                print()
                # Check if we are at rollover point
                if x + 1 < rollover:
                    # We only need to start a short rest if it's before the rollover point
                    start_short_rest = prompt_yes_no("Start short rest?")
                    if start_short_rest:
                        run_timer(short_rest)
                        print()
                    # Check if we need to move on to next pomodoro
                    start_next = prompt_yes_no("Start next pomodoro?")
                    if not start_next:
                        # If we don't want to start another pomodoro,
                        # then we assume they want to be done completely
                        # TODO refactor
                        return

            # Handle end-of-session
            start_next_session = prompt_yes_no("Do you want to start another session?")
            if not start_next_session:
                # break out of outer loop
                break

            # Handle long break
            start_long_break = prompt_yes_no("Do you want a long break?")
            if start_long_break:
                run_timer(long_rest)
                print()
    except KeyboardInterrupt:
        print()
    finally:
        print(yellow("Done"))


@click.command()
@click.option("--long", type=int, default=25, help="Length of long rest (in minutes)")
@click.option("--short", type=int, default=5, help="Length of short rest (in minutes)")
@click.option(
    "--length",
    type=int,
    default=25,
    help="Length of a work period / pomodoro (in minutes)",
)
@click.option(
    "--rollover",
    type=int,
    default=5,
    help="Number of pomodoros before taking a long rest",
)
def cli(long, short, length, rollover):
    print(colorama.ansi.clear_screen(), end="")
    print(colored(MESSAGE, "red"))
    run(
        long_rest=minutes(long),
        short_rest=minutes(short),
        work_period=minutes(length),
        rollover=5,
    )


if __name__ == "__main__":
    print(colored(MESSAGE, "red"))
    cli()
