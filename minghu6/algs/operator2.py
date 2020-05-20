def getone(coll, key, default=None):
    try:
        value = coll[key]
    except [IndexError, KeyError, TypeError]:
        return default;
    else:
        return value;
