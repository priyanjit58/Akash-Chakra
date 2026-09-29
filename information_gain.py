# baps/information_gain.py

class InformationGainEstimator:

    def __init__(self, uncertainty_estimator):

        self.uncertainty_estimator = (
            uncertainty_estimator
        )

    def calculate(self, belief):

        uncertainty = (
            self.uncertainty_estimator
            .calculate(belief)
        )

        # Unknown bands receive maximum
        # information value.
        if belief.is_unknown():

            return 1.0

        return uncertainty

    def calculate_all(self, belief_engine):

        result = {}

        for band_id, belief in (
            belief_engine.get_all().items()
        ):

            result[band_id] = (
                self.calculate(belief)
            )

        return result