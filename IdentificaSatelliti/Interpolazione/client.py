import nlopt
from .interpolator import Interpolator
from .slsqpCreator import SlsqpCreator
from .genericDfCreator import GenericDfCreator
from .genericGbCreator import GenericGbCreator
from .cobylaCreator import CobylaCreator

LN = [nlopt.LN_BOBYQA, nlopt.LN_PRAXIS, nlopt.LN_SBPLX,
      nlopt.LN_NEWUOA, nlopt.LN_NELDERMEAD]
LD = [nlopt.LD_MMA, nlopt.LD_VAR1, nlopt.LD_VAR2,
      nlopt.LD_CCSAQ, nlopt.LD_LBFGS, nlopt.LD_TNEWTON]


def interpolation(data: dict, algorithm=nlopt.LN_COBYLA, sinTol=1e-6,
                  ftol_rel=1e-6, xtol_rel=1e-6, maxeval=None, maxtime=None):
    """
    Overview
    -------------------
    Interpola i punti dati in data con la configurazione impostata.
    data è un dict che deve contenere le coordinate dei valori y e t, la loro
    numerosità e la soglia della frequenza b.
    data{ "numeroPunti" : [val]
          "y": [...]
          "t": [...]
          "b": [val]
        }
    Params
    -------------------
    data (dict) - contiene i punti da interpolare.
    algorithm (int) - algoritmo da utilizzare per l'interpolazione.
    sinTol (float) - tolleranza per i vincoli.
    ftol_rel (float) - tolleranza per la valutazione del passo della funzione
                       obiettivo.
    maxeval (int) - numero di valutazioni massime da effettuare.
    maxtime (float) - tempo massimo di secondi per il calcolo dell'ottimo.

    Raises
    -------------------
    Exception - se data non contiene le informazioni richieste.
                se algorithm è non è noto.

    Returns
    -------------------
    dict - contenente il risultato della computazione.

    """
    # if (not("b" in dict) or not("t" in dict) or not("y" in dict)
    #        or not("b" in dict)):
    #    raise Exception("data non è ben formattato")

    config = {"algorithm": algorithm, "sinTol": sinTol, "ftol_rel": ftol_rel,
              "xtol_rel": xtol_rel, "maxeval": maxeval, "maxtime": maxtime}

    if (config["algorithm"] == nlopt.LN_COBYLA):
        intModel = CobylaCreator()
    elif (config["algorithm"] in LN):
        intModel = GenericDfCreator()
    elif (config["algorithm"] == nlopt.LD_SLSQP):
        intModel = SlsqpCreator()
    elif (config["algorithm"] in LD):
        intModel = GenericGbCreator()
    else:
        raise Exception("algorithm non è noto")
    return intModel.interpolate(data, config)
