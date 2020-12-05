def remove_accent(s: str):
    mapping = {'á': 'a',
               'é': 'e',
               'í': 'i',
               'ó': 'o',
               'ú': 'u',
               'ö': 'o',
               'ü': 'u',
               'ő': 'o',
               'ű': 'u'}

    for a, b in mapping.items():
        s = s.replace(a, b)

    return s
