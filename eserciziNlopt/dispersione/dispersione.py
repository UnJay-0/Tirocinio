import nlopt
import dispersioneDati


def main():
    opt = nlopt.opt(nlopt.LN_COBYLA, 41)
    opt.add_inequality_mconstraint(minimo, [1e-4 for i in range(200)])
    opt.add_inequality_mconstraint(raggio, [1e-4 for i in range(200)])
    opt.add_inequality_mconstraint(interne, [1e-4 for i in range(20)])
    opt.set_max_objective(f)
    opt.set_xtol_rel(1e-1)
    xopt = opt.optimize([0 for i in range(41)])
    for c in range(dispersioneDati.N_CERCHI):
        interno = dist(xopt[c], xopt[c+20], dispersioneDati.CENTRO_SUP[0],
                       dispersioneDati.CENTRO_SUP[1]) \
         - (dispersioneDati.RAGGIO_SUP - dispersioneDati.RAGGI[c]) ** 2
        print(f"l'area {c} è interno? {interno <= 0}")
    for c in range(dispersioneDati.N_CERCHI):
        for i in range(dispersioneDati.N_CERCHI):
            if (c < i):
                raggioV = (dispersioneDati.RAGGI[c]
                           + dispersioneDati.RAGGI[i]
                           ) ** 2 - dist(xopt[c], xopt[c+20], xopt[i], xopt[i+20])
                print(f"vincolo raggio tra {c} {i}? {raggioV <= 0}")
    print(f"valore: {opt.last_optimum_value():.2f}")
    print(f"result: {opt.last_optimize_result()}")


def minimo(result, x, grad):
    """
    Meaning
    -------------------
    calcolo del minimo tra tutte le distanze delle aree

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
        index = 0
        for c in range(dispersioneDati.N_CERCHI):
            for i in range(dispersioneDati.N_CERCHI):
                if (c < i):
                    grad[index][c]
    index = 0
    for c in range(dispersioneDati.N_CERCHI):
        for i in range(dispersioneDati.N_CERCHI):
            if (c < i):
                result[index] = x[40]**2 - dist(x[c], x[c+20], x[i], x[i+20])
                index += 1


def raggio(result, x, grad):
    """
    Meaning
    -------------------
    calcolo del minimo tra tutte le distanze delle aree

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
    index = 0
    for c in range(dispersioneDati.N_CERCHI):
        for i in range(dispersioneDati.N_CERCHI):
            if (c < i):
                result[index] = (dispersioneDati.RAGGI[c]
                                 + dispersioneDati.RAGGI[i]
                                 ) ** 2 - dist(x[c], x[c+20], x[i], x[i+20])
                index += 1


def interne(result, x, grad):
    """
    Meaning
    -------------------
    aree interne alla superficie

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
    for c in range(dispersioneDati.N_CERCHI):
        result[c] = dist(x[c], x[c+20], dispersioneDati.CENTRO_SUP[0],
                         dispersioneDati.CENTRO_SUP[1]) \
         - (dispersioneDati.RAGGIO_SUP - dispersioneDati.RAGGI[c]) ** 2


def f(x, grad):
    """
    Meaning
    -------------------
    massimizzare la distanza minima tra le aree

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
        grad[:] = 2*x
    return x[40]


def dist(xA, xB, yA, yB):
    return (xB - xA)**2 + (yB - yA)**2


if __name__ == '__main__':
    main()
