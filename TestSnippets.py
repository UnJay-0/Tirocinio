def f(x, grad):
    if grad.size > 0:
        grad[:] = 2*x
        # gradients of the of on all parameters
    return 0  # value of f(x)
