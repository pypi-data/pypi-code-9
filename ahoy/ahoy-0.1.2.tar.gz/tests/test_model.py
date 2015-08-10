import numpy as np
from ahoy import turners
from ahoy.model import Model
import test


class TestModel(test.TestBase):

    def test_model_random_seeding(self):
        model_kwargs = {
            'seed': 1,
            'dt': 0.01,

            'n': 10,
            'dim': 2,
            # Must have aligned flag False to test uniform directions function.
            'aligned_flag': False,

            'spatial_flag': False,

            'chi': 0.1,
            'onesided_flag': True,

            # Must have tumbling to test tumbling function.
            'tumble_flag': True,
            'p_0': 1.3,
            'tumble_chemo_flag': True,

            # Must have rotational diffusion to test rot diff function.
            'rotation_flag': True,
            'Dr_0': 1.3,
            'rotation_chemo_flag': True,
        }

        num_iterations = 100

        def get_model(npy_seed):
            np.random.seed(npy_seed)
            model = Model(**model_kwargs)
            for _ in range(num_iterations):
                model.iterate()
            return model

        model_1 = get_model(2)
        model_2 = get_model(3)

        self.assertTrue(np.allclose(model_1.ships.agents.directions.u,
                                    model_2.ships.agents.directions.u))

    def test_spatial_model_random_seeding(self):
        model_kwargs = {
            'seed': 1,
            'dt': 0.01,

            'dim': 2,
            'n': 10,
            # Must have aligned flag False to test uniform directions function.
            'aligned_flag': False,

            'spatial_flag': True,
            'periodic_flag': True,
            'v_0': 1.5,
            # Must have at least one periodic axis to test uniform points
            # function.
            'L': np.array([2.0, 2.2]),
            'origin_flags': np.array([False, False]),

            'chi': 0.1,
            'onesided_flag': True,

            # Must have tumbling to test tumbling function.
            'tumble_flag': True,
            'p_0': 1.3,
            'tumble_chemo_flag': True,

            # Must have rotational diffusion to test rot diff function.
            'rotation_flag': True,
            'Dr_0': 1.3,
            'rotation_chemo_flag': True,

            'temporal_chemo_flag': True,
            'dt_mem': 0.05,
            't_mem': 5.0,

            'pore_flag': True,
            'pore_turner': turners.AlignTurner(),
            'pore_R': 0.1,
            'pore_pf': 0.1,
        }

        num_iterations = 100

        def get_model(npy_seed):
            np.random.seed(npy_seed)
            model = Model(**model_kwargs)
            for _ in range(num_iterations):
                model.iterate()
            return model

        model_1 = get_model(2)
        model_2 = get_model(3)

        self.assertTrue(np.allclose(model_1.ships.agents.positions.r,
                                    model_2.ships.agents.positions.r))
        self.assertTrue(np.allclose(model_1.ships.agents.directions.u,
                                    model_2.ships.agents.directions.u))

    def test_c_field_model_random_seeding(self):
        model_kwargs = {
            'seed': 1,
            'dt': 0.01,

            'dim': 2,
            'rho_0': 10.0,
            # Must have aligned flag False to test uniform directions function.
            'aligned_flag': False,

            'spatial_flag': True,
            'periodic_flag': True,
            'v_0': 1.5,
            'L': np.array([2.0, 2.2]),
            'origin_flags': np.array([False, False]),

            'chi': 0.3,
            'onesided_flag': True,

            # Must have tumbling to test tumbling function.
            'p_0': 1.3,
            'tumble_flag': True,
            'tumble_chemo_flag': True,

            # Must have rotational diffusion to test rot diff function.
            'rotation_flag': True,
            'Dr_0': 1.3,
            'rotation_chemo_flag': True,

            'temporal_chemo_flag': True,
            'dt_mem': 0.1,
            't_mem': 5.0,

            'pore_flag': True,
            'pore_turner': turners.AlignTurner(),
            'pore_R': 0.2,
            'pore_pf': 0.1,

            'c_dx': 0.2,
            'c_D': 10.0,
            'c_delta': 1000.0,
            'c_0': 1.3,
        }

        num_iterations = 100

        def get_model(npy_seed):
            np.random.seed(npy_seed)
            model = Model(**model_kwargs)
            for _ in range(num_iterations):
                model.iterate()
            return model

        model_1 = get_model(2)
        model_2 = get_model(3)

        self.assertTrue(np.allclose(model_1.ships.agents.positions.r,
                                    model_2.ships.agents.positions.r))
        self.assertTrue(np.allclose(model_1.ships.agents.directions.u,
                                    model_2.ships.agents.directions.u))
