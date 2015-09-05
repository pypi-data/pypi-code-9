# coding: utf8

# Copyright 2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest

import MockMockMock


class Interpolator(object):
    def __init__(self, points):
        assert len(points) >= 2
        points = sorted(points.items())
        self.__domain = (points[0][0], points[-1][0])
        self.__intervals = []
        for i in range(len(points) - 1):
            self.__intervals.append((points[i], points[i + 1]))

    @property
    def domain(self):
        return self.__domain

    def __call__(self, point):
        # @todo Binary search
        for (lo, lo_val), (hi, hi_val) in self.__intervals:  
            if point < hi:
                return lo_val + (hi_val - lo_val) * (point - lo) / (hi - lo)
        return lo_val + (hi_val - lo_val) * (point - lo) / (hi - lo)


class InterpolatorTestCase(unittest.TestCase):
    def setUp(self):
        self.interpolator = Interpolator({10: 100, 20: 200, 30: 400})

    def test_domain(self):
        self.assertEqual(self.interpolator.domain, (10, 30))

    def test_exact_points(self):
        self.assertEqual(self.interpolator(10), 100)
        self.assertEqual(self.interpolator(20), 200)
        self.assertEqual(self.interpolator(30), 400)

    def test_interpolated_points(self):
        self.assertEqual(self.interpolator(12), 120)
        self.assertEqual(self.interpolator(15), 150)
        self.assertEqual(self.interpolator(17), 170)
        self.assertEqual(self.interpolator(22), 240)
        self.assertEqual(self.interpolator(25), 300)
        self.assertEqual(self.interpolator(27), 340)

    def test_extrapolated_points(self):
        self.assertEqual(self.interpolator(6), 60)
        self.assertEqual(self.interpolator(8), 80)
        self.assertEqual(self.interpolator(32), 440)
        self.assertEqual(self.interpolator(34), 480)


class Joint(object):
    """
    @todoc
    """
    def __init__(self, actuator, positions):
        """
        positions: dict from [0, 0x3FF] to your logical angle unit (hint: degrees, radians, [0, 1], etc. But be consistent). Must be monotonous (else, weird weird results).
        Intermediate positions are interpolated linearly. Positions outside are errors in set_position, and extrapolated linearly in get_position.
        """
        self.__actuator = actuator
        assert all(isinstance(k, int) and 0 <= k <= 0x3FF for k in positions.keys())
        self.__physical_to_logical = Interpolator({k: float(v) for k, v in positions.items()})
        self.__logical_to_phyical = Interpolator({float(v): k for k, v in positions.items()})

    @property
    def goal_position(self):
        """
        @todoc
        """
        return self.__physical_to_logical(self.__actuator.goal_position.read())

    @goal_position.setter
    def goal_position(self, position):
        lo, hi = self.__logical_to_phyical.domain
        assert lo <= position <= hi  # @todo Remove asserts and raise proper exceptions
        self.__actuator.goal_position.write(int(self.__logical_to_phyical(float(position))))

    def relax(self):
        """
        @todoc
        """
        self.__actuator.torque_enable.write(0)


class JointTestCase(unittest.TestCase):
    def setUp(self):
        super(JointTestCase, self).setUp()
        self.mocks = MockMockMock.Engine()
        self.actuator = self.mocks.create("actuator")
        self.joint = Joint(self.actuator.object, {0x100: -1, 0x200: 0, 0x300: 1})

    def tearDown(self):
        self.mocks.tearDown()
        super(JointTestCase, self).tearDown()

    def test_set(self):
        goal = self.mocks.create("goal")
        self.actuator.expect.goal_position.andReturn(goal.object)
        goal.expect.write(0x200)
        self.joint.goal_position = 0

    def test_get(self):
        goal = self.mocks.create("goal")
        self.actuator.expect.goal_position.andReturn(goal.object)
        goal.expect.read().andReturn(0x200)
        self.assertEqual(self.joint.goal_position, 0)
