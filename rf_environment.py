import random


class RFEnvironment:

    def __init__(self, seed=42):

        random.seed(seed)

        self.signals = []

    def add_signal(
        self,
        time,
        frequency,
        amplitude=1.0,
        emitter_id="E1"
    ):

        self.signals.append({

            "time": float(time),

            "frequency": float(frequency),

            "amplitude": float(amplitude),

            "emitter_id": emitter_id
        })

    def get_activity(self):

        return self.signals

    def generate_demo_environment(self):

        self.signals = []

        # --------------------------------------------
        # Emitter A
        # Mostly fixed
        # --------------------------------------------

        for t in range(0, 100, 5):

            self.add_signal(
                time=t,
                frequency=100,
                amplitude=0.9,
                emitter_id="E1"
            )

        # --------------------------------------------
        # Emitter B
        # Periodic hopping
        # --------------------------------------------

        frequencies = [
            200,
            220,
            240,
            260
        ]

        for i, t in enumerate(range(0, 100, 4)):

            self.add_signal(
                time=t,
                frequency=frequencies[i % len(frequencies)],
                amplitude=0.8,
                emitter_id="E2"
            )

        # --------------------------------------------
        # Emitter C
        # Appears later
        # --------------------------------------------

        for t in range(50, 100, 6):

            self.add_signal(
                time=t,
                frequency=350,
                amplitude=0.7,
                emitter_id="E3"
            )

        self.signals.sort(
            key=lambda x: x["time"]
        )

        return self.signals