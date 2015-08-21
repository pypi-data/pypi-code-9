from traits.api import Float, HasTraits, Property, Range, Int

module_trait = Float

long_module_trait = Range(
    low=0.2,
    high=34)


def dummy_function():
    pass


class Dummy(HasTraits):

    trait_1 = Float

    trait_2 = Property(
        Float,
        depends_on='trait_1')

    not_trait = 2

    trait_3 = Property(
        Float,  # first comment
        depends_on='trait_4')

    trait_4 = Float  # second comment


class Dummy1(HasTraits):

    trait_1 = Int

    trait_2 = Property(
        Int,
        depends_on='trait_1')

    not_trait = 2
