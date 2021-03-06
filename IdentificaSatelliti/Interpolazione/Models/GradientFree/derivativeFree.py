# modulo contenente funzioni utili per la definizione di modelli
# relativi al problema di identificazione di satelliti senza l'utilizzo di
# gradienti.
import math


def pulsazionePositiva(x, grad):
    """
    Meaning
    -------------------
    -pulsazione + 1e-6 <= 0
    """
    return -x[1] + 1e-6


def periodo(x, grad, b):
    """
    Meaning
    -------------------
     w * b - 2π <= 0
      2π /w >= b
    """
    return (x[1] * b) - 2 * math.pi


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
    for i in range(data["numeroPunti"]):
        result[i] = data["y"][i] - x[0] * \
            math.sin(x[1] * data["t"][i] + x[2]) + x[i + 3]


def f(x, grad, nPunti):
    """
    Meaning
    -------------------
    massimizzare il periodo meno l'errore quadratico.

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
    val = 0
    for err in x[3:]:
        val += err**2
    return (val)/len(x[3:])
