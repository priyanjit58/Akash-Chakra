from dataclasses import dataclass


@dataclass
class DwellController:
    minimum_dwell: float = 0.01
    maximum_dwell: float = 0.10

    def validate(self, dwell_time: float) -> float:

        dwell_time = float(dwell_time)

        if dwell_time < self.minimum_dwell:
            dwell_time = self.minimum_dwell

        if dwell_time > self.maximum_dwell:
            dwell_time = self.maximum_dwell

        return dwell_time