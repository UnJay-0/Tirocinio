from ..model import Model
import nlopt
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
        self.opt.add_equality_mconstraint(
            lambda result, x, grad: derivativeFree.sin(
                result, x, grad, data),
            [config["sinTol"] for i in range(data["numeroPunti"])])
        self.opt.set_ftol_rel(config["xtol_rel"])
        self.opt.set_xtol_rel(config["xtol_rel"])
        if config["maxeval"] is not None:
            self.opt.set_maxeval(config["maxeval"])
        self.opt.set_min_objective(
            lambda x, grad: derivativeFree.f(x, grad, data["numeroPunti"]))
        self.opt.add_inequality_constraint(
            derivativeFree.pulsazionePositiva, 1e-6)
        lopt = nlopt.opt(config["algorithm"], 3 + self.data["numeroPunti"])
        lopt.set_ftol_rel(1e-3)
        lopt.set_xtol_rel(1e-3)
        self.opt.set_local_optimizer(lopt)

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
        guess = [1, 1, 0]
        for i in range(self.opt.get_dimension() - 3):
            guess.append(0)
        xopt = self.opt.optimize(guess)
        val = 0
        for err in xopt[3:]:
            val += err**2
        return (self.opt.last_optimum_value(), xopt, val)
