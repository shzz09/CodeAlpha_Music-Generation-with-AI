
import os
import pickle
import pretty_midi

DATASET_PATH = "dataset/midi"
OUTPUT_PATH = "model"

os.makedirs(OUTPUT_PATH, exist_ok=True)

notes = []

# Collect MIDI files
midi_files = []

for root, dirs, files in os.walk(DATASET_PATH):
    for file in files:
        if file.lower().endswith((".mid", ".midi")):
            midi_files.append(os.path.join(root, file))

print(f"Total MIDI files found: {len(midi_files)}")
print("Fast preprocessing started...\n")

# Process MIDI files
for index, file_path in enumerate(midi_files, 1):

    try:
        midi = pretty_midi.PrettyMIDI(file_path)

        for instrument in midi.instruments:

            if instrument.is_drum:
                continue

            # Sort notes by starting time
            sorted_notes = sorted(
                instrument.notes,
                key=lambda n: n.start
            )

            for n in sorted_notes:
                notes.append(n.pitch)

    except Exception:
        pass

    if index % 25 == 0:
        print(f"Processed {index}/{len(midi_files)} files")

# Save extracted notes
with open(os.path.join(OUTPUT_PATH, "notes.pkl"), "wb") as f:
    pickle.dump(notes, f)

print("\nPreprocessing completed!")
print("Total notes extracted:", len(notes))
print("Saved: model/notes.pkl")
