from unittest import TestCase

from datapype.typed_tuple import TypedTuple, field


class TestTypedTuple(TestCase):

    def test_basic_construction(self):
        class TestClass(TypedTuple):
            a = field(int)
    
        instance = TestClass(a=123)
        self.assertEqual(123, instance.a)
        self.assertEqual(123, instance['a'])
        self.assertEqual({'a': 123}, dict(instance))
        self.assertEqual({'a': 123}, instance.asdict())
        self.assertEqual('TestClass(a=123)', repr(instance))

        self.assertEqual(['a'], list(instance))
        self.assertEqual(['a'], list(instance.keys()))
        self.assertEqual([123], list(instance.values()))
        self.assertEqual([('a', 123)], list(instance.items()))
    
    def test_multi_class_composition(self):
        class A(TypedTuple):
            a = field(int)
    
        class B(TypedTuple):
            b = field(int)
    
        class C(A, B):
            c = field(int)
    
        instance = C(a=1, b=2, c=3)
        self.assertEqual(1, instance.a)
        self.assertEqual(2, instance.b)
        self.assertEqual(3, instance.c)

    def test_default_value(self):
        class TestClass(TypedTuple):
            a = field(int)
            b = field(int, default=1)

        instance = TestClass()
        self.assertEqual(None, instance.a)
        self.assertEqual(1, instance.b)

    def test_field_factory(self):
        class TestClass(TypedTuple):
            a = field(int, factory=lambda x: x ** 2)

        self.assertEqual(4, TestClass(a=2).a)


class TestTypedTupleErrors(TestCase):

    def test_immutable_error(self):
        class TestClass(TypedTuple):
            a = field(int)

        instance = TestClass(a=123)
        with self.assertRaises(Exception) as exc_info:
            instance.a = 1
        self.assertEqual(
            'TypedTuple instances should be treated as immutable',
            str(exc_info.exception),
        )

    def test_extra_field_value_error(self):
        class TestClass(TypedTuple):
            a = field(int)
    
        with self.assertRaises(ValueError) as exc_info:
            TestClass(b='bad_field')
        self.assertEqual('Extra fields b', str(exc_info.exception))

    def test_missing_field_value_error(self):
        class TestClass(TypedTuple):
            a = field(int, required=True)

        with self.assertRaises(ValueError) as exc_info:
            TestClass()
        self.assertEqual(
            'Errors constructing TestClass: field \'a\' is missing but required',
            str(exc_info.exception),
        )

    def test_unexpected_type(self):
        class TestClass(TypedTuple):
            a = field(int)

        with self.assertRaises(ValueError) as exc_info:
            TestClass(a='bad')
        self.assertEqual(
            'Errors constructing TestClass: field \'a\' expected int but got str (bad)',
            str(exc_info.exception),
        )

