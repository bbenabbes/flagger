# Flagger
Workflow as code in Celery.

## Development environment
Install flagger requirements (virtual env recommended):

    $ pip install -r requirements.txt

## How to run tests
    $ pytest -m unit

## Simple example

```python
>>> from flagger import Workflow
>>> workflow = Workflow('workflow')
>>>
>>> from flagger import DummyStep
>>> step1 = DummyStep('step1')
>>> step2 = DummyStep('step2')
>>> step3 = DummyStep('step3')
>>> step4 = DummyStep('step4')
>>> step5 = DummyStep('step5')
>>>
>>> workflow.add_edges_from(
...     [
...         (step1, step2),
...         (step1, step3),
...         (step2, step4),
...         (step3, step4),
...         (step4, step5),
...     ]
... )
>>> 
>>> from flagger import play_workflow
>>> play_workflow.apply_async(
...     args=(workflow,)
... )
```
