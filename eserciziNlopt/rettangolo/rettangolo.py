import nlopt
import rettangoloDati


def main():
    opt = nlopt.opt(nlopt.LN_COBYLA, 12)

    opt.set_min_objective(f)
    opt.set_maxtime(1)
    opt.set_xtol_rel(1e-10)
    xopt = opt.optimize([-1000, -1000, -1000, 1000, 1000, 1000, -1000, 1000])
    print(f"punti rettangolo: {xopt}")
    print(f"area rettangolo: {opt.last_optimum_value()}")
    print(f"risultato: {opt.last_optimize_result()}")


def f(x, grad):
    """
    Meaning
    -------------------
    minimizzare l'area del rettangolo

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
        grad[:] = 2*x  # gradients of the of on all parameters
    return dist(x[0], x[2], x[1], x[3]) * dist(x[2], x[4], x[3], x[5])


def contains(result, x, grad):
    """
    Meaning
    -------------------
    ogni punto deve essere a sinistra di AB

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
    if grad.size > 0:
        grad[:] = 2*x  # ...set grad to gradient, in-place...
    for i in range(rettangoloDati.N_PUNTI):
        for j in range(4):
            result[i] = -((x[(2 + 2 * j) % 8] - x[(2 * j) % 8])
                          * (rettangoloDati.COORD_Y[i] - x[(1 + 2 * j) % 8])
                          - (x[(3 + 2 * j) % 8] - x[(1 + 2 * j) % 8])
                          * (rettangoloDati.COORD_X[i] - x[(2 * j) % 8]))


def latiParalleli(x, grad):
    """
    Meaning
    -------------------
    vincolo di uguaglianza su due lati del rettangolo.

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
    the value of the equality constraint on the parameters x.

    """
    if grad.size > 0:
        grad[:] = 2*x  # gradients of the equality constraint on all parameters
    # value of e(x)
    return dist(x[0], x[2], x[1], x[3]) - dist(x[4], x[6], x[5], x[7])


def dist(xA, xB, yA, yB):
    return (xB - xA)**2 + (yB - yA)**2


if __name__ == '__main__':
    main()
