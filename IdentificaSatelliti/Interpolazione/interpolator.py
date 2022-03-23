from abc import ABCMeta, abstractmethod
from .Models.model import Model


class Interpolator(metaclass=ABCMeta):

    @abstractmethod
    def createModel(self, data, config) -> Model:
        pass
