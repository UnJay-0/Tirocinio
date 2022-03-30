from .interpolator import Interpolator
from .Models.model import Model
from .Models.GradientBased.slsqpMod import Slsqp


class SlsqpCreator(Interpolator):
    def createModel(self, data, config) -> Model:
        """
        Meaning
        -------------------
        Costruisce un modello di interpolazione che individua l'ottimo
        (sinusoide di massimo periodo e di minimo errore) sui dati passati per
        parametro e sui valori di configurazione definiti.

        Parameters
        -------------------
        data -> dict contenente i dati (i punti e la loro numerosità)
        config -> dict contenente i valori di configurazione necessari
                  per il modello.
        Returns
        -------------------
        Modello di interpolazione
        """
        return Slsqp(data, config)
