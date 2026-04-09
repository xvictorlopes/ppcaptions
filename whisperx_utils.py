import os
from pathlib import Path

import whisperx
import whisper
from whisperx import alignment, audio as wx_audio
import whisper_utils
import subtitle_utils
from utils import time_task

def transcribe_audio(model, audio_path: Path, srt_path: Path, lang: str = None, device: str = "cpu", batch_size: int = 4):
    audio = wx_audio.load_audio(file=audio_path.as_posix())

    # Transcribe
    with time_task("Running WhisperX transcription engine...", end='\n'):
        transcribe = model.transcribe(audio=audio, language=lang, batch_size=batch_size)

    # Align if possible
    if lang in alignment.DEFAULT_ALIGN_MODELS_HF or lang in alignment.DEFAULT_ALIGN_MODELS_TORCH:
        alignment_device = "cuda" if str(device).startswith("cuda") else "cpu"
        if alignment_device == "cuda":
            try:
                import torch
                if not torch.cuda.is_available():
                    alignment_device = "cpu"
            except Exception:
                alignment_device = "cpu"
        with time_task(message_start="Running alignment...", end='\n'):
            try:
                model_a, metadata = alignment.load_align_model(language_code=lang, device=alignment_device)
                transcribe = alignment.align(transcript=transcribe["segments"], model=model_a, align_model_metadata=metadata, audio=audio, device=alignment_device, return_char_alignments=True)
            except Exception:
                model_a, metadata = alignment.load_align_model(language_code=lang, device="cpu")  # force load on cpu due errors on gpu
                transcribe = alignment.align(transcript=transcribe["segments"], model=model_a, align_model_metadata=metadata, audio=audio, device="cpu", return_char_alignments=True)
    else:
        print(f"Language {lang} not suported for alignment. Skipping this step")

    # Format subtitles
    segments = subtitle_utils.format_segments(transcribe['segments'])

    # Save the subtitle file
    subtitle_utils.SaveSegmentsToSrt(segments, srt_path)

    return transcribe


def detect_language(model, audio_path: Path):
    try:
        if os.getenv("COLAB_RELEASE_TAG"):
            raise Exception("Method invalid for Google Colab")
        audio = wx_audio.load_audio(audio_path.as_posix())
        audio = wx_audio.pad_or_trim(audio, model.model.feature_extractor.n_samples)
        mel = wx_audio.log_mel_spectrogram(audio, n_mels=model.model.model.n_mels)
        encoder_output = model.model.encode(mel)
        results = model.model.model.detect_language(encoder_output)
        language_token, language_probability = results[0][0]
        return language_token[2:-2]
    except:
        print("using whisper base model for detection: ", end='')
        whisper_model = whisper.load_model("base", device="cpu", in_memory=True)
        return whisper_utils.detect_language(model=whisper_model, audio_path=audio_path)
