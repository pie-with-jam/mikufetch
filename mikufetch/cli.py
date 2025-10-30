# mikufetch/cli.py
"""CLI module for Mikufetch. Handles argument parsing and output rendering."""

from argparse import ArgumentParser
import json
import os
import sys
from shutil import get_terminal_size
from typing import List, Tuple

from .info import get_sys_info
from .art import MIKU_ART

# ANSI colors (used only for the info text, not for the art itself)
PINK = "\033[38;5;213m"
BLUE = "\033[38;5;39m"
CYAN = "\033[38;5;87m"
GREEN = "\033[38;5;84m"
YELLOW = "\033[38;5;228m"
RESET = "\033[0m"


def _enable_windows_ansi():
    """
    Enable ANSI escape code support on Windows terminals.

    Windows consoles do not support ANSI colors by default.
    This attempts to enable it. If it fails, colors will fall back
    to raw escape sequences.
    """
    if os.name != "nt":
        return
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        h = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
        mode = ctypes.c_uint()
        if kernel32.GetConsoleMode(h, ctypes.byref(mode)):
            ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            new_mode = mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING
            kernel32.SetConsoleMode(h, new_mode)
    except Exception:
        return


def parse_args():
    """
    Parse CLI arguments for Mikufetch.

    Returns:
        argparse.Namespace: Parsed command-line options.
    """
    parser = ArgumentParser(description="Cute cross-platform system info fetch with Miku ASCII art")
    parser.add_argument("--no-art", action="store_true", help="Do not display ASCII art")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI colors")
    parser.add_argument("--json", action="store_true", help="Output system info as JSON only")
    return parser.parse_args()


def _prepare_info_lines(info: List[Tuple[str, str]]) -> List[str]:
    """
    Convert list of (key, value) pairs to formatted strings.

    Args:
        info (list): System info pairs.

    Returns:
        list[str]: Lines formatted as "Key: Value".
    """
    return [f"{k}: {v}" for k, v in info]


def display_info(info, no_art: bool = False, no_color: bool = False, json_out: bool = False):
    """
    Display system info either with ASCII art or in plain text/JSON.

    Args:
        info (list[tuple]): System information key-value pairs.
        no_art (bool): If True, hide ASCII art.
        no_color (bool): If True, disable ANSI color output.
        json_out (bool): If True, output only JSON.

    Behavior:
        - JSON mode prints only JSON.
        - TTY-aware color output.
        - Aligns Miku ASCII art with system info table.
    """
    if json_out:
        data = {k: v for k, v in info}
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    _enable_windows_ansi()

    colors = {
        "OS": BLUE,
        "Host": BLUE,
        "Kernel": BLUE,
        "Uptime": BLUE,
        "Packages": GREEN,
        "Shell": GREEN,
        "Resolution": GREEN,
        "CPU": CYAN,
        "GPU": CYAN,
        "Memory": YELLOW,
    }

    reset = RESET
    if no_color or not sys.stdout.isatty():
        for k in colors:
            colors[k] = ""
        reset = ""

    if no_art:
        for key, value in info:
            print(f"{colors.get(key,'')}{key}:{reset} {value}")
        return

    art_lines = MIKU_ART.splitlines()
    info_lines = [f"{colors.get(k,'')}{k}:{reset} {v}" for k, v in info]

    # side-by-side ASCII + info
    max_art_width = max(len(line) for line in art_lines)
    padding = 3
    art_height = len(art_lines)
    info_height = len(info_lines)
    start_index = (art_height - info_height) // 2 if art_height > info_height else 0

    for i in range(art_height):
        art_line = art_lines[i]
        if start_index <= i < start_index + info_height:
            info_line = info_lines[i - start_index]
        else:
            info_line = ""
        print(f"{PINK}{art_line.ljust(max_art_width)}{reset}{' ' * padding}{info_line}")


def main() -> int:
    """
    Entry point for CLI execution.

    Returns:
        int: Exit status code (0 = success).
    """
    args = parse_args()
    info = get_sys_info()
    display_info(info, no_art=args.no_art, no_color=args.no_color, json_out=args.json)
    return 0
