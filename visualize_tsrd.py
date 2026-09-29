from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


INPUT_FILE = Path(
    "../data/processed/tsrd_sample.csv"
)


df = pd.read_csv(INPUT_FILE)


print("=" * 70)
print("TSRD VISUALIZATION")
print("=" * 70)

print("\nRows:", len(df))


# ============================================================
# FREQUENCY VS TIME
# ============================================================

plt.figure(
    figsize=(14, 6)
)

plt.scatter(
    df["ToA"],
    df["Frequency"],
    s=2,
    alpha=0.5
)

plt.xlabel(
    "Time of Arrival"
)

plt.ylabel(
    "Centre Frequency"
)

plt.title(
    "TSRD Pulse Activity — Frequency vs Time"
)

plt.grid(
    alpha=0.2
)

plt.tight_layout()

plt.show()


# ============================================================
# PULSE WIDTH
# ============================================================

plt.figure(
    figsize=(12, 5)
)

plt.hist(
    df["PulseWidth"],
    bins=80
)

plt.xlabel(
    "Pulse Width"
)

plt.ylabel(
    "Pulse Count"
)

plt.title(
    "TSRD Pulse Width Distribution"
)

plt.grid(
    alpha=0.2
)

plt.tight_layout()

plt.show()


# ============================================================
# AMPLITUDE
# ============================================================

plt.figure(
    figsize=(12, 5)
)

plt.hist(
    df["Amplitude"],
    bins=80
)

plt.xlabel(
    "Amplitude"
)

plt.ylabel(
    "Pulse Count"
)

plt.title(
    "TSRD Amplitude Distribution"
)

plt.grid(
    alpha=0.2
)

plt.tight_layout()

plt.show()