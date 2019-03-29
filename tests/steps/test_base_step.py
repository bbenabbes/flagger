import pytest

from flagger.steps.base_step import BaseStep
from flagger.workflow import Workflow


@pytest.mark.unit
class BaseStepTest:

    @classmethod
    def setup(cls):
        cls.workflow = Workflow(id='w')
        cls.step = BaseStep(name='step', id='foo-id')

    @classmethod
    def teardown(cls):
        del cls.workflow
        del cls.step

    def test_create_step(self):
        assert 'foo-id' == self.step.id

    def test_run_step(self):
        with pytest.raises(NotImplementedError):
            self.step.run()
