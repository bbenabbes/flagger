from abc import abstractmethod
from uuid import uuid4


class BaseStep:
    """
    Base class for all steps.
    """

    def __init__(self, name, id=None):
        self.name = name
        if not id:
            self.id = str(uuid4())
        else:
            self.id = id

    @abstractmethod
    def run(self):
        raise NotImplementedError('This method must be overridden '
                                  'in all subclasses')

    def __repr__(self):
        return f'Step<{self.__class__.__name__}: {self.name}>'
