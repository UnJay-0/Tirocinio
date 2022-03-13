import nlopt
import atomiDati


def main():
    opt = nlopt.opt(nlopt.LN_COBYLA, 3)
    opt.set_min_objective(f)
    opt.set_xtol_rel(1e-10)
    xopt = opt.optimize([0, 0, 0])
    print(f"posizione sonda: {xopt[0]:.2f} {xopt[1]:.2f} {xopt[2]:.2f}")
    print(f"valore energia: {opt.last_optimum_value()}")
    print(f"terminazione per: {opt.last_optimize_result()}")
    print(f"numero di valutazioni: {opt.get_numevals()}")


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
    val = 0.0
    if grad.size > 0:
        grad[:] = 2*x  # gradients of the of on all parameters
    for i in range(atomiDati.N_ATOMI):
        val += atomiDati.A[i] / ((dist_euclidea(i, x[0], x[1], x[2])) ** 6) \
            - atomiDati.B[i] / ((dist_euclidea(i, x[0], x[1], x[2])) ** 3)
    return val


def dist_euclidea(i, x, y, z):
    return (atomiDati.X[i] - x) ** 2 + (atomiDati.Y[i] - y) ** 2
    + (atomiDati.Z[i] - z) ** 2


if __name__ == '__main__':
    main()
