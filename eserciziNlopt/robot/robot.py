import nlopt
import math
import robotDati


def main():
    opt = nlopt.opt(nlopt.AUGLAG, 2 * robotDati.N_ROBOTS)
    opt.set_local_optimizer(nlopt.opt(nlopt.LN_PRAXIS, 2 * robotDati.N_ROBOTS))
    for i in range(robotDati.N_ROBOTS):
        for j in range(robotDati.N_ROBOTS):
            if i < j:
                opt.add_inequality_constraint(
                    lambda x, grad: dist(x, grad, i, j),)
    opt.set_min_objective(f)
    opt.set_xtol_rel(1e-4)
    opt.set_maxtime(2)
    xopt = opt.optimize([0, 0, 0, 0, 0, 0,
                         0, 600, 900, 1200, 1500, 1800])
    for i in range(robotDati.N_ROBOTS):
        print(f"posizione robot {i}: {xopt[i]: .2f}\
              {xopt[i + robotDati.N_ROBOTS]: .2f}")
    print(f"distanza totale: {opt.last_optimum_value()}")
    for i in range(robotDati.N_ROBOTS):
        for j in range(robotDati.N_ROBOTS):
            if j > i:
                print(
                    f"distanza {i} {j}: {(((robotDati.RAGGIO[i] + robotDati.RAGGIO[j])) - math.sqrt(((xopt[j] - xopt[i]) ** 2 + (xopt[j + robotDati.N_ROBOTS] - xopt[i + robotDati.N_ROBOTS]) ** 2))): .2f} ")
    print(f"opt result code: {opt.last_optimize_result()}")
    print(f"iterazioni: {opt.get_numevals()}")


def dist(x, grad, i, j):
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
    the value of the non linear constraint on the parameters x.
    """
    '''if grad.size > 0:
        grad[i] = -2*x[i] + 2  # gradients of the constraint on all parameters
        grad[j] = -2*x[j] + 2
        grad[i + robotDati.N_ROBOTS] = -2*x[i + robotDati.N_ROBOTS] + 2
        grad[j + robotDati.N_ROBOTS] = -2*x[j + robotDati.N_ROBOTS] + 2'''
    return float((((robotDati.RAGGIO[i] + robotDati.RAGGIO[j])) ** 2)
                 - ((x[j] - x[i]) ** 2
                    + (x[j + robotDati.N_ROBOTS]
                       - x[i + robotDati.N_ROBOTS])
                    ** 2))


def f(x, grad):
    """
    Meaning
    -------------------
    Riduzione al minimo possibile delle fibre ottiche utilizzate per collegare
    i robot

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
    for i in range(robotDati.N_ROBOTS):
        for j in range(robotDati.N_ROBOTS):
            '''if grad.size > 0:
                grad[i] = -2*x[i] + 2
                grad[j] = -2*x[j] + 2
                grad[i + robotDati.N_ROBOTS] = -2*x[i + robotDati.N_ROBOTS] + 2
                grad[j + robotDati.N_ROBOTS] = -2*x[j + robotDati.N_ROBOTS] + 2'''
            if i < j:
                val += ((x[i] - x[j]) ** 2
                        + (x[i + robotDati.N_ROBOTS]
                           - x[j + robotDati.N_ROBOTS])
                        ** 2)
    return val


if __name__ == '__main__':
    main()
