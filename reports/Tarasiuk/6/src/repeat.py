def repeat(pattern, repeat):
    if pattern is None:
        raise TypeError("pattern cannot be None")

    if repeat < 0:
        raise ValueError("repeat must be non-negative")

    return pattern * repeat
