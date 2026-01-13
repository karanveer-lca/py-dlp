# py-dlp 🎧🎥

A small Python CLI wrapper around **yt-dlp** to download:
- 🔉 **Audio as MP3** (optionally embed thumbnail + metadata)
- 🎥 **Video as webm/mp4** (optionally cap max resolution)

Uses:
- `questionary` for interactive prompts
- `rich` for nicer terminal UI

---

## ✨ Features

### 🔉 Audio
- Extract audio as **MP3**
- Optional:
  - `--embed-thumbnail`
  - `--add-metadata`
- Optional destination folder (`-P <path>`)

### 🎥 Video
- Download video in **webm** or **mp4**
- Optional max height cap: **1080 / 720 / 480 / 360**
- Merges audio + video into chosen container

---

## 📦 Dependencies

### Python packages
Installed via `requirements.txt`:
- `rich`
- `questionary`

Also required:
- `yt-dlp` (Python module)

### System dependency
- `ffmpeg` must be installed and accessible in PATH

---

## 🚀 Installation

### 1) Clone
```bash
git clone https://github.com/karanveer-lca/py-dlp.git
cd py-dlp
````

### 2) Create virtual environment (recommended)

**Linux/macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3) Install requirements

```bash
pip install -r requirements.txt
pip install -U yt-dlp
```

### 4) Install ffmpeg

**Ubuntu/Debian**

```bash
sudo apt update
sudo apt install -y ffmpeg
```

**Windows (winget)**

```powershell
winget install Gyan.FFmpeg
```

---

## ▶️ Usage

Run:

```bash
python main.py
```

You’ll see a menu:

* 🎥 Download Video
* 🔉 Download Audio

Then follow the prompts (URL, format, quality, destination, thumbnail/metadata toggles).

---

## 🧠 What this runs

### Audio command

Equivalent to:

```bash
python -m yt_dlp -x --audio-format mp3 --audio-quality 0 --embed-thumbnail --add-metadata <URL> -P <DEST>
```

### Video command

Builds a format string like:

* `bv*[ext=webm][height<=720]+ba[ext=opus]/b[ext=webm]/b`

Then runs:

```bash
python -m yt_dlp <URL> -f "<FORMAT_STRING>" --merge-output-format <webm|mp4>
```

---

## 📁 Output

* By default downloads into the **current directory**
* For audio, you can set a destination folder prompt (uses yt-dlp `-P`)

---

## ⚠️ Notes / Common Problems

* If `ffmpeg` isn’t installed, audio extraction/merging will fail.
* Some videos may not have the requested container/codec combo available; yt-dlp will try to pick best match but can still fail.
* YouTube sometimes rate-limits or blocks downloads; updating yt-dlp usually helps:

```bash
pip install -U yt-dlp
```

---

## 🛠️ Dev Notes

* URL validation requires `http://` or `https://`
* Dependency checks:

  * `python -m yt_dlp --version`
  * `ffmpeg -version`

---

## 📜 License

Unspecified. Add a LICENSE file if you want other humans to know what they’re allowed to do.

---

### Q1: Do you want the README to be Linux-only (cleaner) or keep Windows steps too?

### Q2: Do you want an “Examples” section showing real prompts and outputs?

### Q3: Should I also generate a `pyproject.toml` so installation is one clean `pip install .`?
