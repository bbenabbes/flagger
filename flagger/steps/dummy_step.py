from flagger.steps.base_step import BaseStep


class DummyStep(BaseStep):
    """
    Step that does literally nothing.
    """

    def run(self):
        pass
