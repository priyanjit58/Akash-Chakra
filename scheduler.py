# baps/scheduler.py

import math


class BAPSScheduler:

    def __init__(
        self,
        belief_engine,
        uncertainty_estimator,
        information_gain_estimator,

        wp=0.40,
        wu=0.20,
        wr=0.20,
        wi=0.15,
        ws=0.05
    ):

        self.belief_engine = belief_engine

        self.uncertainty_estimator = (
            uncertainty_estimator
        )

        self.information_gain_estimator = (
            information_gain_estimator
        )

        self.wp = wp
        self.wu = wu
        self.wr = wr
        self.wi = wi
        self.ws = ws

    # ------------------------------------------------
    # REVISIT URGENCY
    # ------------------------------------------------

    def revisit_urgency(
        self,
        belief,
        current_time
    ):

        if belief.is_unknown():

            return 1.0

        elapsed = (
            current_time
            - belief.last_observed_time
        )

        # Saturating urgency curve
        urgency = 1.0 - math.exp(
            -elapsed / 10.0
        )

        return max(
            0.0,
            min(1.0, urgency)
        )

    # ------------------------------------------------
    # SWITCHING COST
    # ------------------------------------------------

    def switching_cost(
        self,
        band_id,
        current_band
    ):

        if current_band is None:

            return 0.0

        if band_id == current_band:

            return 0.0

        return 1.0

    # ------------------------------------------------
    # SCORE
    # ------------------------------------------------

    def score_band(
        self,
        band_id,
        current_band,
        current_time
    ):

        belief = self.belief_engine.get(
            band_id
        )

        probability = (
            belief.probability()
        )

        uncertainty = (
            self.uncertainty_estimator
            .calculate(belief)
        )

        revisit = (
            self.revisit_urgency(
                belief,
                current_time
            )
        )

        information_gain = (
            self.information_gain_estimator
            .calculate(belief)
        )

        switching = (
            self.switching_cost(
                band_id,
                current_band
            )
        )

        score = (

            self.wp * probability

            + self.wu * uncertainty

            + self.wr * revisit

            + self.wi * information_gain

            - self.ws * switching
        )

        return {

            "band_id": band_id,

            "probability":
                probability,

            "uncertainty":
                uncertainty,

            "revisit_urgency":
                revisit,

            "information_gain":
                information_gain,

            "switching_cost":
                switching,

            "score":
                score
        }

    # ------------------------------------------------
    # SELECT NEXT BAND
    # ------------------------------------------------

    def select_band(
        self,
        current_band,
        current_time
    ):

        scores = []

        for band_id in (
            self.belief_engine
            .get_all()
            .keys()
        ):

            result = self.score_band(

                band_id=band_id,

                current_band=current_band,

                current_time=current_time
            )

            scores.append(result)

        scores.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return scores[0], scores