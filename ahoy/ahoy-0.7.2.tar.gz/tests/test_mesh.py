import numpy as np
from ahoy import mesh
import test


class TestUniformMesh1D(test.TestBase):
    dim = 1
    L = np.array([1.8])
    dx = 0.1

    def test_uniform_mesh(self):
        msh = mesh.uniform_mesh_factory(self.L, self.dx)
        for i_dim in range(self.dim):
            self.assertTrue(msh.cellCenters[i_dim, :].value.max() <
                            self.L[i_dim] / 2.0)
            self.assertTrue(msh.cellCenters[i_dim, :].value.min() >
                            -self.L[i_dim] / 2.0)


class TestUniformMesh2D(TestUniformMesh1D):
    dim = 2
    L = np.array([1.7, 3.0])


class TestPorousMesh(test.TestBase):

    def test_porous_random_seeding(self):
        '''Test the reproducibility of the meshing algorithm.'''

        L = np.array([2.0, 2.0])
        R = 0.1
        dx = 0.1
        rs = np.array([
            [-0.5, 0.5],
            [0.0, 0.0],
            [0.1, 0.4],
            [0.88, 0.88],
            [0.88, 0.0],
        ])

        np.random.seed(2)
        mesh_1 = mesh.porous_mesh_factory(rs, R, dx, L)

        np.random.seed(3)
        mesh_2 = mesh.porous_mesh_factory(rs, R, dx, L)

        self.assertTrue(np.allclose(mesh_1.cellCenters.value,
                                    mesh_2.cellCenters.value))
