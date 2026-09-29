import numpy as np


class MetricsCalculator:

    def __init__(self, observations, activity):

        self.observations = observations
        self.activity = activity

    # --------------------------------------------------
    # NUMBER OF SIGNAL EVENTS
    # --------------------------------------------------

    def total_signal_events(self):

        return len(self.activity)

    # --------------------------------------------------
    # DETECTED SIGNAL EVENTS
    # --------------------------------------------------

    def detected_signal_events(self):

        detected = 0

        for observation in self.observations:

            if observation.hit:

                detected += observation.pulse_count

        return detected

    # --------------------------------------------------
    # PROBABILITY OF DETECTION
    # --------------------------------------------------

    def probability_of_detection(self):

        total = self.total_signal_events()

        if total == 0:
            return 0.0

        detected = self.detected_signal_events()

        return min(
            1.0,
            detected / total
        )

    # --------------------------------------------------
    # PROBABILITY OF INTERCEPT
    # --------------------------------------------------

    def probability_of_intercept(self):

        if not self.observations:

            return 0.0

        successful_scans = sum(

            1
            for obs in self.observations
            if obs.hit
        )

        return (
            successful_scans
            / len(self.observations)
        )

    # --------------------------------------------------
    # SCAN EFFICIENCY
    # --------------------------------------------------

    def scan_efficiency(self):

        if not self.observations:

            return 0.0

        return (
            self.detected_signal_events()
            / len(self.observations)
        )

    # --------------------------------------------------
    # FALSE ALARM RATE
    # --------------------------------------------------

    def false_alarm_rate(self):

        false_alarms = 0

        for observation in self.observations:

            # A false alarm is an observation
            # reported as HIT without an actual
            # activity pulse.
            if (
                observation.hit
                and observation.pulse_count == 0
            ):

                false_alarms += 1

        if not self.observations:

            return 0.0

        return (
            false_alarms
            / len(self.observations)
        )

    # --------------------------------------------------
    # AVERAGE INTERCEPT TIME
    # --------------------------------------------------

    def average_intercept_time(self):

        if not self.observations:

            return np.nan

        first_time = (
            self.observations[0].time
        )

        hit_times = [

            obs.time
            for obs in self.observations
            if obs.hit
        ]

        if not hit_times:

            return np.nan

        return min(hit_times) - first_time

    # --------------------------------------------------
    # CUMULATIVE REWARD
    # --------------------------------------------------

    def cumulative_reward(
        self,
        hit_reward=1.0,
        miss_penalty=-0.1,
        switching_penalty=-0.05
    ):

        reward = 0.0

        previous_band = None

        for obs in self.observations:

            if obs.hit:

                reward += hit_reward

            else:

                reward += miss_penalty

            if (
                previous_band is not None
                and previous_band != obs.band_id
            ):

                reward += switching_penalty

            previous_band = obs.band_id

        return reward

    # --------------------------------------------------
    # ALL METRICS
    # --------------------------------------------------

    def calculate_all(self):

        return {

            "total_scans":
                len(self.observations),

            "total_signal_events":
                self.total_signal_events(),

            "detected_signal_events":
                self.detected_signal_events(),

            "Pd":
                self.probability_of_detection(),

            "PI":
                self.probability_of_intercept(),

            "AIT":
                self.average_intercept_time(),

            "false_alarm_rate":
                self.false_alarm_rate(),

            "scan_efficiency":
                self.scan_efficiency(),

            "cumulative_reward":
                self.cumulative_reward()
        }