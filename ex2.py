from typing import Tuple

from datapype.typed_tuple import field, TypedTuple


class Test(TypedTuple):
    x = field(int)
    y = field(float)


def f():
    # type: () -> Tuple[int, float]
    instance = Test(x=123, y=1.0)
    return instance.x, instance.y
