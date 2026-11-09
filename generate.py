
import os
import pickle
import numpy as np
import pretty_midi
import tensorflow as tf

# ---------------- CONFIGURATION ----------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model", "lstm_music_model.keras")
NOTES_PATH = os.path.join(BASE_DIR, "model", "notes.pkl")
OUTPUT_PATH = os.path.join(BASE_DIR, "generated_music.mid")

SEQUENCE_LENGTH = 50

GENERATE_NOTES = int(
    os.getenv("MELODYAI_GENERATE_NOTES", "300")
)

TEMPERATURE = float(
    os.getenv("MELODYAI_TEMPERATURE", "1.0")
)

# ---------------- LOAD MODEL ----------------

print("Loading trained LSTM model...")
model = tf.keras.models.load_model(MODEL_PATH)

print("Loading musical notes...")
with open(NOTES_PATH, "rb") as file:
    notes = pickle.load(file)

if len(notes) < SEQUENCE_LENGTH:
    raise ValueError("Not enough notes available for generation.")

seed = np.array(notes[:SEQUENCE_LENGTH], dtype=np.int32)
generated_notes = list(seed)

# ---------------- GENERATE MUSIC ----------------

print("\nGenerating new music...")
print("Notes:", GENERATE_NOTES)
print("Creativity:", TEMPERATURE)

for i in range(GENERATE_NOTES):

    sequence = np.array(
        generated_notes[-SEQUENCE_LENGTH:],
        dtype=np.int32
    ).reshape(1, SEQUENCE_LENGTH)

    predictions = model(
        sequence,
        training=False
    ).numpy()[0]

    predictions = np.log(predictions + 1e-8) / TEMPERATURE

    probabilities = np.exp(
        predictions - np.max(predictions)
    )

    probabilities /= probabilities.sum()

    next_note = np.random.choice(
        128,
        p=probabilities
    )

    generated_notes.append(int(next_note))

# ---------------- CONVERT TO MIDI ----------------

print("Converting generated notes to MIDI...")

midi = pretty_midi.PrettyMIDI()

piano = pretty_midi.Instrument(program=0)

current_time = 0.0
duration = 0.35

for pitch in generated_notes[SEQUENCE_LENGTH:]:

    note = pretty_midi.Note(
        velocity=90,
        pitch=int(pitch),
        start=current_time,
        end=current_time + duration
    )

    piano.notes.append(note)

    current_time += duration

midi.instruments.append(piano)

midi.write(OUTPUT_PATH)

print("\nMusic generated successfully!")
print("Output file:", OUTPUT_PATH)
print("Generated notes:", GENERATE_NOTES)
