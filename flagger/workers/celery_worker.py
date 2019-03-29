import os
from uuid import uuid4

from celery import Celery
from celery.exceptions import TaskRevokedError
from celery.states import SUCCESS
from kombu.serialization import register

from flagger.json import dumps, loads

register('flagger-json', dumps, loads, content_type='application/x-flagger-json',
         content_encoding='utf-8')
app = Celery('flagger.workers.workers')
config = {
    'accept_content': ['flagger-json'],
    'broker_url': os.environ.get('broker_url'),
    'result_backend': os.environ.get('result_backend', 'db+sqlite:///../flagger.sqlite'),
    'result_serializer': 'flagger-json',
    'task_serializer': 'flagger-json',
    # 'worker_concurrency': os.environ.get('worker_concurrency', 16),
}
app.config_from_object(config)


@app.task(bind=True)
def play_workflow(self, workflow, step_id=None):
    result = None
    if step_id is not None:
        step = workflow.get_step_by(id=step_id)
        if not workflow.is_ready(step=step):
            raise TaskRevokedError('Predecessors are not yet finished.')
        result = step.run()
        self.update_state(state=SUCCESS)
        next_steps = list(workflow.successors(step))
    else:
        next_steps = workflow.get_roots()
    for step in next_steps:
        step.id = str(uuid4())
        play_workflow.apply_async(args=(workflow, step.id,), task_id=step.id)
    return result
