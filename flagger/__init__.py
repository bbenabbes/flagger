from pkg_resources import DistributionNotFound, get_distribution

from flagger.steps.base_step import BaseStep
from flagger.steps.dummy_step import DummyStep
from flagger.workers.celery_worker import play_workflow
from flagger.workflow import Workflow

__all__ = [
    '__version__',
    'BaseStep',
    'DummyStep',
    'play_workflow',
    'Workflow',
]


def _get_version():
    try:
        return get_distribution('flagger').version
    except DistributionNotFound:
        return 'dev'


__version__ = _get_version()
