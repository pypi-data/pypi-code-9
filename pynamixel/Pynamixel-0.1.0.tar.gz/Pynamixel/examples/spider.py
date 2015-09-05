# coding: utf8

# Copyright 2015 Vincent Jacques <vincent@vincent-jacques.net>

r"""
@todoc This is just a stub.
@todoc Add links to the building instructions, maybe a picture or video of the robot.

Cinematic model of a leg
========================

Direct model
------------

@todoc Add a schematic of the leg to explain the direct model.

With :math:`a' = k - a`:

.. math::

    \left\{ \begin{array}{l}
        r = l_1 \cdot \cos(k) + l_2 \cdot \sin(k) + l_3 \cdot \sin(a') + l_4 \cdot \cos(a')
    \\
        z = l_1 \cdot \sin(k) - l_2 \cdot \cos(k) - l_3 \cdot \cos(a') + l_4 \cdot \sin(a')
    \end{array} \right.

Let:

.. math::

    l_{12} = \sqrt{l_1^2 + l_2^2}

    l_{34} = \sqrt{l_3^2 + l_4^2}

    \alpha_{21} = \arctan(l_2 / l_1)

    \alpha_{43} = \arctan(l_4 / l_3)

We obtain:

.. math::

    \left\{ \begin{array}{l}
        r = l_{12} \cdot \cos(k - \alpha_{21}) + l_{34} \cdot \sin(a' + \alpha_{43})
    \\
        z = l_{12} \cdot \sin(k - \alpha_{21}) - l_{34} \cdot \cos(a' + \alpha_{43})
    \end{array} \right.

Let :math:`k' = k - \alpha_{21}` and :math:`a'' = a' + \alpha_{43}`:

.. math::

    \left\{ \begin{array}{l}
        r = l_{12} \cdot \cos(k') + l_{34} \cdot \sin(a'')
    \\
        z = l_{12} \cdot \sin(k') - l_{34} \cdot \cos(a'')
    \end{array} \right.

@todoc Improve readability.

.. plot::

    import math
    import matplotlib.pyplot as plt

    plt.axis('equal')

    l_1 = 5.9
    l_2 = 2.2
    l_3 = 9
    l_4 = 1.4

    l_12 = math.hypot(l_1, l_2)
    l_34 = math.hypot(l_3, l_4)
    alpha_21 = math.atan2(l_2, l_1)
    alpha_43 = math.atan2(l_4, l_3)

    for k in [0, math.pi/20, math.pi/10]:
      for a in [0, math.pi/60, math.pi/30]:
        ap = k - a
        r_1 = l_1 * math.cos(k)
        z_1 = l_1 * math.sin(k)
        r_2 = r_1 + l_2 * math.sin(k)
        z_2 = z_1 - l_2 * math.cos(k)
        r_3 = r_2 + l_3 * math.sin(ap)
        z_3 = z_2 - l_3 * math.cos(ap)
        r_4 = r_3 + l_4 * math.cos(ap)
        z_4 = z_3 + l_4 * math.sin(ap)
        plt.plot([0, r_1, r_2, r_3, r_4], [0, z_1, z_2, z_3, z_4])

        kp = k - alpha_21
        app = ap + alpha_43
        r_2 = l_12 * math.cos(kp)
        z_2 = l_12 * math.sin(kp)
        r_4 = r_2 + l_34 * math.sin(app)
        z_4 = z_2 - l_34 * math.cos(app)
        r = [0, r_2, r_4]
        plt.plot([0, r_2, r_4], [0, z_2, z_4])


Inverse model
-------------

Finding :math:`k'` and :math:`k`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. math::

    \left\{ \begin{array}{l}
        r = l_{12} \cdot \cos(k') + l_{34} \cdot \sin(a'')
    \\
        z = l_{12} \cdot \sin(k') - l_{34} \cdot \cos(a'')
    \end{array} \right.

    \left\{ \begin{array}{l}
        l_{34} \cdot \sin(a'') = r - l_{12} \cdot \cos(k')
    \\
        l_{34} \cdot \cos(a'') = l_{12} \cdot \sin(k') - z
    \end{array} \right.

    \left\{ \begin{array}{l}
        (l_{34} \cdot \sin(a''))^2 = (r - l_{12} \cdot \cos(k'))^2
    \\
        (l_{34} \cdot \cos(a''))^2 = (l_{12} \cdot \sin(k') - z)^2
    \end{array} \right.

    \left\{ \begin{array}{l}
        l_{34}^2 \cdot \sin(a'')^2 = r^2 - 2 \cdot r \cdot l_{12} \cdot \cos(k') + l_{12}^2 \cdot \cos(k')^2
    \\
        l_{34}^2 \cdot \cos(a'')^2 = l_{12}^2 \cdot \sin(k')^2 - 2 \cdot l_{12} \cdot \sin(k') \cdot z + z^2
    \end{array} \right.

    l_{34}^2 \cdot \sin(a'')^2 + l_{34}^2 \cdot \cos(a'')^2 = r^2 - 2 \cdot r \cdot l_{12} \cdot \cos(k') + l_{12}^2 \cdot \cos(k')^2 + l_{12}^2 \cdot \sin(k')^2 - 2 \cdot l_{12} \cdot \sin(k') \cdot z + z^2

    l_{34}^2 \cdot (\sin(a'')^2 + \cos(a'')^2) = r^2 - 2 \cdot r \cdot l_{12} \cdot \cos(k') + l_{12}^2 \cdot (\sin(k')^2 + \cos(k')^2) - 2 \cdot l_{12} \cdot \sin(k') \cdot z + z^2

    l_{34}^2 = r^2 - 2 \cdot r \cdot l_{12} \cdot \cos(k') + l_{12}^2 - 2 \cdot l_{12} \cdot \sin(k') \cdot z + z^2

    r^2 + z^2 + l_{12}^2 - l_{34}^2 = 2 \cdot r \cdot l_{12} \cdot \cos(k') + 2 \cdot l_{12} \cdot \sin(k') \cdot z

    \frac{r^2 + z^2 + l_{12}^2 - l_{34}^2}{2 \cdot l_{12}} = r \cdot \cos(k') + z \cdot \sin(k')

    \frac{r^2 + z^2 + l_{12}^2 - l_{34}^2}{2 \cdot l_{12} \cdot \sqrt{r^2 + z^2}} = \sin(k' + \arctan(r/z))

    \arcsin\left(\frac{r^2 + z^2 + l_{12}^2 - l_{34}^2}{2 \cdot l_{12} \cdot \sqrt{r^2 + z^2}}\right) = k' + \arctan(r/z)

    k' = \arcsin\left(\frac{r^2 + z^2 + l_{12}^2 - l_{34}^2}{2 \cdot l_{12} \cdot \sqrt{r^2 + z^2}}\right) - \arctan(r/z)

    k = \arcsin\left(\frac{r^2 + z^2 + l_{12}^2 - l_{34}^2}{2 \cdot l_{12} \cdot \sqrt{r^2 + z^2}}\right) - \arctan(r/z) + \alpha_{21}

Finding :math:`a''`
~~~~~~~~~~~~~~~~~~~

.. math::

    \left\{ \begin{array}{l}
        r = l_{12} \cdot \cos(k') + l_{34} \cdot \sin(a'')
    \\
        z = l_{12} \cdot \sin(k') - l_{34} \cdot \cos(a'')
    \end{array} \right.

    \left\{ \begin{array}{l}
        l_{12} \cdot \cos(k') = r - l_{34} \cdot \sin(a'')
    \\
        l_{12} \cdot \sin(k') = z + l_{34} \cdot \cos(a'')
    \end{array} \right.

    \left\{ \begin{array}{l}
        (l_{12} \cdot \cos(k'))^2 = (r - l_{34} \cdot \sin(a''))^2
    \\
        (l_{12} \cdot \sin(k'))^2 = (z + l_{34} \cdot \cos(a''))^2
    \end{array} \right.

    \left\{ \begin{array}{l}
        l_{12}^2 \cdot \cos(k')^2 = r^2 - 2 \cdot r \cdot l_{34} \cdot \sin(a'') + l_{34}^2 \cdot \sin(a'')^2
    \\
        l_{12}^2 \cdot \sin(k')^2 = z^2 + 2 \cdot z \cdot l_{34} \cdot \cos(a'') + l_{34}^2 \cdot \cos(a'')^2
    \end{array} \right.

    l_{12}^2 \cdot \cos(k')^2 + l_{12}^2 \cdot \sin(k')^2 = r^2 - 2 \cdot r \cdot l_{34} \cdot \sin(a'') + l_{34}^2 \cdot \sin(a'')^2 + z^2 + 2 \cdot z \cdot l_{34} \cdot \cos(a'') + l_{34}^2 \cdot \cos(a'')^2

    l_{12}^2 \cdot (\cos(k')^2 + \sin(k')^2) = r^2 - 2 \cdot r \cdot l_{34} \cdot \sin(a'') + z^2 + 2 \cdot z \cdot l_{34} \cdot \cos(a'') + l_{34}^2 \cdot (\sin(a'')^2 + \cos(a'')^2)

    l_{12}^2 = r^2 - 2 \cdot r \cdot l_{34} \cdot \sin(a'') + z^2 + 2 \cdot z \cdot l_{34} \cdot \cos(a'') + l_{34}^2

    l_{12}^2 - r^2 - z^2 - l_{34}^2 = 2 \cdot z \cdot l_{34} \cdot \cos(a'') - 2 \cdot r \cdot l_{34} \cdot \sin(a'')

    \frac{l_{12}^2 - r^2 - z^2 - l_{34}^2}{2 \cdot l_{34}} = z \cdot \cos(a'') - r \cdot \sin(a'')

    \frac{l_{12}^2 - r^2 - z^2 - l_{34}^2}{2 \cdot l_{34}} = \sqrt{r^2 + z^2} \cdot \sin(a'' - \arctan(z/r))

    \frac{l_{12}^2 - r^2 - z^2 - l_{34}^2}{2 \cdot l_{34} \cdot \sqrt{r^2 + z^2}} = \sin(a'' - \arctan(z/r))

    \arcsin\left(\frac{l_{12}^2 - r^2 - z^2 - l_{34}^2}{2 \cdot l_{34} \cdot \sqrt{r^2 + z^2}}\right) = a'' - \arctan(z/r)

    a'' = \arcsin\left(\frac{l_{12}^2 - r^2 - z^2 - l_{34}^2}{2 \cdot l_{34} \cdot \sqrt{r^2 + z^2}}\right) + \arctan(z/r)

    a' = \arcsin\left(\frac{l_{12}^2 - r^2 - z^2 - l_{34}^2}{2 \cdot l_{34} \cdot \sqrt{r^2 + z^2}}\right) + \arctan(z/r) - \alpha_{43}

    a = k - \arcsin\left(\frac{l_{12}^2 - r^2 - z^2 - l_{34}^2}{2 \cdot l_{34} \cdot \sqrt{r^2 + z^2}}\right) - \arctan(z/r) + \alpha_{43}

Let's try it
~~~~~~~~~~~~

.. plot::

    import math
    import matplotlib.pyplot as plt

    plt.axis('equal')

    l_1 = 5.9
    l_2 = 2.2
    l_3 = 9
    l_4 = 1.4

    l_12 = math.hypot(l_1, l_2)
    l_34 = math.hypot(l_3, l_4)
    alpha_21 = math.atan2(l_2, l_1)
    alpha_43 = math.atan2(l_4, l_3)

    for r in [6., 8., 10.]:
      for z in [-4., -6., -8.]:
        # @todoc Review previous resolution to explain why it's -arcsin instead of just arcsin
        k = (-math.asin((r ** 2 + z ** 2 + l_12 ** 2 - l_34 ** 2) / (2 * l_12 * math.sqrt(r ** 2 + z ** 2)))) - math.atan(r/z) + alpha_21
        a = k - (-math.asin((l_12 ** 2 - r ** 2 - z ** 2 - l_34 ** 2) / (2 * l_34 * math.sqrt(r ** 2 + z ** 2)))) - math.atan(z/r) + alpha_43

        ap = k - a
        r_1 = l_1 * math.cos(k)
        z_1 = l_1 * math.sin(k)
        r_2 = r_1 + l_2 * math.sin(k)
        z_2 = z_1 - l_2 * math.cos(k)
        r_3 = r_2 + l_3 * math.sin(ap)
        z_3 = z_2 - l_3 * math.cos(ap)
        r_4 = r_3 + l_4 * math.cos(ap)
        z_4 = z_3 + l_4 * math.sin(ap)
        plt.plot([0, r_1, r_2, r_3, r_4], [0, z_1, z_2, z_3, z_4])

        # kp = k - alpha_21
        # app = ap + alpha_43
        # r_2 = l_12 * math.cos(kp)
        # z_2 = l_12 * math.sin(kp)
        # r_4 = r_2 + l_34 * math.sin(app)
        # z_4 = z_2 - l_34 * math.cos(app)
        # plt.plot([0, r_2, r_4], [0, z_2, z_4])
"""

