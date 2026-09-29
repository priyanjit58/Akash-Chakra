# baselines/random_scan.py

import random


class RandomScanner:

    def __init__(
        self,
        band_ids,
        seed=42
    ):

        self.band_ids = list(
            band_ids
        )

        self.random = random.Random(
            seed
        )

    def select_band(self):

        return self.random.choice(
            self.band_ids
        )

    def reset(self):

        pass