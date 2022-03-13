import nlopt
import math
import numpy as np
'''
Costi fissi di acquisto delle macchine: 1000.00 Euro
Costi variabili di produzione: 10.00 Euro/Kg
Coefficiente di proporzionalita k: 80
Quantita massima che il mercato puo assorbire: 70 Kg/mese
Prezzo massimo di vendita: 20.00 Euro/Kg

'''

COSTO_ACQUISTO = 1000
COSTO_PRODUZIONE = 10
COEFF = 80
QUANTITA_MASSIMA = 70
PREZZO_VENDITA = 20


def main():
    opt = nlopt.opt(nlopt.LN_BOBYQA, 1)
    opt.set_lower_bounds(0)
    opt.set_upper_bounds(QUANTITA_MASSIMA)
    opt.set_max_objective(f)
    opt.set_xtol_rel(1e-8)
    x = np.ndarray(shape=1, dtype=float, buffer=np.array([1.0]))
    xopt = opt.optimize(x)
    print(f"farina acquistata: {xopt[0]}")
    print(f"guadagno: {opt.last_optimum_value()}")
    print(f"opt result code: {opt.last_optimize_result()}")


def f(x, grad):
    """
    Meaning
    -------------------
    profitto sulla vendita di prodotti sulla farina di baobab

    Parameters
    -------------------
    x -> numpy array defining the parameters of the problem
         of length n.
    grad -> numpy array defining the gradients of the constraint
            of length n.

    Effects
    -------------------
    Modify grad.

    Returns
    -------------------
    the value of the objective function on the parameters x.
    """
    if grad.size > 0:
        grad[0] = PREZZO_VENDITA - (-COEFF / (2 * math.sqrt(x**3))
                                    + COSTO_PRODUZIONE)
    return float(x * PREZZO_VENDITA - (
                                 COEFF / math.sqrt(x)
                                 + COSTO_PRODUZIONE * x))


if __name__ == '__main__':
    main()
