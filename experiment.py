import json
import os
import csv

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

from evaluation.metrics import MetricsCalculator


class ExperimentRunner:

    def __init__(
        self,
        number_of_bands=36,
        number_of_cycles=100,
        seed=42
    ):

        self.number_of_bands = (
            number_of_bands
        )

        self.number_of_cycles = (
            number_of_cycles
        )

        self.seed = seed

    # ==================================================
    # CREATE ENVIRONMENT
    # ==================================================

    def create_environment(self):

        environment = RFEnvironment(
            seed=self.seed
        )

        activity = (
            environment
            .generate_demo_environment()
        )

        return activity

    # ==================================================
    # CREATE BANDS
    # ==================================================

    def create_bands(self):

        return create_frequency_bands(

            start_frequency=50,

            end_frequency=400,

            number_of_bands=
                self.number_of_bands
        )

    # ==================================================
    # CREATE POLICY
    # ==================================================

    def create_policy(
        self,
        policy_name,
        band_ids
    ):

        if policy_name == "Sequential":

            return SequentialScanner(
                band_ids
            )

        if policy_name == "Random":

            return RandomScanner(
                band_ids,
                seed=self.seed
            )

        return None

    # ==================================================
    # RUN POLICY
    # ==================================================

    def run_policy(
        self,
        policy_name,
        activity,
        bands
    ):

        band_ids = [
            band["id"]
            for band in bands
        ]

        receiver = VirtualESMReceiver(

            bands=bands,

            bandwidth=10.0,

            minimum_dwell=1.0,

            maximum_dwell=5.0,

            switching_time=0.5
        )

        # ----------------------------------------------
        # Belief system
        # ----------------------------------------------

        belief_engine = (
            BayesianBeliefEngine(
                band_ids
            )
        )

        uncertainty_estimator = (
            UncertaintyEstimator()
        )

        information_gain_estimator = (
            InformationGainEstimator(
                uncertainty_estimator
            )
        )

        scheduler = BAPSScheduler(

            belief_engine=

                belief_engine,

            uncertainty_estimator=

                uncertainty_estimator,

            information_gain_estimator=

                information_gain_estimator
        )

        # ----------------------------------------------
        # Baseline policy
        # ----------------------------------------------

        policy = self.create_policy(

            policy_name,

            band_ids
        )

        if policy_name == "Greedy":

            policy = GreedyScanner(
                belief_engine
            )

        # ----------------------------------------------
        # Run
        # ----------------------------------------------

        decision_log = []

        for cycle in range(
            self.number_of_cycles
        ):

            current_band = (
                receiver.current_band
            )

            current_band_id = None

            if current_band:

                current_band_id = (
                    current_band["id"]
                )

            current_time = (
                receiver.current_time
            )

            # ------------------------------------------
            # SELECT BAND
            # ------------------------------------------

            if policy_name == "BAPS":

                decision, all_scores = (
                    scheduler.select_band(

                        current_band=
                            current_band_id,

                        current_time=
                            current_time
                    )
                )

                selected_band = (
                    decision["band_id"]
                )

            else:

                selected_band = (
                    policy.select_band()
                )

                decision = {

                    "band_id":
                        selected_band,

                    "probability":
                        belief_engine
                        .probability(
                            selected_band
                        ),

                    "uncertainty":
                        None,

                    "revisit_urgency":
                        None,

                    "information_gain":
                        None,

                    "switching_cost":
                        None,

                    "score":
                        None
                }

            # ------------------------------------------
            # SCAN
            # ------------------------------------------

            observation = receiver.scan(

                band_id=selected_band,

                dwell_time=2.0,

                rf_activity=activity
            )

            # ------------------------------------------
            # UPDATE BELIEF
            # ------------------------------------------

            belief_engine.update(
                observation
            )

            # ------------------------------------------
            # LOG
            # ------------------------------------------

            decision_log.append({

                "cycle":
                    cycle,

                "band":
                    selected_band,

                "time":
                    observation.time,

                "hit":
                    observation.hit,

                "pulse_count":
                    observation.pulse_count,

                "probability":
                    decision["probability"],

                "uncertainty":
                    decision["uncertainty"],

                "revisit_urgency":
                    decision["revisit_urgency"],

                "information_gain":
                    decision["information_gain"],

                "switching_cost":
                    decision["switching_cost"],

                "score":
                    decision["score"]
            })

        # ----------------------------------------------
        # METRICS
        # ----------------------------------------------

        observations = (
            receiver.observation_history
        )

        metrics = MetricsCalculator(

            observations=
                observations,

            activity=
                activity
        )

        metrics_result = (
            metrics.calculate_all()
        )

        # ----------------------------------------------
        # RESULT
        # ----------------------------------------------

        return {

            "policy":
                policy_name,

            "seed":
                self.seed,

            "number_of_bands":
                self.number_of_bands,

            "number_of_cycles":
                self.number_of_cycles,

            "metrics":
                metrics_result,

            "decisions":
                decision_log,

            "beliefs":
                belief_engine.snapshot()
        }

    # ==================================================
    # RUN COMPLETE EXPERIMENT
    # ==================================================

    def run(self):

        activity = (
            self.create_environment()
        )

        bands = self.create_bands()

        policies = [

            "BAPS",

            "Sequential",

            "Random",

            "Greedy"
        ]

        results = []

        for policy in policies:

            print(
                f"Running {policy} "
                f"(seed={self.seed})..."
            )

            result = self.run_policy(

                policy_name=
                    policy,

                activity=
                    activity,

                bands=
                    bands
            )

            results.append(result)

        return results

    # ==================================================
    # SAVE JSON
    # ==================================================

    @staticmethod
    def save_json(
        results,
        filepath
    ):

        os.makedirs(

            os.path.dirname(filepath),

            exist_ok=True
        )

        with open(
            filepath,
            "w"
        ) as file:

            json.dump(

                results,

                file,

                indent=2,

                allow_nan=True
            )

    # ==================================================
    # SAVE CSV
    # ==================================================

    @staticmethod
    def save_summary_csv(
        results,
        filepath
    ):

        os.makedirs(

            os.path.dirname(filepath),

            exist_ok=True
        )

        rows = []

        for result in results:

            row = {

                "policy":
                    result["policy"],

                "seed":
                    result["seed"],

                **result["metrics"]
            }

            rows.append(row)

        fieldnames = list(
            rows[0].keys()
        )

        with open(
            filepath,
            "w",
            newline=""
        ) as file:

            writer = csv.DictWriter(

                file,

                fieldnames=
                    fieldnames
            )

            writer.writeheader()

            writer.writerows(rows)