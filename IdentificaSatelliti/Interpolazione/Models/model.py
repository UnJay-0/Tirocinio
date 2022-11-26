import copy
from abc import ABCMeta, abstractmethod


class Model(metaclass=ABCMeta):
    '''
    Modello è una classe astratta che specifica i metodi per la gestione ed
    utilizzo di un modello definito sul problema di identificazione di
    satelliti.
    '''

    def __init__(self, data, config):
        """
        Meaning
        -------------------
        Costruttore della classe che inizializza l'istanza sui dati e sui
        valori di configurazione passati per parametro

        Parameters
        -------------------
        data (dict) ->  contenente i dati (i punti e la loro numerosità)
        config (dict) ->  contenente i valori di configurazione necessari
                  per il modello.
        """
        self.data = copy.deepcopy(data)
        self.config = copy.copy(config)

    @abstractmethod
    def optimize(self) -> tuple:
        """
        Meaning
        -------------------
        Individua l'ottimo sui dati definiti nel modello.

        Returns
        -------------------
        una terna contenente il valore ottimo ottenuto,
        l'ampiezza e errore quadratico
        """
        pass
