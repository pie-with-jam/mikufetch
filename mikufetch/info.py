"""System information detection module for Mikufetch.

This module collects system details across different platforms (Windows, macOS, Linux)
and returns them in a unified format for rendering in the CLI.
"""

import platform
import subprocess
import os


def _run(cmd: str) -> str:
    """
    Execute a shell command and return its output as a trimmed string.

    Args:
        cmd (str): Command to run.

    Returns:
        str: Command output or empty string if execution failed.
    """
    try:
        return subprocess.getoutput(cmd).strip()
    except Exception:
        return ""


def _is_windows() -> bool:
    """
    Check whether the system is Windows.

    Returns:
        bool: True on Windows, otherwise False.
    """
    return platform.system().lower() == "windows"


def _is_macos() -> bool:
    """
    Check whether the system is macOS.

    Returns:
        bool: True on macOS, otherwise False.
    """
    return platform.system().lower() == "darwin"


def detect_os() -> str:
    """
    Get OS name and version string.

    Returns:
        str: OS identifier (e.g., Windows-10, Linux, macOS version).
    """
    return platform.platform()


def detect_host() -> str:
    """
    Get system hostname.

    Returns:
        str: Hostname string.
    """
    return platform.node()


def detect_kernel() -> str:
    """
    Get kernel version.

    Returns:
        str: Kernel release version.
    """
    return platform.release()


def detect_shell() -> str:
    """
    Detect the active shell name.

    Returns:
        str: Shell name (cmd, powershell, bash, zsh, etc.) or 'Unknown'.
    """
    if _is_windows():
        return os.environ.get("ComSpec", "cmd").split("\\")[-1]
    sh = os.environ.get("SHELL") or _run("echo $SHELL")
    return sh.split("/")[-1] if sh else "Unknown"


def detect_cpu() -> str:
    """
    Detect CPU model string.

    Returns:
        str: CPU model name or 'Unknown'.
    """
    if _is_windows():
        out = _run("powershell -NoProfile -Command "
                   "\"(Get-CimInstance Win32_Processor | Select-Object -ExpandProperty Name | Select-Object -First 1)\"")
        return out or platform.processor() or "Unknown"
    if _is_macos():
        return _run("sysctl -n machdep.cpu.brand_string") or platform.processor() or "Unknown"
    return _run("lscpu | grep 'Model name' | cut -d':' -f2 | xargs") or platform.processor() or "Unknown"


def detect_memory() -> str:
    """
    Detect memory usage and total RAM.

    Returns:
        str: Memory usage in format 'UsedMiB / TotalMiB' or 'Unknown'.
    """
    if _is_windows():
        ps = (
            "powershell -NoProfile -Command "
            "\"$o=Get-CimInstance Win32_OperatingSystem; "
            "$u=[int](($o.TotalVisibleMemorySize-$o.FreePhysicalMemory)/1024); "
            "$t=[int]($o.TotalVisibleMemorySize/1024); "
            "'{0}MiB / {1}MiB' -f $u, $t\""
        )
        return _run(ps) or "Unknown"

    try:
        mem_total = int(_run("grep MemTotal /proc/meminfo | awk '{print $2}'"))
        mem_avail = int(_run("grep MemAvailable /proc/meminfo | awk '{print $2}'"))
        mem_used = mem_total - mem_avail
        return f"{mem_used//1024}MiB / {mem_total//1024}MiB"
    except Exception:
        return "Unknown"


def detect_gpu() -> str:
    """
    Detect main GPU name.

    Returns:
        str: GPU model string or 'Unknown'.
    """
    if _is_windows():
        return _run("powershell -NoProfile -Command "
                    "\"(Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name | Select-Object -First 1)\"") or "Unknown"
    return _run("lspci | grep -i vga | cut -d':' -f3 | xargs") or "Unknown"


def detect_uptime() -> str:
    """
    Detect system uptime.

    Returns:
        str: Human-readable uptime (e.g., '2d 5h 11m') or raw uptime string on Linux.
    """
    if _is_windows():
        cmd = ("powershell -NoProfile -Command "
               "\"$ts=(Get-Date)-(Get-CimInstance Win32_OperatingSystem).LastBootUpTime; "
               "'{0}d {1}h {2}m' -f [int]$ts.Days,[int]$ts.Hours,[int]$ts.Minutes\"")
        return _run(cmd) or "Unknown"
    return _run("uptime -p") or "Unknown"


def detect_packages() -> str:
    """
    Detect number of installed packages (Linux only).

    Returns:
        str: Package count or 'Unknown'.
    """
    if _is_windows() or _is_macos():
        return "Unknown"
    out = _run("dpkg --list | wc -l")
    if out:
        return f"{out} (dpkg)"
    out = _run("rpm -qa | wc -l")
    if out:
        return f"{out} (rpm)"
    return "Unknown"


def detect_resolution() -> str:
    """
    Detect screen resolution.

    Note:
        Not implemented — placeholder for future support.

    Returns:
        str: 'Unknown'
    """
    return "Unknown"


def get_sys_info() -> list[tuple[str, str]]:
    """
    Collect all system information points.

    Returns:
        list[tuple[str, str]]: List of (key, value) system info pairs.
    """
    return [
        ("OS", detect_os()),
        ("Host", detect_host()),
        ("Kernel", detect_kernel()),
        ("Uptime", detect_uptime()),
        ("Packages", detect_packages()),
        ("Shell", detect_shell()),
        ("Resolution", detect_resolution()),
        ("CPU", detect_cpu()),
        ("GPU", detect_gpu()),
        ("Memory", detect_memory()),
    ]
