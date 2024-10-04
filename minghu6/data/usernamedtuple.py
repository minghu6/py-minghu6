import collections


def namedtuple(*args, **kwargs):
    result = collections.namedtuple(*args, **kwargs)

    def to_dict(self):
        return dict([(field, getattr(self, field)) for field in self._fields])

    result.to_dict = to_dict

    return result
