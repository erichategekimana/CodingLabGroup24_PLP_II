# effects.py
import sys
import time
import itertools
from colorama import Fore, Style, init
init(autoreset=True)

# Initialize colorama
init(autoreset=True)

def type_print(text, delay=0.03, color="default"):
    """Print text one character at a time, like typewriter."""
    color_codes = {
        "default": "",
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE,
    }

    color_code = color_codes.get(color.lower(), "")
    for char in text:
        sys.stdout.write(f"{color_code}{char}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def styled_input(prompt, color="cyan", delay=0.02, symbol=">> "):
    """Displays a styled input prompt using type_print, then collects input."""
    type_print(prompt, delay=delay,  color=color)
    return input(symbol).strip()

def loading_spinner(task="Loading", duration=2):
    """Shows a spinning animation for a duration with a task label."""
    spinner = itertools.cycle(["|", "/", "-", "\\"])
    end_time = time.time() + duration
    while time.time() < end_time:
        sys.stdout.write(f'\r{task}: {next(spinner)}')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * (len(task) + 5) + '\r')

def progress_dots(task="Processing", dots=3, delay=0.4):
    """Displays task followed by increasing dots."""
    for i in range(1, dots + 1):
        print(f"{task}{'.' * i}", end='\r')
        time.sleep(delay)
    print(" " * (len(task) + dots), end='\r') # Clear line

def delayed_response(text, wait=1.5, color=None):
    """Delays then followed by increasing"""
    time.sleep(wait)
    type_print(text, delay=0.02, color=color)

def print_colored(text, color="GREEN"):
    """Prints colored text instantly."""
    print(getattr(Fore, color.upper(), "") + text + Style.RESET_ALL)