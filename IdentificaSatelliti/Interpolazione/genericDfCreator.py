from .interpolator import Interpolator
from .Models.model import Model
from .Models.GradientFree.genericDfMod import GenericDf


class GenericDfCreator(Interpolator):
    """
    Costruisce un modello di interpolazione per il problema di identificazione
    di satelliti che utilizza un solutore qualsiasi derivative free di nlopt.
    """

    def createModel(self, data, config) -> Model:
        """
        Meaning
        -------------------
        Costruisce un modello di interpolazione che individua l'ottimo
        (sinusoide di massimo periodo e di minimo errore) sui dati passati per
        parametro e sui valori di configurazione definiti che utilizza
        un solutore qualsiasi derivative free di nlopt.

        Parameters
        -------------------
        data -> dict contenente i dati (i punti e la loro numerosità)
        config -> dict contenente i valori di configurazione necessari
                  per il modello.
        Returns
        -------------------
        Modello di interpolazione
        """
        return GenericDf(data, config)
