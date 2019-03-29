import pytest

from flagger.state import State


@pytest.mark.unit
class StateTest:

    def test_finished(self):
        states = State.finished()
        expected = [
            'SUCCESS',
            'FAILED',
            'SKIPPED',
        ]
        assert expected == states

    def test_unfinished(self):
        states = State.unfinished()
        expected = [
            None,
            'RUNNING',
        ]
        assert expected == states

    @pytest.mark.parametrize('state, expected', [
        (None, True),
        ('SUCCESS', True),
        ('FAILED', True),
        ('SKIPPED', True),
        ('RUNNING', True),
        ('foo-state', False),
    ])
    def test_is_valid(self, state, expected):
        assert expected == State.is_valid(state)
