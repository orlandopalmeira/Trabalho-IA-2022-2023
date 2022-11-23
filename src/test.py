from Node import Node
from Race import RaceP


red = "\033[1;49;31m"
green = "\033[1;49;32m"
yellow = "\033[1;49;33m"
blue = "\033[1;49;36m"
white = "\033[1;49;36m"
endc = '\033[0m'


def colorize(string, color):
    color_dict = {
        "red": "\033[1;91m",
        "green": "\033[1;92m",
        "yellow": "\033[1;93m",
        "purple": "\033[1;95m",
        "blue": "\033[1;96m",
        "white": "\033[1;97m",
    }
    endc = '\033[0m'
    color = color.lower()
    code = color_dict.get(color)
    if code is None:
        code = color_dict.get("white")
    res = code + string + endc
    return res


example_ansi = colorize("Ola", "green") + colorize("Azul", "blue")
print(example_ansi)
