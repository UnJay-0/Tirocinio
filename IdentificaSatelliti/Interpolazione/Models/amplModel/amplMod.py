from ..model import Model
from amplpy import AMPL
import os


class AmplMod(Model):
    """
    Rappresenta e definisce un modello per la risoluzione del problema di
    Identidicazione di satelliti che utilizza il modello su AMPL
    Classe immutabile.
    """

    def __init__(self, data, config):
        """
        Overview
        -------------------
        Inizializza il modello ampl

        Params
        -------------------
        data (dict) -> contiene i parametri e dati relativi al modello
        config (dict) -> contiene le specifiche di impostazione del modello

        """
        self.ampl = AMPL()
        if data["minMax"]:
            self.ampl.read(
                os.path.abspath('./IdentificaSatelliti/Interpolazione/Models/amplModel/InterpolazioneMin.mod'))
        else:
            self.ampl.read(
                os.path.abspath('./IdentificaSatelliti/Interpolazione/Models/amplModel/InterpolazioneMax.mod'))

        self.w = self.ampl.get_variable("w")
        self.a = self.ampl.get_variable("a")
        self.p = self.ampl.get_variable("p")
        self.config(data)
        self.ampl.set_option("solver", config["algorithm"])

    def config(self, data):
        """
        Overview
        -------------------
        Metodo che imposta i parametri e i dati in input nel modello.

        Params
        -------------------
        data (dict) -> contiene i parametri e i dati del modello

        """
        self.ampl.get_parameter("minW").set(data["minW"])
        self.ampl.get_parameter("maxW").set(data["maxW"])
        self.w.set_value(data["init"])
        self.ampl.get_parameter("nOss").set(data["numeroPunti"])

        self.ampl.get_parameter("tempo").set_values(data["t"])

        self.ampl.get_parameter("y").set_values(data["y"])

        minA, maxA = AmplMod.amplitude(data["y"], data["multiplier"])
        self.ampl.get_parameter("minA").set(minA)
        self.ampl.get_parameter("maxA").set(maxA)
        self.a.set_value((minA + maxA) / 2)
        if data["fixedA"]:
            self.a.set_value(data["fixedA"])

    def amplitude(y, multiplier):
        """
        Overview
        -------------------
        Metodo che imposta i limiti dell'ampiezza.

        Params
        -------------------
        y (list) - valori della sinusoide

        Returns
        -------------------
        Tupla contenente i limiti per i vincoli sull'ampiezza.

        """
        tmp = [abs(el) for el in y]
        maxVal = max(tmp)
        if AmplMod.amplitudeAnalisys(y):
            return (maxVal, maxVal * (20 + (20 * multiplier)))
        else:
            return (maxVal, maxVal*2)

    def amplitudeAnalisys(y):
        """
        Overview
        -------------------
        Metodo che effettua un analisi sulla monotonia dei valori
        della sinusoide.

        Params
        -------------------
        y (list) -> valori della sinusoide.

        Returns
        -------------------
        True se i valori sono tutti positivi o negativi, false altrimenti.

        """
        isPositive = [(el > 0) for el in y if el != 0.0]
        isNegative = [(el < 0) for el in y if el != 0.0]
        allPositive = True
        allNegative = True
        for i in range(len(isPositive)):
            allPositive = allPositive and isPositive[i]
            allNegative = allNegative and isNegative[i]
        return allNegative ^ allPositive

    def optimize(self) -> tuple:
        """
        Overview
        -------------------
        Metodo che avvia il processo di ottimizzazione ed individuazione di
        una soluzione.

        Returns
        -------------------
        Tupla contenete i parametri della soluzionbe individuata.

        """
        fo = self.ampl.get_objective("z")
        self.ampl.solve()
        return (fo.value(), (self.a.value(), self.w.value(), self.p.value()),
                fo.astatus())
