from ..model import Model
from amplpy import AMPL, Environment


class AmplMod(Model):
    """
    Rappresenta e definisce un modello per la risoluzione del problema di
    Identidicazione di satelliti che utilizza il modello su AMPL
    Classe immutabile.
    """

    def __init__(self, data, config):
        self.ampl = AMPL(Environment(
            r'/Users/Jay/Documents/uni/Ricop/ampl_macos64'))
        if data["minMax"]:
            self.ampl.read(
                '/Users/Jay/github/Tirocinio/IdentificaSatelliti/Interpolazione/Models/amplModel/InterpolazioneMin.mod')
        else:
            self.ampl.read(
                '/Users/Jay/github/Tirocinio/IdentificaSatelliti/Interpolazione/Models/amplModel/InterpolazioneMax.mod')

        # self.ampl.read_data(
        #    '/Users/Jay/github/Tirocinio/IdentificaSatelliti/Interpolazione/Models/amplModel/InterpolazioneData.dat')
        self.w = self.ampl.get_variable("w")
        self.a = self.ampl.get_variable("a")
        self.p = self.ampl.get_variable("p")
        self.config(data)
        self.ampl.set_option("solver", config["algorithm"])

    def config(self, data):
        self.ampl.get_parameter("minW").set(data["minW"])
        self.ampl.get_parameter("maxW").set(data["maxW"])
        self.w.set_value(data["init"])
        self.ampl.get_parameter("nOss").set(data["numeroPunti"])

        self.ampl.get_parameter("tempo").set_values(data["t"])

        self.ampl.get_parameter("y").set_values(data["y"])

        minA, maxA = AmplMod.amplitude(data["y"])
        self.ampl.get_parameter("minA").set(minA)
        self.ampl.get_parameter("maxA").set(maxA)
        self.a.set_value((minA + maxA) / 2)
        if data["fixedA"]:
            self.a.fix(data["fixedA"])

    def amplitude(y):
        maxVal = max(y)
        return (maxVal, maxVal*5)

    def optimize(self) -> tuple:
        fo = self.ampl.get_objective("z")
        self.ampl.solve()
        return (fo.value(), (self.a.value(), self.w.value(), self.p.value()),
                fo.astatus())
