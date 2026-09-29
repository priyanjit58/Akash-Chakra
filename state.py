from engine.live_engine import LiveBAPSEngine


engine = LiveBAPSEngine(
    number_of_bands=36,
    seed=42
)

connected_clients = set()