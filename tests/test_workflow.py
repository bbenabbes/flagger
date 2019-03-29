import pytest

from flagger.steps.dummy_step import DummyStep
from flagger.workflow import Workflow


@pytest.mark.unit
class WorkflowTest:

    @classmethod
    def setup(cls):
        cls.workflow = Workflow(id='workflow')
        cls.step1 = DummyStep('step1')
        cls.step2 = DummyStep('step2')
        cls.step3 = DummyStep('step3')
        cls.step4 = DummyStep('step4')
        cls.workflow.add_nodes_from([cls.step1, cls.step2, cls.step3, cls.step4])

    @classmethod
    def teardown(cls):
        del cls.workflow
        del cls.step1
        del cls.step2
        del cls.step3
        del cls.step4

    def test_get_roots(self):
        roots = self.workflow.get_roots()
        expected = [
            self.step1,
            self.step2,
            self.step3,
            self.step4,
        ]
        assert expected == roots

    def test_is_ready(self):
        self.workflow.add_edges_from([
            (self.step1, self.step4),
            (self.step2, self.step4),
            (self.step3, self.step4),
        ])
        assert self.workflow.is_ready(self.step1) is True
        assert self.workflow.is_ready(self.step2) is True
        assert self.workflow.is_ready(self.step3) is True

    def test_get_step_by_returns_none(self):
        step = self.workflow.get_step_by('step1-id')
        assert None is step

    def test_get_step_by(self):
        id = 'step1-id'
        self.step1.id = id
        step = self.workflow.get_step_by(id)
        assert 'step1-id' == step.id
        assert 'step1' == step.name
