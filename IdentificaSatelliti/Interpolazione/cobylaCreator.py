from .interpolator import Interpolator
from .Models.model import Model
from .Models.GradientFree.cobylaMod import Cobyla


class CobylaCreator(Interpolator):

    def createModel(self, data, config) -> Model:
        """
        Meaning
        -------------------
        Costruisce un modello di interpolazione che individua l'ottimo
        (sinusoide di massimo periodo e di minimo errore) sui dati passati per
        parametro e sui valori di configurazione definiti che utilizza
        il solutore COBYLA

        Parameters
        -------------------
        data -> dict contenente i dati (i punti e la loro numerosit√†)
        config -> dict contenente i valori di configurazione necessari
                  per il modello.
        Returns
        -------------------
        Modello di interpolazione
        """
        return Cobyla(data, config)
