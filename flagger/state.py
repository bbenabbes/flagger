class State:
    NONE = None
    RUNNING = 'RUNNING'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    SKIPPED = 'SKIPPED'

    step_states = (
        SUCCESS,
        RUNNING,
        FAILED,
        SKIPPED,
        NONE,
    )

    @classmethod
    def finished(cls):
        return [
            cls.SUCCESS,
            cls.FAILED,
            cls.SKIPPED,
        ]

    @classmethod
    def unfinished(cls):
        return [
            cls.NONE,
            cls.RUNNING,
        ]

    @classmethod
    def is_valid(cls, state):
        return state in cls.finished() + cls.unfinished()