import math
import time

import Pynamixel


class Leg(object):
    l_1 = 6.1
    l_2 = 2.4
    l_3 = 9.3
    l_4 = 1.3

    l_12 = math.hypot(l_1, l_2)
    l_34 = math.hypot(l_3, l_4)
    alpha_21 = math.atan2(l_2, l_1)
    alpha_43 = math.atan2(l_4, l_3)

    def __init__(self, hip, knee, ankle):
        self.hip = hip
        self.knee = knee
        self.ankle = ankle

    def set_rz(self, r, z):
        k, a = self.__compute_ka(float(r), float(z))
        self.knee.goal_position = k
        self.ankle.goal_position = a

    def __compute_ka(self, r, z):
        k = math.pi - math.asin((r ** 2 + z ** 2 + self.l_12 ** 2 - self.l_34 ** 2) / (2 * self.l_12 * math.sqrt(r ** 2 + z ** 2))) - math.atan2(r, z) + self.alpha_21
        a = k + math.asin((self.l_12 ** 2 - r ** 2 - z ** 2 - self.l_34 ** 2) / (2 * self.l_34 * math.sqrt(r ** 2 + z ** 2))) - math.atan2(z, r) + self.alpha_43
        while k > math.pi: k -= 2 * math.pi
        while k < -math.pi: k += 2 * math.pi
        while a > math.pi: a -= 2 * math.pi
        while a < -math.pi: a += 2 * math.pi
        return k, a

    def get_rz(self):
        return self.__compute_rz(self.knee.goal_position, self.ankle.goal_position)

    def __compute_rz(self, k, a):
        ap = k - a
        kp = k - self.alpha_21
        app = ap + self.alpha_43
        r = self.l_12 * math.cos(kp) + self.l_34 * math.sin(app)
        z = self.l_12 * math.sin(kp) - self.l_34 * math.cos(app)
        return r, z


