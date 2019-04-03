from typing import Type, Union


class field(object):
    def __init__(self, type_arg, required=False, default=None):
        self.type_arg = type_arg if isinstance(type_arg, tuple) else (type_arg,)

    def check(self, value):
        if not isinstance(value, self.type_arg):
            raise ValueError('Expected {} but got {} ({})'.format(
                ', '.join(map(lambda cls: cls.__name__, self.type_arg)),
                type(value).__name__,
                value,
            ))
        return value


class field(type_arg):
    type_arg = type_arg if isinstance(type_arg, tuple) else (type_arg,)

    class _Field(object):
        


def _get_fields(cls):
    if not hasattr(cls, '_fields'):
        fields = tuple((k for k in dir(cls) if isinstance(getattr(cls, k), field)))
        setattr(cls, '_fields', fields)
    return getattr(cls, '_fields')


class TypedTuple(tuple):
    def __new__(cls, **kwargs):
        values = (getattr(cls, name).check(kwargs[name]) for name in _get_fields(cls))
        result = super(TypedTuple, cls).__new__(cls, values)
        for name, value in zip(result._fields, result):
            setattr(result, name, value)
        return result

    def keys(self):
        return tuple(self._fields)

    def values(self):
        return tuple(self)

    def items(self):
        return ((name, self[name]) for name in self._fields)

    def asdict(self):
        return dict(self)

    def __getitem__(self, key):
        if isinstance(key, str):
            return getattr(self, key)
        return super(TypedTuple, self).__getitem__(key)

    def __setattr__(self, name, value):
        if name is '_fields' or (name in self._fields and name in vars(self)):
            raise Exception('cant let you do that')
        super(TypedTuple, self).__setattr__(name, value)

    def __repr__(self):
        values = repr(dict(self))[1:-1].replace('\'', '').replace(': ', '=')
        return '{}({})'.format(type(self).__name__, values)
