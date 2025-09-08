# mikufetch
a simple cross-platform system info fetch script with a Hatsune Miku ASCII art.

this script shows basic system info like OS, kernel, uptime, CPU, GPU and more - all next to a cute Hatsune Miku in your terminal!
---

## how to Use

### linux / macOS
```bash
git clone https://github.com/yogurtmenn/mikufetch.git
cd mikufetch
chmod +x mikufetch.py
./mikufetch.py
```

### windows (powershell)
```powershell
git clone https://github.com/yogurtmenn/mikufetch.git
cd mikufetch
python .\mikufetch.py
```

---

## options
- `--no-art`: print info without ASCII art
- `--no-color`: disable ANSI colors
- `--json`: output JSON only

examples:
```bash
./mikufetch.py --no-art
./mikufetch.py --json
```
