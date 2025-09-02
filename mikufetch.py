#!/usr/bin/env python3
import platform
import subprocess
from shutil import get_terminal_size

PINK = "\033[38;5;213m"
BLUE = "\033[38;5;39m"
CYAN = "\033[38;5;87m"
GREEN = "\033[38;5;84m"
YELLOW = "\033[38;5;228m"
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
    packages = ""
    try:
        packages = subprocess.getoutput("dpkg --list | wc -l").strip() + " (dpkg)"
    except:
        try:
            packages = subprocess.getoutput("rpm -qa | wc -l").strip() + " (rpm)"
        except:
            packages = "Unknown"
    
    shell = subprocess.getoutput("echo $SHELL").split('/')[-1]
    
    try:
        resolution = subprocess.getoutput("xrandr | grep '*' | head -1 | awk '{print $1}'")
    except:
        resolution = "Unknown"
    
    try:
        mem_total = int(subprocess.getoutput("grep MemTotal /proc/meminfo | awk '{print $2}'"))
        mem_used = int(subprocess.getoutput("grep MemAvailable /proc/meminfo | awk '{print $2}'"))
        mem_used = mem_total - mem_used
        memory = f"{mem_used//1024}MiB / {mem_total//1024}MiB"
    except:
        memory = "Unknown"
    
    return [
        ("OS", platform.system(), BLUE),
        ("Host", platform.node(), BLUE),
        ("Kernel", platform.release(), BLUE),
        ("Uptime", subprocess.getoutput("uptime -p"), BLUE),
        ("Packages", packages, GREEN),
        ("Shell", shell, GREEN),
        ("Resolution", resolution, GREEN),
        ("CPU", subprocess.getoutput("lscpu | grep 'Model name' | cut -d':' -f2 | xargs"), CYAN),
        ("GPU", subprocess.getoutput("lspci | grep -i vga | cut -d':' -f3 | xargs"), CYAN),
        ("Memory", memory, YELLOW)
    ]

def main():
    info = get_sys_info()
    term_width = get_terminal_size().columns

    art_lines = MIKU_ART.split('\n')
    art_height = len(art_lines)
    max_art_width = max(len(line) for line in art_lines)

    max_key_len = max(len(key) for key, _, _ in info)
    text_padding = 3
    min_required_width = max_art_width + max_key_len + text_padding + 15

    if term_width < min_required_width:
        print("Terminal is too narrow for horizontal output")
        for key, value, color in info:
            print(f"{color}{key}:{RESET} {value}")
        return

    info_count = len(info)
    start_index = (art_height - info_count) // 2

    for i in range(art_height):
        art_line = art_lines[i]

        if start_index <= i < start_index + info_count:
            key, value, color = info[i - start_index]
            text_line = f"{color}{key}:{RESET} {value}"
        else:
            text_line = ""

        print(f"{PINK}{art_line.ljust(max_art_width)}{RESET}{' ' * text_padding}{text_line}")

if __name__ == "__main__":
    main()
