from pathlib import Path

import h5py
import numpy as np
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = Path(
    "../data/raw/tsrd/YOUR_FILE.h5"
)

OUTPUT_FILE = Path(
    "../data/processed/tsrd_sample.csv"
)


# ============================================================
# CHANGE THIS AFTER INSPECTION
# ============================================================

DATASET_PATH = "REPLACE_WITH_REAL_DATASET_PATH"


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("TSRD EXTRACTION")
print("=" * 70)

print("\nInput:")
print(INPUT_FILE)

print("\nDataset:")
print(DATASET_PATH)


with h5py.File(INPUT_FILE, "r") as h5:

    if DATASET_PATH not in h5:

        print("\nDataset path not found.")

        print("\nAvailable root objects:")

        for key in h5.keys():

            print(" -", key)

        raise KeyError(
            f"Dataset '{DATASET_PATH}' not found."
        )

    dataset = h5[DATASET_PATH]

    print("\nShape:")
    print(dataset.shape)

    print("\nDtype:")
    print(dataset.dtype)

    data = dataset[:]


# ============================================================
# CONVERT TO NUMPY
# ============================================================

data = np.asarray(data)

print("\nLoaded array:")
print(data.shape)


# ============================================================
# BASIC VALIDATION
# ============================================================

if data.ndim != 2:

    raise ValueError(
        "Expected a 2D PDW matrix."
    )


print("\nNumber of rows:", data.shape[0])
print("Number of columns:", data.shape[1])


# ============================================================
# CREATE DATAFRAME
# ============================================================

if data.shape[1] >= 5:

    df = pd.DataFrame(
        data[:, :5],
        columns=[
            "ToA",
            "Frequency",
            "PulseWidth",
            "AoA",
            "Amplitude"
        ]
    )

else:

    raise ValueError(
        "Dataset has fewer than 5 columns."
    )


# ============================================================
# CLEAN NUMERIC DATA
# ============================================================

for column in df.columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


df = df.dropna()


# ============================================================
# SORT BY TIME
# ============================================================

df = df.sort_values(
    "ToA"
).reset_index(drop=True)


# ============================================================
# PRINT SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("PDW SUMMARY")
print("=" * 70)

print(df.head())

print("\nShape:")
print(df.shape)

print("\nStatistics:")

print(
    df.describe()
)


# ============================================================
# SAVE
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\nSaved:")
print(OUTPUT_FILE.resolve())

print("\nExtraction complete.")