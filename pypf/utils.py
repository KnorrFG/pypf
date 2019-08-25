def first(x):
    return next(iter(x))


def keymap(func, d: dict):
    return {func(key): val for key, val in d.items()}


def valmap(func, d: dict):
    return {key: func(val) for key, val in d.items()}


def line(s: str):
    return " ".join(line.strip() for line in s.splitlines())