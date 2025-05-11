import argparse
import os
import numpy as np
import speech_recognition as sr
import whisper
import torch
from datetime import datetime, timedelta, timezone
from queue import Queue
from time import sleep
from sys import platform

WAKE_WORD = "TOPSY"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="medium", help="Model to use",
                        choices=["tiny", "base", "small", "medium", "large"])
    parser.add_argument("--non_english", action='store_true')
    parser.add_argument("--energy_threshold", default=1000, type=int)
    parser.add_argument("--record_timeout", default=10, type=float)
    parser.add_argument("--phrase_timeout", default=20, type=float)
    args = parser.parse_args()

    data_queue = Queue()
    phrase_bytes = bytes()
    triggered = False
    last_phrase_time = None
    full_transcript = []

    recorder = sr.Recognizer()
    recorder.energy_threshold = args.energy_threshold
    recorder.dynamic_energy_threshold = False

    # Load Whisper model
    model = args.model + ".en" if not args.non_english and args.model != "large" else args.model
    audio_model = whisper.load_model(model)

    def record_callback(_, audio: sr.AudioData):
        data = audio.get_raw_data()
        data_queue.put(data)

    print("🔁 Initializing microphone and model...")

    source = sr.Microphone(sample_rate=16000)
    print("🎧 Calibrating ambient noise... please stay silent.")
    with source:
        recorder.adjust_for_ambient_noise(source)
    print("✅ Ready. Say the wake word to begin.")

    recorder.listen_in_background(source, record_callback, phrase_time_limit=args.record_timeout)

    while True:
        now = datetime.now(timezone.utc)

        if not data_queue.empty():
            phrase_complete = False
            if last_phrase_time and now - last_phrase_time > timedelta(seconds=args.phrase_timeout):
                if triggered:
                    print("\n⏹️ Detected silence. Ending phrase.\n")
                    print("📝 Final Transcription:")
                    print(" ".join(full_transcript).strip())
                    return
                phrase_bytes = bytes()
                phrase_complete = True

            last_phrase_time = now

            audio_chunk = b''.join(data_queue.queue)
            data_queue.queue.clear()
            phrase_bytes += audio_chunk

            audio_np = np.frombuffer(phrase_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
            text = result['text'].strip()

            if not triggered and WAKE_WORD.lower() in text.lower():
                triggered = True
                print(f"\n🟢 Wake word '{WAKE_WORD}' detected. Begin speaking...\n")
                phrase_bytes = bytes()
                full_transcript = []
            elif triggered:
                if phrase_complete:
                    full_transcript.append(text)
                else:
                    if full_transcript:
                        full_transcript[-1] = text
                    else:
                        full_transcript.append(text)

                os.system('cls' if os.name == 'nt' else 'clear')
                print("🎙️ Listening...\n")
                print(" ".join(full_transcript))

        sleep(0.25)

if __name__ == "__main__":
    main()
