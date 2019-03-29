import json
from itertools import chain

from flagger.plugins_manager import steps
from flagger.steps.base_step import BaseStep
from flagger.workflow import Workflow


def dumps(*args, **kwargs):
    return json.dumps(*args, cls=JSONEncoder, **kwargs)


def loads(*args, **kwargs):
    return json.loads(*args, cls=JSONDecoder, **kwargs)


class JSONEncoder(json.JSONEncoder):

    def default(self, obj):  # pylint: disable=method-hidden
        if isinstance(obj, Workflow):
            return {
                '__type__': 'Workflow',
                'value': _node_link_data(obj),
            }
        if isinstance(obj, BaseStep):
            return {
                '__type__': 'Step',
                'class_name': type(obj).__name__,
                'module_name': type(obj).__module__,
                'value': obj.__dict__,
            }
        return json.JSONEncoder.default(self, obj)


class JSONDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook,
                                  *args, **kwargs)

    def object_hook(self, obj):  # pylint: disable=method-hidden
        if '__type__' not in obj:
            return obj
        if obj['__type__'] == 'Workflow':
            return _node_link_graph(obj['value'])
        if obj['__type__'] == 'Step':
            step = steps[obj['class_name']]
            return step(**obj['value'])


def _node_link_data(G):
    attrs = dict(source='source', target='target', name='id',
                 key='key', link='links')
    name = attrs['name']
    source = attrs['source']
    target = attrs['target']
    links = attrs['link']
    data = {
        'id': G.id,
        'nodes': [dict(chain(G.nodes[n].items(), [(name, n)])) for n in G],
        links: [
            dict(chain(d.items(), [(source, u), (target, v)]))
            for u, v, d in G.edges(data=True)
        ]
    }
    return data


def _node_link_graph(data):
    graph = Workflow(data['id'])
    for node in data['nodes']:
        graph.add_node(node['id'])
    for link in data['links']:
        source = graph.get_step_by(id=link['source'].id)
        target = graph.get_step_by(id=link['target'].id)
        graph.add_edge(source, target)
    return graph
