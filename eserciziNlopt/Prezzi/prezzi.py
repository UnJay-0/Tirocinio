import nlopt
import math
import prezziDati


def main():
    opt = nlopt.opt(nlopt.LN_COBYLA, 6)
    opt.add_inequality_mconstraint(produzione, [1e-4 for i in range(5)])
    opt.add_equality_mconstraint(prezzoQuantita, [1e-4 for i in range(3)])
    opt.set_max_objective(f)
    opt.set_lower_bounds(0)
    opt.set_xtol_rel(1e-30)
    xopt = opt.optimize([0, 0, 0, 0, 0, 0])
    print(f"quantita acquistate: {xopt[0]:.2f} {xopt[1]:.2f} {xopt[2]:.2f}")
    print(f"prezzo di vendita: {xopt[3]:.2f} {xopt[4]:.2f} {xopt[5]:.2f}")
    print(f"guadagno: {opt.last_optimum_value():.2f}")
    print(f"result: {opt.last_optimize_result()}")


def f(x, grad):
    """
    Meaning
    -------------------

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
    value = 0
    for p in range(prezziDati.N_PRODOTTI):
        value += x[p] * x[p + 3]
    return value  # value of f(x)


def prezzoQuantita(result, x, grad):
    """
    Meaning
    -------------------

    Parameters
    -------------------
    x -> numpy array defining the parameters of the problem
         of length n.
    grad -> 2d NumPy array defining the gradients of the constraint
            of size m x n, where m is the number of the constraints and
            n the number of parameters

    Effects
    -------------------
    Modify grad.

    Returns
    -------------------
    the value of the non linear constraint on the parameters x.

    """
    for p in range(prezziDati.N_PRODOTTI):
        result[p] = x[p + 3] - prezziDati.ALFA[p] + prezziDati.BETA[p] * \
            (math.e ** (- prezziDati.GAMMA[p] * x[p]))


def produzione(result, x, grad):
    """
    Meaning
    -------------------
    vincoli sulla quantità per prodotto producibile in base alle materie
    disponibili.

    Parameters
    -------------------
    x -> numpy array defining the parameters of the problem
         of length n.
    grad -> 2d NumPy array defining the gradients of the constraint
            of size m x n, where m is the number of the constraints and
            n the number of parameters

    Effects
    -------------------
    Modify grad.

    Returns
    -------------------
    the value of the non linear constraint on the parameters x.

    """
    for m in range(prezziDati.N_MATERIE):
        val = 0
        for p in range(prezziDati.N_PRODOTTI):
            val += (x[p] * prezziDati.COMP_PROD[m][p])
        result[m] = val - prezziDati.DISP[m]


if __name__ == '__main__':
    main()
