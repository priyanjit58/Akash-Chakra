from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Observation:

    time: float

    band_id: int

    center_frequency: float

    dwell_time: float

    hit: bool

    observed_frequency: Optional[float] = None

    pulse_count: int = 0

    signal_strength: Optional[float] = None

    observation_status: str = "UNKNOWN"

    def to_dict(self):
        return asdict(self)

    def __repr__(self):

        return (
            f"Observation("
            f"t={self.time:.3f}, "
            f"band={self.band_id}, "
            f"freq={self.center_frequency:.2f}, "
            f"hit={self.hit}, "
            f"pulses={self.pulse_count})"
        )