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

def _is_linux() -> bool:
    """
    Check whether the system is macOS.

    Returns:
        bool: True on macOS, otherwise False.
    """
    return platform.system().lower() == "linux"


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
    if _is_windows():
        # Use the file version of ntoskrnl.exe to reflect the actual kernel build
        ps = (
            "powershell -NoProfile -Command "
            "\"$p='C:/Windows/System32/ntoskrnl.exe'; "
            "(Get-Item $p).VersionInfo.FileVersion\""
        )
        out = _run(ps)
        return out or platform.release()
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
    if _is_macos():
        raw = _run("sysctl hw.memsize")
        try:
            total = int(raw.split(":")[1].strip()) // (1024 * 1024)
            return f"{total} MiB"
        except:
            return "Unknown"

    if _is_windows():
        ps = (
            "powershell -NoProfile -Command "
            "\"$o=Get-CimInstance Win32_OperatingSystem; "
            "$u=[int](($o.TotalVisibleMemorySize-$o.FreePhysicalMemory)/1024); "
            "$t=[int]($o.TotalVisibleMemorySize/1024); "
            "'{0}MiB / {1}MiB' -f $u, $t\""
        )
        return _run(ps) or "Unknown"

    if platform.system().lower() == "linux":
        raw = _run("grep MemTotal /proc/meminfo")
        return raw.split()[1] + " kB"

    return "Unknown"

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
        return _run(cmd)


    if _is_macos():
        raw = _run("uptime")
        import re
        m = re.search(r"up (.+?),\s+\d+ user", raw)
        return m.group(1).replace(",", "") if m else "Unknown"


    if _is_linux():
        try:
            with open("/proc/uptime") as f:
                sec = float(f.read().split()[0])
        except:
            sec = 0
        d = int(sec // 86400)
        h = int((sec % 86400) // 3600)
        m = int((sec % 3600) // 60)
        return f"{d}d {h}h {m}m"

    return "Unknown"

def detect_packages() -> str:
    """
    Detect number of installed packages (Linux only).

    Returns:
        str: Package count or 'Unknown'.
    """
    if _is_windows() or _is_macos():
        return ""
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

    Returns:
        str: Resolution like '1920x1080' or 'Unknown'. On multi-monitor setups,
        returns the primary display resolution.
    """
    if _is_windows():
        ps = (
            "powershell -NoProfile -Command "
            "\"$v=Get-CimInstance Win32_VideoController | Where-Object {$_.CurrentHorizontalResolution -and $_.CurrentVerticalResolution} | Select-Object -First 1; "
            "if ($v) { '{0}x{1}' -f $v.CurrentHorizontalResolution,$v.CurrentVerticalResolution } "
            "else { Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SystemInformation]::PrimaryMonitorSize.Width.ToString() + 'x' + [System.Windows.Forms.SystemInformation]::PrimaryMonitorSize.Height }\""
        )
        return _run(ps) or "Unknown"

    if _is_macos():
        raw = _run("system_profiler SPDisplaysDataType | grep Resolution")
        # формат:      Resolution: 2560 x 1600 Retina
        parts = raw.replace("Resolution:", "").strip().split()
        if len(parts) >= 3:
            return f"{parts[0]}x{parts[2]}"
        return "Unknown"

    # Linux
    out = _run("xrandr --current 2>/dev/null | awk '/\\*/ {print $1; exit}'")
    if out:
        return out
    fb = _run("cat /sys/class/graphics/fb0/virtual_size 2>/dev/null")
    if fb and "," in fb:
        w, h = fb.split(",", 1)
        w = w.strip(); h = h.strip()
        if w.isdigit() and h.isdigit():
            return f"{w}x{h}"
    return "Unknown"


def get_sys_info() -> list[tuple[str, str]]:
    """
    Collect all system information points.

    Returns:
        list[tuple[str, str]]: List of (key, value) system info pairs.
    """
    items: list[tuple[str, str]] = [
        ("OS", detect_os()),
        ("Host", detect_host()),
        ("Kernel", detect_kernel()),
        ("Uptime", detect_uptime()),
    ]
    # Only show packages where it makes sense (primarily Linux distros)
    pkgs = detect_packages()
    if pkgs:
        items.append(("Packages", pkgs))
    items.extend([
        ("Shell", detect_shell()),
        ("Resolution", detect_resolution()),
        ("CPU", detect_cpu()),
        ("Memory", detect_memory()),
    ])
    return items
