from ..model import Model
import nlopt
from . import derivativeFree


class Cobyla(Model):
    """
    Rappresenta e definisce un modello per la risoluzione del problema di
    Identidicazione di satelliti che utilizza il solutore COBYLA
    Classe immutabile.
    """
    opt = None

    def __init__(self, data, config):
        super().__init__(data, config)
        self.opt = nlopt.opt(nlopt.LN_COBYLA, 3 + data["numeroPunti"])
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
        l'ampiezza e errore quadratico
        """
        guess = [0, self.data["init"], 0]
        for i in range(self.data["numeroPunti"]):
            guess.append(0)
        xopt = self.opt.optimize(guess)
        return (self.opt.last_optimum_value(), xopt,
                self.opt.last_optimize_result())
