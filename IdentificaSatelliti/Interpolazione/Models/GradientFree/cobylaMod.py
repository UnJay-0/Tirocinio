from ..model import Model
import nlopt
from . import derivativeFree


class Cobyla(Model):
    """
    Rappresenta e definisce un modello per la risoluzione del problema di
    Identidicazione di satelliti che utilizza il solutore COBYLA
    Classe mutabile.
    """
    opt = None

    def __init__(self, data, config):
        super().__init__(data, config)
        self.opt = nlopt.opt(nlopt.LN_COBYLA, 3 + self.data["numeroPunti"])
        self.opt.add_equality_mconstraint(
            lambda result, x, grad: derivativeFree.sinusoidale(
                result, x, grad, data),
            [config["sinusoidaleTol"] for i in range(data["numeroPunti"])])
        self.opt.set_ftol_rel(config["ftol_rel"])
        self.opt.set_xtol_rel(config["xtol_rel"])
        if config["maxeval"] is not None:
            self.opt.set_maxeval(config["maxeval"])
        self.opt.set_max_objective(derivativeFree.f)

    def optimize(self) -> tuple:
        """
        Meaning
        -------------------
        Effettua il calcolo dell'ottimo.

        Returns
        -------------------
        una terna contenente il valore ottimo ottenuto,
        l'ampiezza e errore quadratico
        """
        xopt = self.opt.optimize(
            [0 for i in range(3 + self.data["numeroPunti"])])
        val = 0
        for err in xopt[3:]:
            val += err**2
        return (self.opt.last_optimum_value(), xopt[1], val)
