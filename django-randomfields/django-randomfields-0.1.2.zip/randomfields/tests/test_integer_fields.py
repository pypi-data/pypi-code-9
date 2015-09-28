from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from django.utils.six.moves import range
from randomfields.models.fields import RandomFieldBase
from randomfields.models.fields.integer import RandomIntegerFieldBase, RandomBigIntegerField, RandomIntegerField, RandomSmallIntegerField, \
                                        RandomBigIntegerIdentifierField, RandomIntegerIdentifierField, RandomSmallIntegerIdentifierField, \
                                        NarrowPositiveIntegerField, IntegerIdentifierValue
from .. import random
from . import mock

def raise_not_implemented(*args, **kwargs):
    raise NotImplementedError()

class FieldTests(SimpleTestCase):
    @mock.patch('randomfields.random.secure_random')
    def test_random_randint(self, mocked_secure_random):
        # verify secure_random was mocked
        self.assertIsInstance(random.secure_random, mocked_secure_random.__class__)
        
        # verify secure_random.randint hasn't been called
        self.assertEqual(mocked_secure_random.randint.call_count, 0)
        random.randint(1, 1)
        
        # verify secure_random.randint was called
        self.assertEqual(mocked_secure_random.randint.call_count, 1)
        
        # override secure_random.randint so that it raises a NotImplementedError
        mocked_secure_random.randint = raise_not_implemented
        with self.assertRaises(NotImplementedError):
            mocked_secure_random.randint(1, 2)
        
        with mock.patch('randomfields.random.log_exceptions', new=True):
            # force the exception to be logged
            self.assertTrue(random.log_exceptions)
            
            with mock.patch('randomfields.random.insecure_random') as mocked_insecure_random:
                with mock.patch('randomfields.random.logger') as mocked_logger:
                    # mock the logger so we can verify the exception gets logged
                    self.assertEqual(mocked_logger.exception.call_count, 0)
                    
                    # verify the mocked insecure_random.randint hasn't been called
                    self.assertEqual(mocked_insecure_random.randint.call_count, 0)
                    random.randint(1, 1)
                    
                    # verify exception was logged
                    self.assertEqual(mocked_logger.exception.call_count, 1)
                    
                    # verify mocked_insecure_random.randint was called
                    self.assertEqual(mocked_insecure_random.randint.call_count, 1)
    
    @mock.patch('randomfields.random.secure_random')
    def test_random_coice(self, mocked_secure_random):
        # verify secure_random was mocked
        self.assertIsInstance(random.secure_random, mocked_secure_random.__class__)
        
        # verify secure_random.choice hasn't been called
        self.assertEqual(mocked_secure_random.choice.call_count, 0)
        random.choice("ab")
        
        # verify secure_random.choice was called
        self.assertEqual(mocked_secure_random.choice.call_count, 1)
        
        # override secure_random.choice so that it raises a NotImplementedError
        mocked_secure_random.choice = raise_not_implemented
        with self.assertRaises(NotImplementedError):
            mocked_secure_random.choice("ab")
        
        with mock.patch('randomfields.random.log_exceptions', new=True):
            # force the exception to be logged
            self.assertTrue(random.log_exceptions)
            
            with mock.patch('randomfields.random.insecure_random') as mocked_insecure_random:
                with mock.patch('randomfields.random.logger') as mocked_logger:
                    # mock the logger so we can verify the exception gets logged
                    self.assertEqual(mocked_logger.exception.call_count, 0)
                    
                    # verify the mocked insecure_random.choice hasn't been called
                    self.assertEqual(mocked_insecure_random.choice.call_count, 0)
                    random.choice("ab")
                    
                    # verify exception was logged
                    self.assertEqual(mocked_logger.exception.call_count, 1)
                    
                    # verify mocked_insecure_random.choice was called
                    self.assertEqual(mocked_insecure_random.choice.call_count, 1)
    
    def test_zero_possibilities(self):
        field = RandomFieldBase()
        with self.assertRaises(NotImplementedError):
            field.possibilities
        with self.assertRaises(ValueError):
            field.possibilities = 0
        field.possibilities = 7
        with self.assertRaises(NotImplementedError):
            field.possibilities = 12
                
    def test_invalid_rifb_attrs(self):
        class InvalidAttrsTypeError1(RandomIntegerFieldBase):
            # lower_bound and upper_bound must be specified when bytes is not
            bytes = None
            lower_bound = None
            upper_bound = None
            
        class InvalidAttrsTypeError2(RandomIntegerFieldBase):
            # lower_bound and upper_bound must be None when bytes is specified
            bytes = 4
            lower_bound = 5
            upper_bound = 10
        
        class InvalidAttrsTypeError3(RandomIntegerFieldBase):
            # bytes type error
            bytes = object()
        
        class InvalidAttrsTypeError4(RandomIntegerFieldBase):
            # lower_bound type error
            lower_bound = None
            upper_bound = 10
        
        class InvalidAttrsTypeError5(RandomIntegerFieldBase):
            # upper_bound type error
            lower_bound = 10
            upper_bound = None
        
        for cls in [InvalidAttrsTypeError1, InvalidAttrsTypeError2, InvalidAttrsTypeError3, InvalidAttrsTypeError4, InvalidAttrsTypeError5]:
            with self.assertRaises(TypeError):
                cls()
        
        class InvalidAttrsValueError1(RandomIntegerFieldBase):
            # bytes value error
            bytes = "foo"
        
        class InvalidAttrsValueError2(RandomIntegerFieldBase):
            # lower_bound value error
            lower_bound = "foo"
            upper_bound = 10
        
        class InvalidAttrsValueError3(RandomIntegerFieldBase):
            # upper_bound value error
            lower_bound = 10
            upper_bound = "foo"
        
        for cls in [InvalidAttrsValueError1, InvalidAttrsValueError2, InvalidAttrsValueError3]:
            with self.assertRaises(ValueError):
                cls()
        
    def test_big_integer_bounds(self):
        field = RandomBigIntegerField()
        self.assertEqual(field.lower_bound, -9223372036854775808)
        self.assertEqual(field.upper_bound, 9223372036854775807)
    
    def test_integer_bounds(self):
        field = RandomIntegerField()
        self.assertEqual(field.lower_bound, -2147483648)
        self.assertEqual(field.upper_bound, 2147483647)
    
    def test_small_integer_bounds(self):
        field = RandomSmallIntegerField()
        self.assertEqual(field.lower_bound, -32768)
        self.assertEqual(field.upper_bound, 32767)
    
    def test_integer_formfield_bounds(self):
        for field_cls in [RandomIntegerField, RandomBigIntegerField, RandomSmallIntegerField, NarrowPositiveIntegerField]:
            field = field_cls()
            form_field = field.formfield()
            
            # no exceptions
            form_field.clean(field.lower_bound)
            form_field.clean(field.upper_bound)
            for value in [int(field.lower_bound + p * (field.possibilities - 2)) for p in (.1, .3, .5, .7, .9)]:
                form_field.clean(value)
            
            with self.assertRaises(ValidationError):
                form_field.clean(field.lower_bound-1)
            with self.assertRaises(ValidationError):
                form_field.clean(field.upper_bound+1)
    
    def test_integer_random(self):
        for field_cls in [RandomIntegerField, RandomBigIntegerField, RandomSmallIntegerField]:
            field = field_cls()
            bytes_ = field.bytes
            for _ in range(10):
                val1 = field.random()
                self.assertGreaterEqual(val1, field.lower_bound)
                self.assertLessEqual(val1, field.upper_bound)
                
                # force random method to use randint instead of unpack/urandom
                field.bytes = None
                val2 = field.random()
                self.assertGreaterEqual(val2, field.lower_bound)
                self.assertLessEqual(val2, field.upper_bound)
                
                # reset
                field.bytes = bytes_
    
    def _test_integer_identifier_conversions(self, field_cls, value_map):
        field = field_cls()
        for db_value, display_value in value_map:
            result = field.to_python(db_value)
            self.assertEqual(db_value, result.db_value)
            self.assertEqual(display_value, result.display_value)
            
            result = field.to_python(display_value)
            self.assertEqual(db_value, result.db_value)
            self.assertEqual(display_value, result.display_value)
    
    def test_bigintegerfield_identifier_conversions(self):
        value_map = (
            (-9223372036854775808, 9223372036854775808),
            (0, 18446744073709551616),
            (9223372036854775807, 27670116110564327423),
        )
        self._test_integer_identifier_conversions(RandomBigIntegerIdentifierField, value_map)
    
    def test_integerfield_identifier_conversions(self):
        value_map = (
            (-2147483648, 2147483648),
            (0, 4294967296),
            (2147483647, 6442450943),
        )
        self._test_integer_identifier_conversions(RandomIntegerIdentifierField, value_map)

    def test_smallintegerfield_identifier_conversions(self):
        value_map = (
            (-32768, 32768),
            (0, 65536),
            (32767, 98303),
        )
        self._test_integer_identifier_conversions(RandomSmallIntegerIdentifierField, value_map)
    
    def test_integerfield_identifier_formfield_validation(self):
        for field_cls in (RandomBigIntegerIdentifierField, RandomIntegerIdentifierField, RandomSmallIntegerIdentifierField):
            field = field_cls()
            form_field = field.formfield()
            
            # identifiers are mapped to value + possibilities, so values range (lowerbound, upperbound)
            # should raise validation errors
            with self.assertRaises(ValidationError):
                form_field.clean(field.lower_bound)
            with self.assertRaises(ValidationError):
                form_field.clean(field.upper_bound)
            for value in [int(field.lower_bound + p * (field.possibilities - 2)) for p in (.1, .3, .5, .7, .9)]:
                with self.assertRaises(ValidationError):
                    form_field.clean(value)
            
            # no exceptions
            form_field.clean(field.lower_bound + field.possibilities)
            form_field.clean(field.upper_bound + field.possibilities)
            for value in [int(field.lower_bound + p * (field.possibilities - 2)) for p in (.1, .3, .5, .7, .9)]:
                form_field.clean(value + field.possibilities)
    
    def test_integerfield_identifier_zfill_width(self):
        for field_cls in (NarrowPositiveIntegerField, RandomBigIntegerIdentifierField, RandomIntegerIdentifierField, RandomSmallIntegerIdentifierField):
            field = field_cls()
            lb = "%s" % field.to_python(field.lower_bound)
            ub = "%s" % field.to_python(field.upper_bound)
            lb_len = len(lb)
            ub_len = len(ub)
            self.assertEqual(lb_len, ub_len, "{} and {} are of different string width, {} != {}".format(lb, ub, lb_len, ub_len))
    
    def _test_integer_identifier_value_inputs(self, excClass, *args):
        with self.assertRaises(excClass):
            IntegerIdentifierValue(*args)
    
    def test_integer_identifier_hashable(self):
        value1 = IntegerIdentifierValue(1, 3, -1, 1)
        value1_hash = hash(value1)
        
        value1_dup = IntegerIdentifierValue(1, 3, -1, 1)
        value1_dup_hash = hash(value1_dup)
        
        value2 = IntegerIdentifierValue(0, 3, -1, 1)
        value2_hash = hash(value2)
        
        value3 = IntegerIdentifierValue(-1, 3, -1, 1)
        value3_hash = hash(value3)
        
        self.assertEqual(value1_hash, value1_dup_hash)
        self.assertNotEqual(value1_hash, value2_hash)
        self.assertNotEqual(value1_hash, value3_hash)
    
    def test_integer_identifier_value_inputs(self):
        # no exceptions
        value = 1
        possibilities = 3
        lower_bound = -1
        upper_bound = 1
        IntegerIdentifierValue(value, possibilities, lower_bound, upper_bound)
        
        # test invalid type
        self._test_integer_identifier_value_inputs(TypeError, None, possibilities, lower_bound, upper_bound)
        self._test_integer_identifier_value_inputs(TypeError, value, None, lower_bound, upper_bound)
        self._test_integer_identifier_value_inputs(TypeError, value, possibilities, None, upper_bound)
        self._test_integer_identifier_value_inputs(TypeError, value, possibilities, lower_bound, None)
        
        # test invalid value
        self._test_integer_identifier_value_inputs(ValueError, "foo", possibilities, lower_bound, upper_bound)
        self._test_integer_identifier_value_inputs(ValueError, value, "foo", lower_bound, upper_bound)
        self._test_integer_identifier_value_inputs(ValueError, value, possibilities, "foo", upper_bound)
        self._test_integer_identifier_value_inputs(ValueError, value, possibilities, lower_bound, "foo")
        
        # test upper_bound < lower_bound
        self._test_integer_identifier_value_inputs(ValueError, value, possibilities, upper_bound+1, upper_bound)
        
        # test invalid possibilities
        self._test_integer_identifier_value_inputs(ValueError, value, 0, lower_bound, upper_bound)