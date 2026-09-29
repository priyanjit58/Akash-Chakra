class Emitter:

    def __init__(
        self,
        emitter_id,
        frequency,
        behavior="fixed"
    ):

        self.emitter_id = emitter_id

        self.frequency = frequency

        self.behavior = behavior

    def describe(self):

        return {

            "emitter_id": self.emitter_id,

            "frequency": self.frequency,

            "behavior": self.behavior
        }