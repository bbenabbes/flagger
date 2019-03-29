from celery.result import AsyncResult
from networkx import DiGraph

from flagger.state import State


class Workflow(DiGraph):

    def __init__(self, id):
        self.id = id
        super().__init__()

    def get_roots(self):
        res = []
        for node in list(self.nodes):
            if len(list(self.predecessors(node))) == 0:
                res.append(node)
        return res

    def is_ready(self, step):
        return all(AsyncResult(predecessor.id).state in [State.SUCCESS,
                                                         State.SKIPPED]
                   for predecessor in self.predecessors(step))

    def get_step_by(self, id):
        for node in list(self.nodes):
            if node.id == id:
                return node

    def __repr__(self):
        return f'<Workflow: {self.id}>'
