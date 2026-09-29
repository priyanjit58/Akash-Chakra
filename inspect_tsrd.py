from pathlib import Path
import h5py


# ============================================================
# CONFIGURATION
# ============================================================

DATA_DIR = Path("../data/raw/tsrd")


# ============================================================
# FIND HDF5 FILES
# ============================================================

files = list(DATA_DIR.rglob("*.h5")) + list(DATA_DIR.rglob("*.hdf5"))

print("=" * 70)
print("TSRD FILE INSPECTOR")
print("=" * 70)

if not files:
    print("\nNo HDF5 files found.")
    print(f"Put your TSRD files inside:\n{DATA_DIR.resolve()}")
    raise SystemExit

print(f"\nFound {len(files)} HDF5 file(s):\n")

for i, file in enumerate(files, 1):
    print(f"{i}. {file}")


# ============================================================
# SELECT FIRST FILE
# ============================================================

file_path = files[0]

print("\n" + "=" * 70)
print("INSPECTING")
print(file_path)
print("=" * 70)


# ============================================================
# HDF5 RECURSIVE INSPECTOR
# ============================================================

def inspect_item(name, obj):

    indent = "  " * name.count("/")

    if isinstance(obj, h5py.Group):

        print(f"{indent}[GROUP] {name}")

    elif isinstance(obj, h5py.Dataset):

        print(f"{indent}[DATASET] {name}")

        print(f"{indent}  Shape : {obj.shape}")
        print(f"{indent}  Dtype : {obj.dtype}")

        if obj.attrs:

            print(f"{indent}  Attributes:")

            for key, value in obj.attrs.items():

                print(
                    f"{indent}    {key}: {value}"
                )


# ============================================================
# OPEN FILE
# ============================================================

with h5py.File(file_path, "r") as h5:

    print("\nHDF5 ROOT:")
    print(list(h5.keys()))

    print("\nFULL STRUCTURE:\n")

    h5.visititems(inspect_item)


print("\n" + "=" * 70)
print("INSPECTION COMPLETE")
print("=" * 70)