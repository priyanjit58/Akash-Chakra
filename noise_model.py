import random


class NoiseModel:

    def __init__(
        self,
        false_alarm_probability=0.0,
        seed=42
    ):

        self.false_alarm_probability = (
            false_alarm_probability
        )

        random.seed(seed)

    def generate_false_alarm(self):

        return (
            random.random()
            < self.false_alarm_probability
        )