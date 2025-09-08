#!/usr/bin/env python3
import platform
import subprocess
import os
import json
import shlex
import sys
from shutil import get_terminal_size
from argparse import ArgumentParser

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

def _run(cmd: str) -> str:
    try:
        return subprocess.getoutput(cmd).strip()
    except Exception:
        return ""


def _is_windows() -> bool:
    return platform.system().lower() == "windows"


def _is_macos() -> bool:
    return platform.system().lower() == "darwin"


def _detect_packages() -> str:
    if _is_windows() or _is_macos():
        return "Unknown"
    out = _run("dpkg --list | wc -l")
    if out:
        return f"{out} (dpkg)"
    out = _run("rpm -qa | wc -l")
    if out:
        return f"{out} (rpm)"
    return "Unknown"


def _detect_shell() -> str:
    if _is_windows():
        # Try PowerShell, then ComSpec
        if os.environ.get("PSModulePath"):
            return "powershell"
        return os.environ.get("ComSpec", "cmd").split("\\")[-1]
    sh = os.environ.get("SHELL") or _run("echo $SHELL")
    return sh.split("/")[-1] if sh else "Unknown"


def _detect_resolution() -> str:
    if _is_windows():
        ps = (
            "powershell -NoProfile -Command "
            "\"$v = Get-CimInstance Win32_VideoController | Select-Object -First 1 "
            "-Property CurrentHorizontalResolution,CurrentVerticalResolution; "
            "if ($v.CurrentHorizontalResolution -and $v.CurrentVerticalResolution) "
            "{ '{0}x{1}' -f $v.CurrentHorizontalResolution,$v.CurrentVerticalResolution }\""
        )
        out = _run(ps)
        if out:
            return out
        ps_fallback = (
            "powershell -NoProfile -Command "
            "\"$m = Get-CimInstance Win32_DesktopMonitor | Select-Object -First 1 "
            "-Property ScreenWidth,ScreenHeight; "
            "if ($m.ScreenWidth -and $m.ScreenHeight) { '{0}x{1}' -f $m.ScreenWidth,$m.ScreenHeight }\""
        )
        out = _run(ps_fallback)
        return out or "Unknown"
    if _is_macos():
        # Parse system_profiler output
        out = _run("system_profiler SPDisplaysDataType | grep Resolution | head -1")
        # Example:      Resolution: 2560 x 1440
        parts = out.replace(":", " ").split()
        for i, p in enumerate(parts):
            if p.isdigit() and i + 2 < len(parts) and parts[i + 1] == "x" and parts[i + 2].isdigit():
                return f"{parts[i]}x{parts[i+2]}"
        return "Unknown"
    # Linux
    out = _run("xrandr | grep '*' | head -1 | awk '{print $1}'")
    return out or "Unknown"


def _detect_memory() -> str:
    if _is_windows():
        ps = (
            "powershell -NoProfile -Command "
            "\"$o=Get-CimInstance Win32_OperatingSystem; "
            "$u=[int](($o.TotalVisibleMemorySize-$o.FreePhysicalMemory)/1024); "
            "$t=[int]($o.TotalVisibleMemorySize/1024); "
            "'{0}MiB / {1}MiB' -f $u, $t\""
        )
        out = _run(ps)
        return out or "Unknown"
    if _is_macos():
        # vm_stat outputs page counts; first get page size
        page_size_line = _run("sysctl hw.pagesize")
        try:
            page_size = int(page_size_line.split(":", 1)[1])
            vm = _run("vm_stat")
            stats = {}
            for line in vm.splitlines():
                if ":" in line:
                    key, val = line.split(":", 1)
                    stats[key.strip()] = int(val.strip().strip(". "))
            total_pages = sum(
                stats.get(k, 0)
                for k in [
                    "Pages active",
                    "Pages inactive",
                    "Pages speculative",
                    "Pages wired down",
                    "Pages free",
                    "Pages throttled",
                    "Pages occupied by compressor",
                ]
            )
            free_pages = stats.get("Pages free", 0)
            used_bytes = (total_pages - free_pages) * page_size
            total_bytes = total_pages * page_size
            return f"{used_bytes // (1024*1024)}MiB / {total_bytes // (1024*1024)}MiB"
        except Exception:
            return "Unknown"
    # Linux
    try:
        mem_total = int(_run("grep MemTotal /proc/meminfo | awk '{print $2}'"))
        mem_avail = int(_run("grep MemAvailable /proc/meminfo | awk '{print $2}'"))
        mem_used = mem_total - mem_avail
        return f"{mem_used//1024}MiB / {mem_total//1024}MiB"
    except Exception:
        return "Unknown"


