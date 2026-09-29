# main_stage3.py

from environment.rf_environment import (
    RFEnvironment
)

from environment.frequency_model import (
    create_frequency_bands
)

from receiver.esm_receiver import (
    VirtualESMReceiver
)

from baps.belief import (
    BayesianBeliefEngine
)

from baps.uncertainty import (
    UncertaintyEstimator
)

from baps.information_gain import (
    InformationGainEstimator
)

from baps.scheduler import (
    BAPSScheduler
)

from baselines.sequential_scan import (
    SequentialScanner
)

from baselines.random_scan import (
    RandomScanner
)

from baselines.greedy_scan import (
    GreedyScanner
)


def run_policy(
    policy_name,
    receiver,
    activity,
    bands,
    number_of_cycles=50
):

    band_ids = [
        band["id"]
        for band in bands
    ]

    # --------------------------------------------
    # BAPS belief system
    # --------------------------------------------

    belief_engine = BayesianBeliefEngine(
        band_ids
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

    # --------------------------------------------
    # Baseline
    # --------------------------------------------

    if policy_name == "Sequential":

        policy = SequentialScanner(
            band_ids
        )

    elif policy_name == "Random":

        policy = RandomScanner(
            band_ids,
            seed=42
        )

    elif policy_name == "Greedy":

        policy = GreedyScanner(
            belief_engine
        )

    elif policy_name == "BAPS":

        policy = None

    else:

        raise ValueError(
            f"Unknown policy: {policy_name}"
        )

    # --------------------------------------------
    # Statistics
    # --------------------------------------------

    hits = 0

    misses = 0

    history = []

    # --------------------------------------------
    # CLOSED LOOP
    # --------------------------------------------

    for cycle in range(
        number_of_cycles
    ):

        current_band = (
            receiver.current_band
        )

        current_band_id = None

        if current_band is not None:

            current_band_id = (
                current_band["id"]
            )

        current_time = (
            receiver.current_time
        )

        # ----------------------------------------
        # SELECT BAND
        # ----------------------------------------

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
                    )
            }

        # ----------------------------------------
        # SCAN
        # ----------------------------------------

        observation = receiver.scan(

            band_id=selected_band,

            dwell_time=2.0,

            rf_activity=activity
        )

        # ----------------------------------------
        # UPDATE BELIEF
        # ----------------------------------------

        belief_engine.update(
            observation
        )

        # ----------------------------------------
        # METRICS
        # ----------------------------------------

        if observation.hit:

            hits += 1

        else:

            misses += 1

        history.append({

            "cycle":
                cycle,

            "policy":
                policy_name,

            "band":
                selected_band,

            "hit":
                observation.hit,

            "time":
                observation.time,

            "probability":
                belief_engine
                .probability(
                    selected_band
                )
        })

        # ----------------------------------------
        # LOG
        # ----------------------------------------

        print(

            f"[{policy_name:9}] "

            f"Cycle={cycle:02d} "

            f"Band={selected_band:02d} "

            f"{'HIT ' if observation.hit else 'MISS'} "
        )

        if (
            policy_name == "BAPS"
        ):

            print(

                f"  P="
                f"{decision['probability']:.3f} "

                f"U="
                f"{decision['uncertainty']:.3f} "

                f"R="
                f"{decision['revisit_urgency']:.3f} "

                f"I="
                f"{decision['information_gain']:.3f} "

                f"S="
                f"{decision['score']:.3f}"
            )

    return {

        "policy":
            policy_name,

        "hits":
            hits,

        "misses":
            misses,

        "history":
            history,

        "beliefs":
            belief_engine.snapshot()
    }


def main():

    print("=" * 70)

    print(
        "AKASH CHAKRA"
    )

    print(
        "STAGE 3 — BAYESIAN BAPS ENGINE"
    )

    print("=" * 70)

    # ============================================
    # RF ENVIRONMENT
    # ============================================

    environment = RFEnvironment(
        seed=42
    )

    activity = (
        environment
        .generate_demo_environment()
    )

    # ============================================
    # FREQUENCY BANDS
    # ============================================

    bands = create_frequency_bands(

        start_frequency=50,

        end_frequency=400,

        number_of_bands=36
    )

    # ============================================
    # RUN POLICIES
    # ============================================

    policies = [

        "BAPS",

        "Sequential",

        "Random",

        "Greedy"
    ]

    results = {}

    for policy_name in policies:

        print(
            "\n" + "=" * 70
        )

        print(
            f"RUNNING {policy_name.upper()}"
        )

        print(
            "=" * 70
        )

        receiver = VirtualESMReceiver(

            bands=bands,

            bandwidth=10.0,

            minimum_dwell=1.0,

            maximum_dwell=5.0,

            switching_time=0.5
        )

        results[policy_name] = (
            run_policy(

                policy_name=

                    policy_name,

                receiver=

                    receiver,

                activity=

                    activity,

                bands=

                    bands,

                number_of_cycles=

                    50
            )
        )

    # ============================================
    # SUMMARY
    # ============================================

    print(
        "\n\n"
        + "=" * 70
    )

    print(
        "STAGE 3 SUMMARY"
    )

    print(
        "=" * 70
    )

    for policy_name, result in (
        results.items()
    ):

        total = (
            result["hits"]
            + result["misses"]
        )

        hit_rate = (

            result["hits"]
            / total
            if total > 0
            else 0
        )

        print(

            f"{policy_name:10} | "

            f"HIT = "
            f"{result['hits']:3d} | "

            f"MISS = "
            f"{result['misses']:3d} | "

            f"Hit Rate = "
            f"{hit_rate:.3f}"
        )


if __name__ == "__main__":

    main()