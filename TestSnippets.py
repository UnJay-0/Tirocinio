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
    if grad.size > 0:
        grad[:] = 2*x  # gradients of the of on all parameters
    return 0  # value of f(x)


def fc(x, grad):
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
    if grad.size > 0:
        grad[:] = 2*x  # gradients of the constraint on all parameters
    return 0  # value of fc(x)


def h(x, grad):
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
    the value of the equality constraint on the parameters x.

    """
    if grad.size > 0:
        grad[:] = 2*x  # gradients of the equality constraint on all parameters
    return 0  # value of e(x)


def c(result, x, grad):
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
    if grad.size > 0:
        grad[:] = 2*x  # ...set grad to gradient, in-place...
    result[0] = 0  # ...value of c_0(x)...
    result[1] = 0  # ...value of c_1(x)...
