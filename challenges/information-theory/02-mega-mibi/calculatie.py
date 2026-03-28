def missing(tb):
    actual = tb * (10**12)
    expecting = tb * (2**40)
    return ((expecting - actual) / expecting) * 100


print(missing(4))
