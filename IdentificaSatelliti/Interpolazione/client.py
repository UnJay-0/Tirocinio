from .amplModCreator import AmplModCreator

AMPL = ["snopt", "knitro", "lgo", "minos", "loqo", "conopt"]


def interpolation(data: dict, algorithm="knitro", sinTol=1e-6,
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
    data (dict) -> contiene i punti da interpolare.
    algorithm (int) -> algoritmo da utilizzare per l'interpolazione.
    sinTol (float) -> tolleranza per i vincoli.
    ftol_rel (float) -> tolleranza per la valutazione del passo della funzione
                       obiettivo.
    maxeval (int) -> numero di valutazioni massime da effettuare.
    maxtime (float) -> tempo massimo di secondi per il calcolo dell'ottimo.

    Raises
    -------------------
    Exception -> se data non contiene le informazioni richieste.
                se algorithm è non è noto.

    Returns
    -------------------
    dict -> contenente il risultato della computazione.

    """

    config = {"algorithm": algorithm, "sinTol": sinTol, "ftol_rel": ftol_rel,
              "xtol_rel": xtol_rel, "maxeval": maxeval, "maxtime": maxtime}

    if (config["algorithm"] in AMPL):
        intModel = AmplModCreator()
    else:
        raise Exception("algorithm non è noto")
    return intModel.interpolate(data, config)
