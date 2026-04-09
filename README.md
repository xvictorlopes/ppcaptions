# PU Prime Captions

An AI-powered subtitle studio that runs on your machine or on Google Colab. Transcribes, translates, and burns subtitles into videos using Whisper / WhisperX — fully automated.

---

## How it works

PU Prime Captions runs a complete pipeline — from raw media to a fully subtitled video — with no manual intervention.

```
Input  →  Transcription  →  Translation  →  Export
```

| Step | Description |
|---|---|
| **Input** | Local file, folder, or URL (YouTube, Twitch…) |
| **Transcription** | Whisper / WhisperX with voice activity detection (Silero or Pyannote VAD) |
| **Translation** | Google Translate or Gemini AI with context-aware chunking |
| **Export** | `.srt`, softsub (MP4 + subtitle track) and hardsub (burned-in captions) |

**Key features:**

- **Word-level alignment** — WhisperX aligns every word to the exact moment it is spoken
- **GPU acceleration** — auto-detects CUDA, MPS, or CPU; supports NVENC, VAAPI, AMF and other hardware encoders via FFmpeg
- **Automatic download** — pass a YouTube, Twitch, or any yt-dlp-supported URL directly
- **Softsub & Hardsub** — embedded subtitle track and/or captions burned into the video frames
- **TLTW summary** — "Too Long To Watch": Markdown summary with title, tags, key points, and timestamped chapters via Gemini AI
- **Docker support** — run in an isolated container with GPU support

---

## Run on Google Colab

No GPU? Use Google's free infrastructure without installing anything on your computer.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/xvictorlopes/ppcaptions/blob/main/ppcaptions.ipynb)

1. **Open the Notebook** — click the badge above (a Google account is required)
2. **Run the _Prepare_ cell** — installs ppcaptions, FFmpeg, fonts, and all dependencies; mounts Google Drive
3. **Set options in the _Configure_ cell** — input folder, Whisper model, target language, video codec, and more — all through a visual form
4. **Run the _Run_ cell** — processing starts; generated files are saved directly to your Google Drive

> **Tips:** Use the free **GPU T4** runtime for faster transcription. You can pass a YouTube URL directly in the `input_path` field. Free Colab sessions disconnect after ~12 hours.

---

## Installation

### uv (recommended)

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and run:

```sh
uv tool install git+https://github.com/xvictorlopes/ppcaptions.git
```

To upgrade:

```sh
uv tool upgrade ppcaptions
```

### pip

```sh
pip install ppcaptions
```

### From source

Requirements: Python 3.9–3.12, Git, FFmpeg.

```sh
git clone https://github.com/xvictorlopes/ppcaptions.git
cd ppcaptions
pip install -r requirements.txt --upgrade
```

> Windows: `choco install ffmpeg-full` · Linux: `apt install ffmpeg`

### Docker

```sh
# Build
docker compose build

# Process a video
docker compose run --rm ppcaptions -i /data/video.mp4 --translate pt

# With GPU (NVIDIA Container Toolkit required)
docker compose run --rm --gpus all ppcaptions -i /data/video.mp4
```

---

## Usage

```sh
ppcaptions -i [input_path] [options]
```

Minimum command:

```sh
ppcaptions -i /path/to/video.mp4
```

---

## CLI Reference

