from ..model import Model
import nlopt
import math
from . import derivativeFree


class GenericDf(Model):
    """
    Rappresenta e definisce un modello per la risoluzione del problema di
    Identidicazione di satelliti che utilizza Augmented Lagrangian algorithm
    con un qualsiasi algoritmo Derivative Free definito in nlopt.
    """

    opt = None

    def __init__(self, data, config):
        super().__init__(data, config)
        self.opt = nlopt.opt(nlopt.AUGLAG, 3 + self.data["numeroPunti"])
        self.constraints()
        self.settings()

    def settings(self):
        self.opt.set_ftol_rel(self.config["xtol_rel"])
        self.opt.set_xtol_rel(self.config["xtol_rel"])
        if self.config["maxeval"] is not None:
            self.opt.set_maxeval(self.config["maxeval"])
        if self.config["maxtime"] is not None:
            self.opt.set_maxtime(self.config["maxtime"])
        self.opt.set_min_objective(
             lambda x, grad: derivativeFree.f(
                 x, grad, self.data["numeroPunti"]))
        lopt = nlopt.opt(self.config["algorithm"],
                         3 + self.data["numeroPunti"])
        lopt.set_ftol_rel(1e-3)
        lopt.set_xtol_rel(1e-3)
        self.opt.set_local_optimizer(lopt)

    def constraints(self):
        self.opt.add_inequality_constraint(
            derivativeFree.pulsazionePositiva, 1e-6)
        self.opt.add_inequality_constraint(
            lambda x, grad: derivativeFree.periodo(x, grad, self.data["b"]),
            self.config["sinTol"])
        self.opt.add_inequality_constraint(
            derivativeFree.pulsazionePositiva, 1e-6)
        self.opt.add_equality_mconstraint(
            lambda result, x, grad: derivativeFree.sin(
                result, x, grad, self.data),
            [self.config["sinTol"] for i in range(self.data["numeroPunti"])])

    def optimize(self) -> tuple:
        """
        Meaning
        -------------
        Individua l'ottimo sui dati definiti nel modello.

        Returns
        -------------------
        una terna contenente il valore ottimo ottenuto,
        i termini della sinusoide e l'errore quadratico
        """
        guess = [0, self.data["b"] * 2 * math.pi, 0]
        for i in range(self.data["numeroPunti"]):
            guess.append(0)
        xopt = self.opt.optimize(guess)
        val = 0
        for err in xopt[3:]:
            val += err**2
        return (self.opt.last_optimum_value(), xopt, val,
                self.opt.last_optimize_result())
