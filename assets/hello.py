import sys
import time
import random

RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
WHITE  = "\033[97m"
DIM    = "\033[2m"

def move_up(n):    sys.stdout.write(f"\033[{n}A")
def move_down(n):  sys.stdout.write(f"\033[{n}B")
def col(n):        sys.stdout.write(f"\033[{n}G")
def clear_line():  sys.stdout.write("\033[2K")
def hide_cursor(): sys.stdout.write("\033[?25l")
def show_cursor(): sys.stdout.write("\033[?25h")
def flush():       sys.stdout.flush()

HI = [
    r" _   _ _   _   _                   _ ",
    r"| | | (_) | |_| |__   ___ _ __ ___| |",
    r"| |_| | | | __| '_ \ / _ \ '__/ _ \ |",
    r"|  _  | | | |_| | | |  __/ | |  __/_|",
    r"|_| |_|_|  \__|_| |_|\___|_|  \___(_)"
]

GEORGE = [
    r" ___ _              ____                           _ ",
    r"|_ _( )_ __ ___    / ___| ___  ___  _ __ __ _  ___| |",
    r" | ||/| '_ ` _ \  | |  _ / _ \/ _ \| '__/ _` |/ _ \ |",
    r" | |  | | | | | | | |_| |  __/ (_) | | | (_| |  __/_|",
    r"|___| |_| |_| |_|  \____|\___|\___/|_|  \__, |\___(_)",
    r"                                        |___/        "
]

SUBTITLE = "Software Developer  •  Open Source Enthusiast"
DIVIDER  = "─" * len(SUBTITLE)

SCRAMBLE = r"!@#$%^&*<>?|[]{}~ABCDEFabcdef0123456789"

def centre(line, width=80):
    pad = max(0, (width - len(line)) // 2)
    return " " * pad + line

def scramble_frame(lines, progress):
    out = []
    for line in lines:
        w   = len(line)
        locked = int(progress * w)
        row = []
        for i, ch in enumerate(line):
            if ch == " ":
                row.append(" ")
            elif i < locked:
                row.append(ch)
            else:
                row.append(random.choice(SCRAMBLE))
        out.append("".join(row))
    return out

def print_block(lines, colour="", width=80):
    for line in lines:
        sys.stdout.write(colour + centre(line, width) + RESET + "\n")

def overwrite_block(lines, colour, n_lines, width=80):
    move_up(n_lines)
    for line in lines:
        clear_line()
        sys.stdout.write(colour + BOLD + centre(line, width) + RESET + "\n")
    flush()

def scramble_reveal(lines, colour, fps=20, duration=1.4, width=80):
    n     = len(lines)
    steps = int(fps * duration)

    print_block(scramble_frame(lines, 0.0), colour + BOLD, width)
    flush()
    time.sleep(1 / fps)

    for step in range(1, steps + 1):
        progress = step / steps
        rendered = scramble_frame(lines, progress)
        overwrite_block(rendered, colour, n, width)
        time.sleep(1 / fps)

    overwrite_block(lines, colour, n, width)
    flush()


def typewriter(text, colour, x_pad=0, fps=22, width=80):
    pad = max(0, (width - len(text)) // 2)
    prefix = " " * pad

    for i in range(len(text) + 1):
        cursor = "█" if i < len(text) else " "
        clear_line()
        sys.stdout.write(
            "\r" + colour + BOLD + prefix + text[:i] + cursor + RESET
        )
        flush()
        time.sleep(1 / fps)
    sys.stdout.write("\n")
    flush()

def main():
    width = 80
    hide_cursor()
    try:
        sys.stdout.write("\n")

        scramble_reveal(HI, CYAN, duration=1, width=width)
        time.sleep(0.2)

        scramble_reveal(GEORGE, GREEN, duration=1, width=width)
        time.sleep(0.2)

        pad = " " * max(0, (width - len(DIVIDER)) // 2)
        sys.stdout.write(DIM + pad + DIVIDER + RESET + "\n")
        flush()

        typewriter(SUBTITLE, YELLOW, width=width)

        sys.stdout.write("\n")
        flush()

    finally:
        show_cursor()

if __name__ == "__main__":
    main()