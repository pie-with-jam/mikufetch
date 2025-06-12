#!/usr/bin/env python3
import platform
import subprocess
from shutil import get_terminal_size

PINK = "\033[38;5;213m"
BLUE = "\033[38;5;39m"
RESET = "\033[0m"

MIKU_ART = r"""
⠄⠄⠄⠄⠄⠄⣀⣀⠄⠄⠄⠄⣀⣀⣀⣀⣀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄
⠄⠄⠄⣠⣤⠞⡋⠉⠧⠶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⢀⠏⠲⣄⠄⠄⠄
⠄⢀⡴⠋⢁⢐⣵⣶⣿⠟⣛⣿⣿⣿⠿⢿⣿⣦⣝⡻⣿⢇⡟⠄⣠⣿⣿⣷⣦
⠄⠸⢳⡜⢱⣿⣿⠛⡅⣿⣿⣿⡟⣱⣿⣦⡙⣿⣿⣿⡆⡜⠄⣀⢹⣿⣿⣿⣿
⠄⢰⣧⢱⣿⣿⢃⠾⣃⢿⣿⣿⢰⣿⣿⣿⠳⠘⣿⣿⣦⡙⢤⡻⠸⡿⠿⣿⣿
⠄⣿⡟⣼⣿⡏⣴⣿⣿⡜⣿⣿⢸⣿⣿⣿⣿⣷⠸⣿⣿⣿⢲⣙⢦⠄⠄⣼⣿
⢸⣿⡇⣿⣿⡇⣿⡏⠈⣷⣜⢿⢸⣿⣿⡟⠈⣿⣆⢹⣿⣿⠄⠙⣷⠄⠄⣿⣿
⣾⣿⡇⣿⣿⠃⣿⡇⠰⣿⣿⣶⣸⣿⣿⣇⠰⣿⣿⡆⣿⡟⠄⠄⡏⠄⢸⣿⣿
⠟⣵⣦⢹⣿⢸⣿⣿⣶⣿⣿⣥⣿⣿⣿⣿⣶⣿⣿⡇⣿⡇⣀⣤⠃⠄⡀⠟⠋
⡘⣿⡰⠊⠇⢾⣿⣿⣿⣿⣟⠻⣿⡿⣻⣿⣿⣿⣿⢃⡿⢰⡿⠋⠄⠄⠄⠄⣠
⣿⣌⠵⠋⠈⠈⠻⢿⣿⣿⣿⣿⣶⣾⣿⣿⣿⣿⡇⠸⣑⡥⢂⣼⡷⠂⠄⢸⣿
⣿⣿⡀⠄⠄⠄⠄⠄⢌⣙⡛⢛⠛⣛⠛⣛⢋⣥⡂⢴⡿⣱⣿⠟⠄⠄⠄⠘⣿
⣿⣿⣿⣷⣦⣄⣀⣀⡼⡿⣷⡜⡗⠴⠸⠟⣼⡿⣴⡓⢎⣛⠁⠄⠄⠄⠄⠄⢿
⣿⣿⣿⣿⣿⣿⠄⠙⠻⢧⣿⣿⡜⣼⢸⣎⣭⣹⢸⡿⣣⠞⢷⡀⠄⠄⠄⠄⢸
⣿⣿⣿⣿⣿⣿⠄⠄⠄⠄⣿⣿⡇⣿⢸⣿⣿⣿⡗⢨⠁⠄⠄⢳⡄⠄⠄⠄⢸
"""

def get_sys_info():
    return [
        ("OS", platform.system()),
        ("Host", platform.node()),
        ("Kernel", platform.release()),
        ("Uptime", subprocess.getoutput("uptime -p")),
        ("CPU", subprocess.getoutput("lscpu | grep 'Model name' | cut -d':' -f2 | xargs")),
        ("GPU", subprocess.getoutput("lspci | grep -i vga | cut -d':' -f3 | xargs"))
    ]

def main():
    info = get_sys_info()
    term_width = get_terminal_size().columns

    art_lines = MIKU_ART.split('\n')
    art_height = len(art_lines)
    max_art_width = max(len(line) for line in art_lines)

    max_key_len = max(len(key) for key, _ in info)
    text_padding = 3
    min_required_width = max_art_width + max_key_len + text_padding + 10

    if term_width < min_required_width:
        print("Terminal is too narrow for horizontal output")
        for key, value in info:
            print(f"{BLUE}{key}:{RESET} {value}")
        return

    info_count = len(info)
    start_index = (art_height - info_count) // 2

    for i in range(art_height):
        art_line = art_lines[i]

        if start_index <= i < start_index + info_count:
            key, value = info[i - start_index]
            text_line = f"{BLUE}{key.rjust(max_key_len)}:{RESET} {value}"
        else:
            text_line = ""

        print(f"{PINK}{art_line.ljust(max_art_width)}{RESET}{' ' * text_padding}{text_line}")

if __name__ == "__main__":
    main()