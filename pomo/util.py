from datetime import timedelta


def to_min_sec(td):
    return (int(td.seconds / 60), int(td.seconds % 60))


def format_time(time):
    return "{0:0>2}:{1:0>2}".format(*to_min_sec(time))


def seconds(seconds):
    return timedelta(seconds=seconds)


def minutes(minutes):
    return timedelta(minutes=minutes)


def prompt_yes_no(prompt):
    answer = input("{} (y/n): ".format(prompt)).strip()
    return answer == "y"


from termcolor import colored
import colorama


def color_impl(color):
    def impl(str):
        return colored(str, color)

    return impl


yellow = color_impl("yellow")
red = color_impl("red")
green = color_impl("green")


from num2words import num2words as num_to_words
from functools import partial

num_to_ordinal = partial(num_to_words, to="ordinal")
