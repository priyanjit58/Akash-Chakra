# baps/uncertainty.py

class UncertaintyEstimator:

    def calculate(self, belief):

        alpha = belief.alpha
        beta = belief.beta

        total = alpha + beta

        variance = (
            alpha * beta
        ) / (
            total ** 2
            * (total + 1)
        )

        # Maximum Beta variance approaches 0.25
        normalized = 4.0 * variance

        return max(
            0.0,
            min(1.0, normalized)
        )

    def calculate_all(self, belief_engine):

        result = {}

        for band_id, belief in (
            belief_engine.get_all().items()
        ):

            result[band_id] = (
                self.calculate(belief)
            )

        return result