# baps/belief.py

from dataclasses import dataclass


@dataclass
class BandBelief:

    band_id: int

    alpha: float = 1.0
    beta: float = 1.0

    observations: int = 0
    hits: int = 0
    misses: int = 0

    last_observed_time: float = -1.0

    def probability(self):

        return self.alpha / (
            self.alpha + self.beta
        )

    def update(
        self,
        hit: bool,
        time: float
    ):

        if hit:

            self.alpha += 1

            self.hits += 1

        else:

            self.beta += 1

            self.misses += 1

        self.observations += 1

        self.last_observed_time = time

    def is_unknown(self):

        return self.observations == 0

    def to_dict(self):

        return {

            "band_id": self.band_id,

            "alpha": self.alpha,

            "beta": self.beta,

            "probability":
                self.probability(),

            "observations":
                self.observations,

            "hits":
                self.hits,

            "misses":
                self.misses,

            "last_observed_time":
                self.last_observed_time,

            "unknown":
                self.is_unknown()
        }


class BayesianBeliefEngine:

    def __init__(self, band_ids):

        self.beliefs = {

            band_id:
            BandBelief(
                band_id=band_id
            )

            for band_id in band_ids
        }

    def update(
        self,
        observation
    ):

        band_id = observation.band_id

        if band_id not in self.beliefs:

            raise ValueError(
                f"Unknown band: {band_id}"
            )

        self.beliefs[band_id].update(

            hit=observation.hit,

            time=observation.time
        )

    def probability(self, band_id):

        return self.beliefs[
            band_id
        ].probability()

    def get(self, band_id):

        return self.beliefs[band_id]

    def get_all(self):

        return self.beliefs

    def snapshot(self):

        return {

            band_id:
            belief.to_dict()

            for band_id, belief
            in self.beliefs.items()
        }
        