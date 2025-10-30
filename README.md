# mikufetch

Cute cross-platform system info fetcher with Hatsune Miku ASCII art.

Shows OS, kernel, uptime, CPU, GPU, memory and more next to a terminal Miku.

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
