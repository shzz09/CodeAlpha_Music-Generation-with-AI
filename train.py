
import os
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# CONFIGURATION
SEQUENCE_LENGTH = 50
MAX_NOTES = 200000
STRIDE = 3
EPOCHS = 5
BATCH_SIZE = 128

MODEL_PATH = "model/lstm_music_model.keras"

# Reproducibility
np.random.seed(42)
tf.random.set_seed(42)

print("================================")
print("     MELODYAI - LSTM TRAINING")
print("================================")

# LOAD DATASET
print("\nLoading extracted musical notes...")

with open("model/notes.pkl", "rb") as file:
    notes = pickle.load(file)

if len(notes) <= SEQUENCE_LENGTH:
    raise ValueError("Not enough musical notes for training.")

# Limit dataset for CPU training
notes = np.asarray(notes[:MAX_NOTES], dtype=np.int32)

if np.any((notes < 0) | (notes > 127)):
    raise ValueError("Invalid MIDI pitch values found.")

print("Total notes loaded:", len(notes))

# CREATE SEQUENCES
print("\nPreparing training sequences...")

windows = np.lib.stride_tricks.sliding_window_view(
    notes, SEQUENCE_LENGTH + 1
)[::STRIDE]

X = windows[:, :-1].copy()
y = windows[:, -1].copy()

# Train-validation split
split = int(len(X) * 0.90)

X_train, X_val = X[:split], X[split:]
y_train, y_val = y[:split], y[split:]

print("Training samples:", len(X_train))
print("Validation samples:", len(X_val))

# BUILD LSTM MODEL
print("\nBuilding LSTM neural network...")

model = Sequential([
    Embedding(input_dim=128, output_dim=64,
              input_length=SEQUENCE_LENGTH),

    LSTM(128),

    Dropout(0.2),

    Dense(128, activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# CALLBACKS
os.makedirs("model", exist_ok=True)

callbacks = [
    EarlyStopping(
        monitor="val_loss",
        patience=2,
        restore_best_weights=True
    ),
    ModelCheckpoint(
        MODEL_PATH,
        monitor="val_loss",
        save_best_only=True
    )
]

# TRAIN MODEL
print("\nStarting LSTM training...\n")

history = model.fit(
    X_train,
    y_train,
    validation_data=(X_val, y_val),
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    shuffle=True,
    callbacks=callbacks,
    verbose=1
)

# SAVE MODEL
model.save(MODEL_PATH)

print("\n================================")
print("       TRAINING COMPLETED!")
print("================================")
print("Model saved successfully!")
print("Location:", MODEL_PATH)
print("Final training accuracy:",
      round(history.history["accuracy"][-1] * 100, 2), "%")
print("Final validation accuracy:",
      round(history.history["val_accuracy"][-1] * 100, 2), "%")

