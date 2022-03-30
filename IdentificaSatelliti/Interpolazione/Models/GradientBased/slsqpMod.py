from . import gradientBased
import nlopt
from ..model import Model


class Slsqp(Model):
    """
    Rappresenta e definisce un modello per la risoluzione del problema di
    Identidicazione di satelliti che utilizza il solutore SLSQP
    Classe immutabile.
    """

    opt = None

    def __init__(self, data, config):
        super().__init__(data, config)
        self.opt = nlopt.opt(nlopt.LD_SLSQP, 3 + self.data["numeroPunti"])
        self.opt.add_equality_mconstraint(
            lambda result, x, grad: gradientBased.sin(
                result, x, grad, data),
            [config["sinTol"] for i in range(data["numeroPunti"])])
        self.opt.set_ftol_rel(config["ftol_rel"])
        self.opt.set_xtol_rel(config["xtol_rel"])
        if config["maxeval"] is not None:
            self.opt.set_maxeval(config["maxeval"])
        self.opt.set_min_objective(
            lambda x, grad: gradientBased.f(x, grad, data["numeroPunti"]))

    def optimize(self) -> tuple:
        """
        Meaning
        -------------
        Individua l'ottimo sui dati definiti nel modello.

        Returns
        -------------------
        una terna contenente il valore ottimo ottenuto,
        l'ampiezza e errore quadratico
        """
        guess = [0.1, 0.1, 0]
        for i in range(self.opt.get_dimension() - 3):
            guess.append(0)
        xopt = self.opt.optimize(guess)
        val = 0
        for err in xopt[3:]:
            val += err**2
        return (self.opt.last_optimum_value(), xopt, val)
