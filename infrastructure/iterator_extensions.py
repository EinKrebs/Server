import typing


def to_dictionary(pairs: typing.Iterator[tuple]):
    res = {}
    for pair in pairs:
        if len(pair) != 2:
            raise ValueError("Only pairs are allowed")
        res[pair[0]] = pair[1]
    return res


def dictionary_to_string(dictionary: typing.Dict[str, str],
                         pair_delimiter: str,
                         key_value_delimiter: str):
    return pair_delimiter.join(str(key) + key_value_delimiter + str(value)
                               for key, value in dictionary.items())
