from unittest.mock import Mock

from pytest import raises

from flagger.json import dumps, loads
from flagger.steps.dummy_step import DummyStep
from flagger.workflow import Workflow


class JSONEncoderTest:

    def test_encode_workflow(self):
        workflow = Workflow(id='workflow')
        result = dumps(workflow)
        expected = '{"__type__": "Workflow", "value": {"id": ' \
                   '"workflow", "nodes": [], "links": []}}'
        assert expected == result

    def test_encode_step(self):
        step = DummyStep(name='faked-name', id='faked-id')
        result = dumps(step)
        expected = '{"__type__": "Step", "class_name": "DummyStep", "module_name": ' \
                   '"flagger.steps.dummy_step", "value": {"name": "faked-name", ' \
                   '"id": "faked-id"}}'
        assert expected == result

    def test_raises_ex_when_not_json_serializable(self):
        not_serializable = Mock()
        with raises(TypeError):
            dumps(not_serializable)


class JSONDecoderTest:

    def test_decode_workflow(self):
        workflow = '{"__type__": "Workflow", "value": {"id": "workflow", ' \
                   '"nodes": [{"id": {"__type__": "Step", "class_name": "DummyStep", ' \
                   '"module_name": "flagger.steps.dummy_step", "value": {"name": ' \
                   '"faked-name", "id": "faked-id"}}}, {"id": {"__type__": "Step", ' \
                   '"class_name": "DummyStep", ' \
                   '"module_name": "flagger.steps.dummy_step", ' \
                   '"value": {"name": "faked-name", "id": "faked-id"}}}], ' \
                   '"links": [{"source": {"__type__": "Step", ' \
                   '"class_name": "DummyStep", ' \
                   '"module_name": "flagger.steps.dummy_step", "value": {' \
                   '"name": "faked-name", "id": "faked-id"}}, "target": ' \
                   '{"__type__": "Step", "class_name": "DummyStep", ' \
                   '"module_name": "flagger.steps.dummy_step", "value": ' \
                   '{"name": "faked-name", "id": "faked-id"}}}]}}'
        result = loads(workflow)
        assert isinstance(result, Workflow)
        assert all(isinstance(node, DummyStep)
                   for node in list(result.nodes))

    def test_decode_step(self):
        step = '{"__type__": "Step", "class_name": "DummyStep", "module_name": ' \
               '"flagger.steps.dummy_step", "value": {"name": "faked-name", ' \
               '"id": "faked-id"}}'
        result = loads(step)
        assert result
        assert isinstance(result, DummyStep)
        assert result.id == 'faked-id'
        assert result.name == 'faked-name'

    def test_raises_ex_when_not_decodable(self):
        not_serializable = Mock()
        with raises(TypeError):
            loads(not_serializable)
