# baselines/sequential_scan.py


class SequentialScanner:

    def __init__(self, band_ids):

        self.band_ids = list(band_ids)

        self.index = 0

    def select_band(self):

        band_id = self.band_ids[
            self.index
        ]

        self.index = (
            self.index + 1
        ) % len(self.band_ids)

        return band_id

    def reset(self):

        self.index = 0