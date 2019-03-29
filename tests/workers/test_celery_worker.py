from unittest.mock import patch

import pytest

from flagger.steps.dummy_step import DummyStep
from flagger.workers.celery_worker import play_workflow
from flagger.workflow import Workflow


@pytest.mark.unit
class CeleryWorkerTest:

    @patch('flagger.workers.celery_worker.uuid4')
    @patch('flagger.workers.celery_worker.play_workflow.apply_async')
    def test_play_workflow(self, apply_async, uuid4):
        workflow = Workflow(id='w')
        step = DummyStep(name='step', id='id')
        workflow.add_node(step)
        uuid4.return_value = step.id
        play_workflow(workflow=workflow)  # pylint: disable=no-value-for-parameter
        apply_async.assert_called_once_with(args=(workflow, 'id'), task_id='id')
