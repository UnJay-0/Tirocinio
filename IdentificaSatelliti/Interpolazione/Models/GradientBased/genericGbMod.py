from . import gradientBased
import nlopt
from ..model import Model


class GenericGb(Model):
    """
    Rappresenta e definisce un modello per la risoluzione del problema di
    Identidicazione di satelliti che utilizza un solutore basati sul gradiente
    implementati in nlopt.
    Classe immutabile.
    """

    opt = None

    def __init__(self, data, config):
        super().__init__(data, config)
        self.opt = nlopt.opt(nlopt.AUGLAG, 3 + self.data["numeroPunti"])
        self.settings()
        self.constraints()

    def constraints(self):
        self.opt.add_inequality_constraint(
            gradientBased.pulsazionePositiva, 1e-6)
        self.opt.add_inequality_constraint(
            lambda x, grad: gradientBased.periodo(x, grad, self.data["b"]),
            self.config["sinTol"])
        self.opt.add_inequality_constraint(
            gradientBased.pulsazionePositiva, 1e-6)
        self.opt.add_equality_mconstraint(
            lambda result, x, grad: gradientBased.sin(
                result, x, grad, self.data),
            [self.config["sinTol"] for i in range(self.data["numeroPunti"])])

    def settings(self):
        self.opt.set_ftol_rel(self.config["xtol_rel"])
        self.opt.set_xtol_rel(self.config["xtol_rel"])
        if self.config["maxeval"] is not None:
            self.opt.set_maxeval(self.config["maxeval"])
        self.opt.set_min_objective(
             lambda x, grad: gradientBased.f(
                 x, grad, self.data["numeroPunti"]))
        lopt = nlopt.opt(self.config["algorithm"],
                         3 + self.data["numeroPunti"])
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
        guess = [0.1, 0.1, 0]
        for i in range(self.opt.get_dimension() - 3):
            guess.append(0)
        xopt = self.opt.optimize(guess)
        val = 0
        for err in xopt[3:]:
            val += err**2
        return (self.opt.last_optimum_value(), xopt, val)
