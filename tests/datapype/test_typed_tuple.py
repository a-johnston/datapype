from datapype.typed_tuple import TypedTuple, field


def test_basic_construction():
    class TestClass(TypedTuple):
        a = field(int)

    instance = TestClass(a=123)
    assert 123 == instance.a


def test_multi_class_composition():
    class A(TypedTuple):
        a = field(int)

    class B(TypedTuple):
        b = field(int)

    class C(A, B):
        c = field(int)

    instance = C(a=1, b=2, c=3)
    assert 1 == instance.a
    assert 2 == instance.b
    assert 3 == instance.c
