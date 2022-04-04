# modulo contenente funzioni utili per la definizione di modelli
# relativi al problema di identificazione di satelliti con l'utilizzo di
# gradienti.

import math


def periodo(x, grad, b):
    """
    Meaning
    -------------------
     w / 2π - b  <= 0
    """
    if grad.size > 0:
        for i in range(grad.size):
            grad[i] = 0
        grad[1] = b
    return x[1] * b - 2 * math.pi


def pulsazionePositiva(x, grad):
    """
    Meaning
    -------------------
    pulsazione + 1e-6 >= 0
    """
    if grad.size > 0:
        for i in range(grad.size):
            grad[i] = 0
        grad[1] = -1
    return -x[1] + 1e-6


def sin(result, x, grad, data):
    """
    Meaning
    -------------------
    tutti i punti devono essere interpolati in una sinusoide con un
    certo relativo errore.

    Parameters
    -------------------
    x -> numpy array defining the parameters of the problem
         of length n.
    grad -> 2d NumPy array defining the gradients of the constraint
            of size m x n, where m is the number of the constraints and
            n the number of parameters
    result -> constraints
    data -> posizione e numero dei punti da interpolare.


    Effects
    -------------------
    Modify grad.

    Returns
    -------------------
    the value of the non linear constraint on the parameters x.

    """
    if grad.size > 0:
        sinGradient(x, grad, data)
    for i in range(data["numeroPunti"]):
        result[i] = data["y"][i] - x[0] * \
            math.sin(x[1] * data["t"][i] + x[2]) + x[i + 2]


def sinGradient(x, grad, data):
    for i in range(data["numeroPunti"]):
        grad[i, 0] = - math.sin(x[1] * data["t"][i] + x[2])
        grad[i, 1] = - data["t"][i] * x[0] * \
            math.cos(x[1] * data["t"][i] + x[2])
        grad[i, 2] = - x[0] * math.cos(x[1] * data["t"][i] + x[2])
        for j in range(data["numeroPunti"]):
            grad[i, j + 3] = 1 if j == i else 0


def f(x, grad, nPunti):
    """
    Meaning
    -------------------
    minimizzare la frequenza più l'errore quadratico.

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
        grad[0] = 0
        grad[1] = x[1] / 2 * math.pi * abs(x[1])
        grad[2] = 0
        for i in range(3, nPunti):
            grad[i] = 2 * x[i]
    val = 0
    for err in x[3:]:
        val += err**2
    return (val)
