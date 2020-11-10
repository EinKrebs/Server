import typing


def to_dictionary(pairs: typing.Iterator[tuple]):
    res = {}
    for pair in pairs:
        if len(pair) != 2:
            raise ValueError("Only pairs are allowed")
        res[pair[0]] = pair[1]
    return res
