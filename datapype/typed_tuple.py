from collections import OrderedDict
from typing import Type, Union


_missing = object()


class field(object):
    def __init__(self, *type_arg, required=False, default=None, factory=None):
        self.type_arg = type_arg
        self.required = required
        self.default = default
        self.factory = factory

    def check(self, value):
        if value is _missing:
            if self.required is True:
                return None, 'Field is missing but required'
            value = self.default
        if self.factory is not None:
            value = self.factory(value)
        if value is not None and not isinstance(value, self.type_arg):
            expected = ', '.join(map(lambda c: c.__name__, self.type_arg))
            actual = type(value).__name__
            return None, f'Expected {expected} but got {name} ({value})'
        return value, None


def _get_fields(cls):
    if not hasattr(cls, '_fields'):
        fields = ((k, getattr(cls, k)) for k in dir(cls) if isinstance(getattr(cls, k), field))
        setattr(cls, '_fields', OrderedDict(fields))
    return getattr(cls, '_fields')


class TypedTuple(object):
    def __init__(self, **kwargs):
        errors = []
        fields = _get_fields(type(self))
        extra_fields = sorted(set(kwargs) - set(fields))
        if extra_fields:
            raise ValueError(f'Extra fields {", ".join(extra_fields)}')
        for key, field in fields.items():
            value, err = field.check(kwargs.get(key, _missing))
            if err:
                errors += err
            setattr(self, key, value)
        if errors:
            raise ValueError(f'Errors constructing {type(self).__name__}: {", ".join(errors)}')

    def __iter__(self):
        return iter(self._fields)

    def keys(self):
        return self

    def values(self):
        return (self[k] for x in self._fields)

    def items(self):
        return ((name, self[k]) for k in self._fields)

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

