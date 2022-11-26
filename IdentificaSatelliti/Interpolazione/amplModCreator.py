from .interpolator import Interpolator
from .Models.model import Model
from .Models.amplModel.amplMod import AmplMod


class AmplModCreator(Interpolator):

    def createModel(self, data, config) -> Model:
        """
        Overview
        -------------------
        Costruisce un modello di interpolazione che individua l'ottimo
        (sinusoide di massimo periodo e di minimo errore) sui dati passati per
        parametro e sui valori di configurazione definiti.

        Parameters
        -------------------
        data (dict) ->  contenente i dati (i punti e la loro numerosità)
        config (dict) ->  contenente i valori di configurazione necessari
                  per il modello.
        Returns
        -------------------
        Modello di interpolazione
        """
        return AmplMod(data, config)