| Option | Description |
|---|---|
| `-i`, `--input_path` | Path to a media folder, single file, or URL. URLs are downloaded via yt-dlp. |
| `-ts:e`, `--transcription_engine` | Transcription engine: `whisperx` (default) or `whisper` |
| `-ts:m`, `--transcription_model` | Whisper model name or path. Default: `large-v3-turbo` |
| `-ts:d`, `--transcription_device` | Device: `auto` (default), `cpu`, `cuda` |
| `-ts:c`, `--transcription_compute_type` | Quantization: `default`, `int8`, `float16`, `float32`, etc. |
| `-ts:v`, `--transcription_vad` | VAD detector: `silero` (default) or `pyannote` |
| `-ts:b`, `--transcription_batch` | Batch size for WhisperX. Default: `4` |
| `--input_lang` | Force source language. Default: `auto` |
| `--translate` | Target language code (e.g. `pt-BR`, `fr`, `es`). Skipped if same as source. |
| `--translate_engine` | Translation engine: `google` (default) or `gemini` |
| `--gemini_api_key` | Gemini API key. Repeat for multiple keys (quota rotation). |
| `--tltw` | Generate a "Too Long To Watch" summary. Requires `--gemini_api_key`. |
| `--output_tltw` | Output folder for TLTW summaries. |
| `-c:v`, `--codec_video` | Video codec. Default: `h264`. Hardware: `h264_nvenc`, `h264_vaapi`, etc. |
| `-c:a`, `--codec_audio` | Audio codec. Default: `aac`. Options: `libopus`, `libmp3lame`, `pcm_s16le`. |
| `-o:s`, `--output_softsubs` | Output folder for softsub videos and `.srt` files. |
| `-o:h`, `--output_hardsubs` | Output folder for hardsub videos. |
| `-o:d`, `--output_downloads` | Output folder for downloaded media. |
| `--overwrite` | Overwrite existing output files. |
| `--subtitle_formats` | Subtitle formats to export: `srt`, `txt`. Example: `srt,txt`. |
| `--disable_softsubs` | Skip embedding subtitle track into the MP4 container. |
| `--disable_hardsubs` | Skip burning captions into the video frames. |
| `--process_input_subs` | Process existing `.srt` files in the input folder (translate / TLTW). |
| `--norm` | Normalize folder timestamps and run vidqa before processing. |
| `--copy_files` | Copy non-video files from the input directory to output directories. |

Run `ppcaptions --help` for the full list.

---

## Whisper Models

| Model | Parameters | VRAM | Speed | Quality | Best for |
|---|---|---|---|---|---|
| tiny | 39 M | ~1 GB | ●●●●● | ●○○○○ | Quick tests |
| small | 244 M | ~2 GB | ●●●●○ | ●●○○○ | Low VRAM machines |
| medium | 769 M | ~5 GB | ●●●○○ | ●●●○○ | General use |
| turbo | 809 M | ~6 GB | ●●●●○ | ●●●●○ | Great speed/quality tradeoff |
| large-v3 | 1.55 B | ~10 GB | ●●○○○ | ●●●●○ | High accuracy |
| **large-v3-turbo** *(default)* | 809 M | ~6 GB | ●●●●○ | ●●●●● | Best accuracy + speed |
| distil-large-v3 | 756 M | ~6 GB | ●●●●○ | ●●●○○ | English, fast and lightweight |

> VRAM estimated for float16. Actual usage depends on batch size and audio length.

---

## GPU Acceleration

ppcaptions automatically selects the best accelerator at runtime (`cuda` > `mps` > `cpu`). Override with `--transcription_device` if needed.

With Docker, expose GPUs via the NVIDIA Container Toolkit:

```sh
docker compose run --rm --gpus all ppcaptions -i /data/video.mp4
```

---

## Third-party tools

| Tool | Description |
|---|---|
| [Whisper](https://github.com/openai/whisper) | OpenAI speech recognition model trained on 680k hours of multilingual audio |
| [WhisperX](https://github.com/m-bain/whisperX) | Accelerated Whisper fork with forced word-level alignment and VAD support |
| [FFmpeg](https://ffmpeg.org) | Video/audio processing engine for muxing, burning, and transcoding |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Video downloader supporting YouTube, Twitch, Vimeo and thousands of platforms |
| [PyTorch](https://pytorch.org) | Deep learning framework that runs the Whisper models |
| [Gemini AI](https://aistudio.google.com) | Used optionally for high-quality translation and TLTW summary generation |
| [Silero VAD](https://github.com/snakers4/silero-vad) | Default voice activity detector used by WhisperX |
| [deep-translator](https://github.com/nidhaloff/deep-translator) | Python library abstracting multiple translation APIs |
| [pysrt](https://github.com/byroot/pysrt) | `.srt` file manipulation: reading, writing, and timestamp editing |

---

## License

This project is licensed under the terms of the [GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/).
