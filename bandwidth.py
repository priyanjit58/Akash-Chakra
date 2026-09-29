from dataclasses import dataclass


@dataclass
class ReceiverBandwidth:
    center_frequency: float
    bandwidth: float

    @property
    def lower_frequency(self):
        return self.center_frequency - self.bandwidth / 2

    @property
    def upper_frequency(self):
        return self.center_frequency + self.bandwidth / 2

    def contains(self, frequency: float) -> bool:
        return (
            self.lower_frequency
            <= frequency
            <= self.upper_frequency
        )

    def describe(self):
        return {
            "center_frequency": self.center_frequency,
            "bandwidth": self.bandwidth,
            "lower_frequency": self.lower_frequency,
            "upper_frequency": self.upper_frequency,
        }