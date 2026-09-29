from typing import List, Dict, Any

from receiver.bandwidth import ReceiverBandwidth
from receiver.dwell import DwellController
from receiver.observation import Observation


class VirtualESMReceiver:

    def __init__(
        self,
        bands: List[Dict[str, Any]],
        bandwidth: float = 10.0,
        minimum_dwell: float = 0.01,
        maximum_dwell: float = 0.10,
        switching_time: float = 0.005,
    ):

        self.bands = bands

        self.bandwidth = bandwidth

        self.dwell_controller = DwellController(
            minimum_dwell=minimum_dwell,
            maximum_dwell=maximum_dwell
        )

        self.switching_time = switching_time

        self.current_band = None

        self.current_time = 0.0

        self.observation_history = []

    # --------------------------------------------------
    # BAND SELECTION
    # --------------------------------------------------

    def select_band(self, band_id: int):

        band = self._get_band(band_id)

        if band is None:
            raise ValueError(
                f"Band {band_id} does not exist."
            )

        switching_delay = 0.0

        if (
            self.current_band is not None
            and self.current_band["id"] != band_id
        ):
            switching_delay = self.switching_time

        self.current_time += switching_delay

        self.current_band = band

        return band

    # --------------------------------------------------
    # SCAN
    # --------------------------------------------------

    def scan(
        self,
        band_id: int,
        dwell_time: float,
        rf_activity: List[Dict[str, Any]]
    ):

        band = self.select_band(band_id)

        dwell_time = self.dwell_controller.validate(
            dwell_time
        )

        receiver_bandwidth = ReceiverBandwidth(
            center_frequency=band["center_frequency"],
            bandwidth=self.bandwidth
        )

        start_time = self.current_time

        end_time = start_time + dwell_time

        detected = []

        for signal in rf_activity:

            signal_time = signal["time"]
            signal_frequency = signal["frequency"]

            time_match = (
                start_time
                <= signal_time
                <= end_time
            )

            frequency_match = (
                receiver_bandwidth.contains(
                    signal_frequency
                )
            )

            if time_match and frequency_match:
                detected.append(signal)

        hit = len(detected) > 0

        observed_frequency = None
        signal_strength = None

        if hit:

            observed_frequency = detected[0]["frequency"]

            signal_strength = detected[0].get(
                "amplitude"
            )

        observation = Observation(

            time=start_time,

            band_id=band_id,

            center_frequency=band["center_frequency"],

            dwell_time=dwell_time,

            hit=hit,

            observed_frequency=observed_frequency,

            pulse_count=len(detected),

            signal_strength=signal_strength,

            observation_status=(
                "HIT" if hit else "MISS"
            )
        )

        self.current_time = end_time

        self.observation_history.append(
            observation
        )

        return observation

    # --------------------------------------------------
    # INTERNAL
    # --------------------------------------------------

    def _get_band(self, band_id):

        for band in self.bands:

            if band["id"] == band_id:
                return band

        return None

    # --------------------------------------------------
    # RESET
    # --------------------------------------------------

    def reset(self):

        self.current_band = None

        self.current_time = 0.0

        self.observation_history = []

    # --------------------------------------------------
    # HISTORY
    # --------------------------------------------------

    def get_history(self):

        return [
            observation.to_dict()
            for observation
            in self.observation_history
        ]