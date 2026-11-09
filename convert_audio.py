import pretty_midi
import numpy as np
from scipy.io import wavfile

print("Loading generated MIDI...")
midi = pretty_midi.PrettyMIDI("generated_music.mid")

print("Converting MIDI to WAV...")
audio = midi.synthesize(fs=22050)

# Normalize audio
audio = np.clip(audio, -1.0, 1.0)
audio = (audio * 32767).astype(np.int16)

wavfile.write("generated_music.wav", 22050, audio)

print("\nAudio conversion completed!")
print("Saved: generated_music.wav")