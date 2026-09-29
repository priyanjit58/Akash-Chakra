# baselines/greedy_scan.py


class GreedyScanner:

    def __init__(
        self,
        belief_engine
    ):

        self.belief_engine = (
            belief_engine
        )

    def select_band(self):

        beliefs = (
            self.belief_engine
            .get_all()
        )

        best_band = max(

            beliefs.keys(),

            key=lambda band_id:
                beliefs[
                    band_id
                ].probability()
        )

        return best_band

    def reset(self):

        pass