def _detect_cpu() -> str:
    if _is_windows():
        ps = (
            "powershell -NoProfile -Command "
            "\"(Get-CimInstance Win32_Processor | Select-Object -ExpandProperty Name | Select-Object -First 1)\""
        )
        out = _run(ps)
        return out or (platform.processor() or "Unknown")
    if _is_macos():
        out = _run("sysctl -n machdep.cpu.brand_string")
        return out or platform.processor() or "Unknown"
    # Linux
    out = _run("lscpu | grep 'Model name' | cut -d':' -f2 | xargs")
    return out or platform.processor() or "Unknown"


def _detect_gpu() -> str:
    if _is_windows():
        ps = (
            "powershell -NoProfile -Command "
            "\"(Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name | Select-Object -First 1)\""
        )
        out = _run(ps)
        return out or "Unknown"
    if _is_macos():
        out = _run("system_profiler SPDisplaysDataType | grep 'Chipset Model' | head -1 | cut -d':' -f2 | xargs")
        return out or "Unknown"
    # Linux
    out = _run("lspci | grep -i vga | cut -d':' -f3 | xargs")
    return out or "Unknown"


def _detect_uptime() -> str:
    if _is_windows():
        cmd = (
            "powershell -NoProfile -Command "
            "\"$ts=(Get-Date)-(Get-CimInstance Win32_OperatingSystem).LastBootUpTime; "
            "'{0}d {1}h {2}m' -f [int]$ts.Days,[int]$ts.Hours,[int]$ts.Minutes\""
        )
        out = _run(cmd)
        return out or "Unknown"
    if _is_macos() or platform.system().lower() == "linux":
        out = _run("uptime -p")
        return out or "Unknown"
    return "Unknown"


def get_sys_info():
    return [
        ("OS", platform.platform(), BLUE),
        ("Host", platform.node(), BLUE),
        ("Kernel", platform.release(), BLUE),
        ("Uptime", _detect_uptime(), BLUE),
        ("Packages", _detect_packages(), GREEN),
        ("Shell", _detect_shell(), GREEN),
        ("Resolution", _detect_resolution(), GREEN),
        ("CPU", _detect_cpu(), CYAN),
        ("GPU", _detect_gpu(), CYAN),
        ("Memory", _detect_memory(), YELLOW),
    ]

def main():
    parser = ArgumentParser(description="Cute cross-platform system info fetch with Miku ASCII art")
    parser.add_argument("--no-art", action="store_true", help="do not display ASCII art")
    parser.add_argument("--no-color", action="store_true", help="disable ANSI colors")
    parser.add_argument("--json", action="store_true", help="output info as JSON only")
    args = parser.parse_args()

    global PINK, BLUE, CYAN, GREEN, YELLOW, RESET
    if args.no_color or (not sys.stdout.isatty() if 'sys' in globals() else False):
        PINK = BLUE = CYAN = GREEN = YELLOW = RESET = ""

    info = get_sys_info()

    if args.json:
        data = {key: value for key, value, _ in info}
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    if args.no_art:
        for key, value, color in info:
            print(f"{color}{key}:{RESET} {value}")
        return

    term_width = get_terminal_size().columns
    art_lines = MIKU_ART.split('\n')
    art_height = len(art_lines)
    max_art_width = max(len(line) for line in art_lines)

    max_key_len = max(len(key) for key, _, _ in info)
    text_padding = 3
    min_required_width = max_art_width + max_key_len + text_padding + 15

    if term_width < min_required_width:
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
