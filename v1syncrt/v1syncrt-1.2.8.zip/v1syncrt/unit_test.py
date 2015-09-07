__author__ = 'mjhunick'

import unittest
from behave.parser import parse_feature
from helpers import *


class TestHelpers(unittest.TestCase):
    def setUp(self):
        pass

    def test_is_reg_test_number(self):
        returns_true = ['RT-0', 'RT-123456789123456789', 'RT-9']
        returns_false = [' RT-0', 'RT-', 'RT1', 'RS-123', 'T-22', 'rt-2']
        for tag in returns_true:
            self.assertTrue(is_reg_test_number(tag))
        for tag in returns_false:
            self.assertFalse(is_reg_test_number(tag))

    def test_is_reg_suite_number(self):
        returns_true = ['RS-0', 'RS-123456789123456789', 'RS-9']
        returns_false = [' RS-0', 'RS-', 'RS1', 'RT-123', 'S-22', 'rs-2']
        for tag in returns_true:
            self.assertTrue(is_reg_suite_number(tag))
        for tag in returns_false:
            self.assertFalse(is_reg_suite_number(tag))

    def test_is_test_set_number(self):
        returns_true = ['TS-0', 'TS-123456789123456789', 'TS-9']
        returns_false = [' TS-0', 'TS-', 'TS1', 'RS-123', 'S-22', 'ts-2']
        for tag in returns_true:
            self.assertTrue(is_test_set_number(tag))
        for tag in returns_false:
            self.assertFalse(is_test_set_number(tag))

    def test_feature_to_string(self):
        feature_str = u'''\
@T-1 @t2
Feature: asfrwef

    Background: ege g wg we
        Given wetiwep   ef 2
        And efoefqo wef

    @etweg @erherh
    Scenario: gwg wghwghwg23 f 4 4
        Given 23t434  we
        When weotjgweopw weg3 " t32"
        Then qwrdv f w    we
        And dqwdqw    wwww 2 s

    Scenario Outline:
        Given <abc>
        Then <def>
        Examples: asd
            | abc | def   |
            | w   | wdwdw |
        Examples:\
'''
        self.assertEqual(feature_to_string(parse_feature(feature_str)), feature_str)


class TestFeatureWrapper(unittest.TestCase):
    def setUp(self):
        feature_filename = 'UNITTEST.feature'
        feature_str = u'''\
@T-1 @t2
Feature: asfrwef

    Background: ege g wg we
        Given wetiwep   ef 2
        And efoefqo wef

    @etweg @erherh
    Scenario: gwg wghwghwg23 f 4 4
        Given 23t434  we
        When weotjgweopw weg3 " t32"
        Then qwrdv f w    we
        And dqwdqw    wwww 2 s

    @asdasd
    Scenario Outline:
        Given <abc>
        Then <def>
        Examples: asd
            | abc | def   |
            | w   | wdwdw |
        Examples:\
'''
        with open(feature_filename, 'w') as f:
            f.write(feature_str)
        self.feature = FeatureWrapper(feature_filename)

    def tearDown(self):
        os.remove(self.feature.filename)

    def test_to_string(self):
        with open(self.feature.filename) as f:
            self.assertEqual(f.read(), self.feature.to_string())

    def test_dump_to_file(self):
        self.feature.lines += ['# HOLA']
        self.feature.dump_to_file()
        with open(self.feature.filename) as f:
            self.assertEqual(f.read(), self.feature.to_string())

    def test_add_scenario(self):
        scenario_str = u'''\
    @asd @qwe
    Scenario: ewfwegwg
        Given fewig ri
        When werignwgiwe
        Then ejeqwgijqegioqj egowej egg
        And eewg g   g g\
'''
        feature_str = 'Feature:\n' + scenario_str
        feat2 = parse_feature(feature_str)
        self.feature.add_scenario(feat2.scenarios[0])
        self.assertIn(scenario_str, self.feature.to_string())
        with open(self.feature.filename) as f:
            self.assertEqual(f.read(), self.feature.to_string())

    def test_remove_scenarios_with_tags(self):
        self.feature.remove_scenarios_with_tags(['etweg', 'asdasd'])
        self.assertEqual(self.feature.scenarios, [])
        self.assertEqual(parse_file(self.feature.filename).scenarios, []) # FIXME se rompe con scenario outline


if __name__ == '__main__':
    unittest.main(verbosity=2)