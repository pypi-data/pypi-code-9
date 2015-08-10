import numpy as np
from ahoy import obstructors, turners
import test


class TestPorousObstructor(test.TestBase):

    def test_random_seeding(self):
        obstructor_kwargs = {
            'turner': turners.ReflectTurner(),
            'R': 50.0,
            'L': np.array([200.0, 200.0]),
            'pf': 0.4,
            'periodic_flag': True,
        }

        rng_seed = 1

        def get_obstructor(npy_seed):
            np.random.seed(npy_seed)
            rng = np.random.RandomState(rng_seed)
            obstructor = obstructors.PorousObstructor(rng=rng,
                                                      **obstructor_kwargs)
            return obstructor

        obstructor_1 = get_obstructor(2)
        obstructor_2 = get_obstructor(3)

        self.assertTrue(np.allclose(obstructor_1.R, obstructor_2.R))
        self.assertTrue(np.allclose(obstructor_1.L, obstructor_2.L))
        self.assertTrue(np.allclose(obstructor_1.rs, obstructor_2.rs))
