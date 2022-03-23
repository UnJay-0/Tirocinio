import copy
from abc import ABCMeta, abstractmethod


class Model(metaclass=ABCMeta):
    '''
    Modello è un interfaccia che specifica i metodi per la gestione ed
    utilizzo di un modello definito sul problema di identificazione di
    satelliti.
    '''

    def __init__(self, data, config):
        self.data = copy.deepcopy(data)
        self.config = copy.copy(config)

    @abstractmethod
    def optimize(self) -> tuple:
        pass

    def setData(self, data) -> None:
        self.data = copy.deepcopy(data)
