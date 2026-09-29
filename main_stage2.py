from environment.rf_environment import RFEnvironment
from environment.frequency_model import create_frequency_bands

from receiver.esm_receiver import VirtualESMReceiver


def main():

    print("=" * 60)
    print("AKASH CHAKRA")
    print("STAGE 2 — VIRTUAL ESM RECEIVER")
    print("=" * 60)

    # --------------------------------------------------
    # 1. CREATE RF ENVIRONMENT
    # --------------------------------------------------

    environment = RFEnvironment(
        seed=42
    )

    activity = (
        environment.generate_demo_environment()
    )

    print(
        f"\nRF activity generated: "
        f"{len(activity)} pulses"
    )

    # --------------------------------------------------
    # 2. CREATE FREQUENCY BANDS
    # --------------------------------------------------

    bands = create_frequency_bands(
        start_frequency=50,
        end_frequency=400,
        number_of_bands=36
    )

    print(
        f"Frequency bands: {len(bands)}"
    )

    # --------------------------------------------------
    # 3. CREATE VIRTUAL ESM
    # --------------------------------------------------

    receiver = VirtualESMReceiver(

        bands=bands,

        bandwidth=10.0,

        minimum_dwell=1.0,

        maximum_dwell=5.0,

        switching_time=0.5
    )

    # --------------------------------------------------
    # 4. MANUAL SCAN SEQUENCE
    # --------------------------------------------------

    scan_sequence = [
        5,
        10,
        15,
        20,
        25,
        30
    ]

    print("\nStarting receiver scans...\n")

    for band_id in scan_sequence:

        observation = receiver.scan(

            band_id=band_id,

            dwell_time=2.0,

            rf_activity=activity
        )

        print(observation)

    # --------------------------------------------------
    # 5. SUMMARY
    # --------------------------------------------------

    history = receiver.get_history()

    hits = sum(
        1
        for observation in history
        if observation["hit"]
    )

    misses = len(history) - hits

    print("\n" + "=" * 60)

    print("RECEIVER SUMMARY")

    print("=" * 60)

    print(
        f"Total scans : {len(history)}"
    )

    print(
        f"HITs         : {hits}"
    )

    print(
        f"MISSes       : {misses}"
    )

    print(
        f"Current time : "
        f"{receiver.current_time:.2f}"
    )


if __name__ == "__main__":
    main()