class Spider(object):
    def __init__(self, hardware):
        self.system = Pynamixel.System(Pynamixel.Bus(hardware))
        for i in range(1, 19):
            self.system.add_device(Pynamixel.devices.AX12, i)

        POSITION_22_DEGREES = 0x24A
        POSITION_M22_DEGREES = 0x1B4
        POSITION_45_DEGREES = 0x298
        POSITION_M45_DEGREES = 0x166
        POSITION_70_DEGREES = 0x2EE
        POSITION_M70_DEGREES = 0x110
        POSITION_90_DEGREES = 0x332
        POSITION_M90_DEGREES = 0x0CC

        RADIANS_M90_DEGREES = 2 * math.pi * -90 / 360
        RADIANS_70_DEGREES = 2 * math.pi * 70 / 360

        self.right_front_leg = Leg(
            Pynamixel.concepts.Joint(self.system.get_device(1), {POSITION_M90_DEGREES: -1, POSITION_M45_DEGREES: 1}),
            Pynamixel.concepts.Joint(self.system.get_device(3), {POSITION_90_DEGREES: RADIANS_M90_DEGREES, POSITION_M70_DEGREES: RADIANS_70_DEGREES}),
            Pynamixel.concepts.Joint(self.system.get_device(5), {POSITION_90_DEGREES: RADIANS_M90_DEGREES, POSITION_M70_DEGREES: RADIANS_70_DEGREES}),
        )

        self.right_middle_leg = Leg(
            Pynamixel.concepts.Joint(self.system.get_device(7), {POSITION_M22_DEGREES: -1, POSITION_22_DEGREES: 1}),
            Pynamixel.concepts.Joint(self.system.get_device(9), {POSITION_M90_DEGREES: RADIANS_M90_DEGREES, POSITION_70_DEGREES: RADIANS_70_DEGREES}),
            Pynamixel.concepts.Joint(self.system.get_device(11), {POSITION_M90_DEGREES: RADIANS_M90_DEGREES, POSITION_70_DEGREES: RADIANS_70_DEGREES}),
        )

        self.right_rear_leg = Leg(
            Pynamixel.concepts.Joint(self.system.get_device(13), {POSITION_45_DEGREES: -1, POSITION_90_DEGREES: 1}),
            Pynamixel.concepts.Joint(self.system.get_device(15), {POSITION_M90_DEGREES: RADIANS_M90_DEGREES, POSITION_70_DEGREES: RADIANS_70_DEGREES}),
            Pynamixel.concepts.Joint(self.system.get_device(17), {POSITION_M90_DEGREES: RADIANS_M90_DEGREES, POSITION_70_DEGREES: RADIANS_70_DEGREES}),
        )

        self.left_front_leg = Leg(
            Pynamixel.concepts.Joint(self.system.get_device(2), {POSITION_90_DEGREES: -1, POSITION_45_DEGREES: 1}),
            Pynamixel.concepts.Joint(self.system.get_device(4), {POSITION_M90_DEGREES: RADIANS_M90_DEGREES, POSITION_70_DEGREES: RADIANS_70_DEGREES}),
            Pynamixel.concepts.Joint(self.system.get_device(6), {POSITION_M90_DEGREES: RADIANS_M90_DEGREES, POSITION_70_DEGREES: RADIANS_70_DEGREES}),
        )

        self.left_middle_leg = Leg(
            Pynamixel.concepts.Joint(self.system.get_device(8), {POSITION_22_DEGREES: -1, POSITION_M22_DEGREES: 1}),
            Pynamixel.concepts.Joint(self.system.get_device(10), {POSITION_90_DEGREES: RADIANS_M90_DEGREES, POSITION_M70_DEGREES: RADIANS_70_DEGREES}),
            Pynamixel.concepts.Joint(self.system.get_device(12), {POSITION_90_DEGREES: RADIANS_M90_DEGREES, POSITION_M70_DEGREES: RADIANS_70_DEGREES}),
        )

        self.left_rear_leg = Leg(
            Pynamixel.concepts.Joint(self.system.get_device(14), {POSITION_M45_DEGREES: -1, POSITION_M90_DEGREES: 1}),
            Pynamixel.concepts.Joint(self.system.get_device(16), {POSITION_90_DEGREES: RADIANS_M90_DEGREES, POSITION_M70_DEGREES: RADIANS_70_DEGREES}),
            Pynamixel.concepts.Joint(self.system.get_device(18), {POSITION_90_DEGREES: RADIANS_M90_DEGREES, POSITION_M70_DEGREES: RADIANS_70_DEGREES}),
        )

        self.left_trileg = [self.right_middle_leg, self.left_front_leg, self.left_rear_leg]
        self.right_trileg = [self.left_middle_leg, self.right_front_leg, self.right_rear_leg]

    def walk(self):
        try:
            # @todo Provide better support for broadcasted (registered) writes. (Specificaly: "0x20" and "16 bits" is already known in AX12.goal_position => DRY)
            self.system.bus.broadcast(Pynamixel.instructions.WriteData(0x20, [128, 0]))  # Moving speed
            amp = 0.5
            while True:
                self.__go(4, -7, -amp, self.left_trileg)  # Raise left
                self.__go(4, -10, -amp, self.right_trileg, wait=False)  # Move right back
                self.__go(4, -7, amp, self.left_trileg)  # Move left forward
                self.__go(4, -10, amp, self.left_trileg)  # Lower left
                self.__go(4, -7, -amp, self.right_trileg)  # Raise right
                self.__go(4, -10, -amp, self.left_trileg, wait=False)  # Move left back
                self.__go(4, -7, amp, self.right_trileg)  # Move right forward
                self.__go(4, -10, amp, self.right_trileg)  # Lower right
        finally:
            # @todo A context manager doing just that
            self.system.bus.broadcast(Pynamixel.instructions.WriteData(0x18, 0))  # Turn torque off

    def __go(self, r, z, t, legs, wait=True):
        with self.system.registered_writes:
            for leg in legs:
                leg.set_rz(r, z)
                leg.hip.goal_position = t
        if wait:
            self.__wait_until_still()

    def __wait_until_still(self):
        # @todo Should this be a utility in Pynamixel?
        errors = 0
        while True:
            try:
                for i in range(1, 19):
                    moving = self.system.get_device(i).moving.read()
                    errors = 0
                    if moving != 0:
                        time.sleep(0.2)
                        break
                else:
                    return
            except Pynamixel.CommunicationError:
                errors += 1
                if errors >= 10:
                    raise


if __name__ == "__main__":
    # @todo Use the "hardware from config" facility when implemented
    # hardware = Pynamixel.hardwares.USB2AX("COM3", 1000000)
    hardware = Pynamixel.hardwares.USB2AX("/dev/ttyACM0", 1000000)
    spider = Spider(hardware)
    print("Interrupt with Ctrl+C")
    spider.walk()
