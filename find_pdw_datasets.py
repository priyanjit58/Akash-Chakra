from pathlib import Path
import h5py


DATA_DIR = Path("../data/raw/tsrd")


files = list(DATA_DIR.rglob("*.h5")) + list(
    DATA_DIR.rglob("*.hdf5")
)


if not files:

    print("No TSRD HDF5 files found.")

    raise SystemExit


print("=" * 70)
print("SEARCHING FOR POSSIBLE PDW DATASETS")
print("=" * 70)


keywords = [
    "pdw",
    "pulse",
    "scan",
    "toa",
    "frequency",
    "freq",
    "amplitude",
    "aoa",
    "width"
]


for file_path in files:

    print("\n")
    print("-" * 70)

    print("FILE:")
    print(file_path)

    print("-" * 70)

    with h5py.File(file_path, "r") as h5:

        matches = []

        def visitor(name, obj):

            name_lower = name.lower()

            if isinstance(obj, h5py.Dataset):

                score = sum(
                    keyword in name_lower
                    for keyword in keywords
                )

                if score > 0:

                    matches.append(
                        (
                            score,
                            name,
                            obj.shape,
                            obj.dtype
                        )
                    )

        h5.visititems(visitor)

        matches.sort(
            key=lambda x: x[0],
            reverse=True
        )

        for score, name, shape, dtype in matches:

            print(
                f"\nScore : {score}"
                f"\nPath  : {name}"
                f"\nShape : {shape}"
                f"\nDtype : {dtype}"
            )


print("\n")
print("=" * 70)
print("SEARCH COMPLETE")
print("=" * 70)