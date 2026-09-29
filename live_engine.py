import asyncio
import random
from datetime import datetime

from environment.rf_environment import RFEnvironment
from environment.frequency_model import create_frequency_bands

from receiver.esm_receiver import VirtualESMReceiver

from baps.belief import BayesianBeliefEngine
from baps.uncertainty import UncertaintyEstimator
from baps.information_gain import InformationGainEstimator
from baps.scheduler import BAPSScheduler

from baselines.sequential_scan import SequentialScanner
from baselines.random_scan import RandomScanner
from baselines.greedy_scan import GreedyScanner


class LiveBAPSEngine:

    def __init__(
        self,
        number_of_bands=36,
        seed=42
    ):

        self.number_of_bands = number_of_bands
        self.seed = seed

        self.running = False

        self.cycle = 0

        self.policy = "BAPS"

        self.scenario = "Demo"

        self.dwell_time = 2.0

        self.speed = 1.0

        self.event_log = []

        self.reset()

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.environment = RFEnvironment(
            seed=self.seed
        )

        self.activity = (
            self.environment
            .generate_demo_environment()
        )

        self.bands = create_frequency_bands(

            start_frequency=50,

            end_frequency=400,

            number_of_bands=self.number_of_bands
        )

        band_ids = [
            band["id"]
            for band in self.bands
        ]

        self.receiver = VirtualESMReceiver(

            bands=self.bands,

            bandwidth=10.0,

            minimum_dwell=1.0,

            maximum_dwell=5.0,

            switching_time=0.5
        )

        self.belief_engine = (
            BayesianBeliefEngine(
                band_ids
            )
        )

        self.uncertainty_estimator = (
            UncertaintyEstimator()
        )

        self.information_gain_estimator = (
            InformationGainEstimator(
                self.uncertainty_estimator
            )
        )

        self.scheduler = BAPSScheduler(

            belief_engine=
                self.belief_engine,

            uncertainty_estimator=
                self.uncertainty_estimator,

            information_gain_estimator=
                self.information_gain_estimator
        )

        self.sequential = SequentialScanner(
            band_ids
        )

        self.random = RandomScanner(
            band_ids,
            seed=self.seed
        )

        self.greedy = GreedyScanner(
            self.belief_engine
        )

        self.cycle = 0

        self.event_log = []

    # ==================================================
    # CHANGE POLICY
    # ==================================================

    def set_policy(self, policy):

        allowed = {
            "BAPS",
            "Sequential",
            "Random",
            "Greedy"
        }

        if policy not in allowed:

            raise ValueError(
                f"Unsupported policy: {policy}"
            )

        self.policy = policy

    # ==================================================
    # SELECT BAND
    # ==================================================

    def select_band(self):

        current_band = (
            self.receiver.current_band
        )

        current_band_id = None

        if current_band:

            current_band_id = (
                current_band["id"]
            )

        current_time = (
            self.receiver.current_time
        )

        if self.policy == "BAPS":

            decision, scores = (
                self.scheduler.select_band(

                    current_band=
                        current_band_id,

                    current_time=
                        current_time
                )
            )

            return (
                decision["band_id"],
                decision,
                scores
            )

        if self.policy == "Sequential":

            band = (
                self.sequential.select_band()
            )

        elif self.policy == "Random":

            band = (
                self.random.select_band()
            )

        elif self.policy == "Greedy":

            band = (
                self.greedy.select_band()
            )

        else:

            band = 0

        belief = (
            self.belief_engine.get(
                band
            )
        )

        decision = {

            "band_id": band,

            "probability":
                belief.probability(),

            "uncertainty":
                self.uncertainty_estimator
                .calculate(belief),

            "revisit_urgency": 0.0,

            "information_gain":
                self.information_gain_estimator
                .calculate(belief),

            "switching_cost": 0.0,

            "score": 0.0
        }

        return band, decision, []

    # ==================================================
    # RUN ONE CYCLE
    # ==================================================

    def run_cycle(self):

        band_id, decision, all_scores = (
            self.select_band()
        )

        observation = self.receiver.scan(

            band_id=band_id,

            dwell_time=self.dwell_time,

            rf_activity=self.activity
        )

        self.belief_engine.update(
            observation
        )

        self.cycle += 1

        event = {

            "cycle":
                self.cycle,

            "timestamp":
                datetime.utcnow().isoformat(),

            "band_id":
                band_id,

            "frequency":
                observation.center_frequency,

            "hit":
                observation.hit,

            "pulse_count":
                observation.pulse_count,

            "dwell_time":
                observation.dwell_time,

            "probability":
                decision.get(
                    "probability",
                    0
                ),

            "uncertainty":
                decision.get(
                    "uncertainty",
                    0
                ),

            "revisit_urgency":
                decision.get(
                    "revisit_urgency",
                    0
                ),

            "information_gain":
                decision.get(
                    "information_gain",
                    0
                ),

            "switching_cost":
                decision.get(
                    "switching_cost",
                    0
                ),

            "score":
                decision.get(
                    "score",
                    0
                )
        }

        self.event_log.insert(
            0,
            event
        )

        self.event_log = (
            self.event_log[:100]
        )

        return event

    # ==================================================
    # DASHBOARD STATE
    # ==================================================

    def get_state(self):

        beliefs = (
            self.belief_engine.snapshot()
        )

        current_band = (
            self.receiver.current_band
        )

        current_band_id = (
            current_band["id"]
            if current_band
            else None
        )

        # Current BAPS ranking
        decision, scores = (
            self.scheduler.select_band(

                current_band=
                    current_band_id,

                current_time=
                    self.receiver.current_time
            )
        )

        # ----------------------------------------------
        # Spectrum activity
        # ----------------------------------------------

        spectrum = []

        for band in self.bands:

            band_id = band["id"]

            belief = beliefs[
                band_id
            ]

            spectrum.append({

                "band_id":
                    band_id,

                "frequency":
                    band["center_frequency"],

                "probability":
                    belief["probability"],

                "uncertainty":
                    self.uncertainty_estimator
                    .calculate(
                        self.belief_engine
                        .get(band_id)
                    ),

                "observations":
                    belief["observations"],

                "hits":
                    belief["hits"],

                "misses":
                    belief["misses"]
            })

        # ----------------------------------------------
        # Metrics
        # ----------------------------------------------

        observations = (
            self.receiver.observation_history
        )

        total_scans = len(
            observations
        )

        hits = sum(
            1
            for obs in observations
            if obs.hit
        )

        pi = (
            hits / total_scans
            if total_scans
            else 0
        )

        signal_events = sum(
            obs.pulse_count
            for obs in observations
        )

        total_activity = len(
            self.activity
        )

        pd = min(
            1.0,
            signal_events / total_activity
        ) if total_activity else 0

        return {

            "system": {

                "name":
                    "AKASH CHAKRA",

                "engine":
                    "BAPS",

                "running":
                    self.running,

                "policy":
                    self.policy,

                "scenario":
                    self.scenario,

                "cycle":
                    self.cycle,

                "simulation_time":
                    self.receiver.current_time
            },

            "current_scan": {

                "band_id":
                    current_band_id,

                "frequency":
                    (
                        current_band["center_frequency"]
                        if current_band
                        else None
                    ),

                "dwell":
                    self.dwell_time
            },

            "decision":
                decision,

            "spectrum":
                spectrum,

            "metrics": {

                "Pd":
                    pd,

                "PI":
                    pi,

                "AIT":
                    self.calculate_ait(),

                "scan_cycles":
                    total_scans,

                "hits":
                    hits,

                "misses":
                    total_scans - hits
            },

            "beliefs":
                beliefs,

            "ranking":
                scores[:10],

            "event_log":
                self.event_log
        }

    # ==================================================
    # AIT
    # ==================================================

    def calculate_ait(self):

        observations = (
            self.receiver.observation_history
        )

        hit_times = [

            obs.time
            for obs in observations
            if obs.hit
        ]

        if not hit_times:

            return None

        start = observations[0].time

        return min(hit_times) - start

    # ==================================================
    # ASYNC LOOP
    # ==================================================

    async def run_loop(
        self,
        broadcaster
    ):

        while True:

            if self.running:

                try:

                    self.run_cycle()

                    await broadcaster(
                        self.get_state()
                    )

                except Exception as error:

                    print(
                        "Engine error:",
                        error
                    )

            await asyncio.sleep(
                max(
                    0.1,
                    1.0 / self.speed
                )
            )