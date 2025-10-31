# mikufetch

Cute cross-platform system info fetcher with Hatsune Miku ASCII art.

Shows OS, kernel, uptime, CPU, memory and more next to a terminal Miku.

---

## Install

```bash
pip install mikufetch
```

---

## How to Use

### Linux / macOS
```bash
git clone https://github.com/yogurtmenn/mikufetch.git
cd mikufetch
pip install .    # install from local source directory
mikufetch

```
Or
```bash
pip install mikufetch
mikufetch
```

### Windows (PowerShell)
```powershell
git clone https://github.com/yogurtmenn/mikufetch.git
cd mikufetch
pip install .
mikufetch
```

---

## Options
- `--no-art`: print info without ASCII art
- `--no-color`: disable ANSI colors
- `--json`: output JSON only

Examples:
```bash
mikufetch --no-art
mikufetch --json
```

---

## Linux optional utilities

For best detection (Resolution and GPU), install these non-Python utilities:

- xrandr (for resolution)

Install commands by distro:

- Debian/Ubuntu: `sudo apt update && sudo apt install -y x11-xserver-utils mesa-utils`
- Arch: `sudo pacman -S --noconfirm xorg-xrandr mesa-demos`
- Fedora: `sudo dnf install -y xorg-x11-server-utils mesa-demos`


screen of fetch:
![Image alt](https://files.catbox.moe/zgzgzx.png)
by [pie with jam](https://github.com/pie-with-jam)
