"""
Multiobjective test problems.

So far, this module only contains a base class for multiobjective test
problems.

"""

import diversipy.subset

from optproblems.base import TestProblem
from optproblems.binary import LeadingOnesTrailingZeros
#from optproblems.zdt import ZDT1, ZDT2, ZDT3, ZDT4, ZDT5, ZDT6



class MultiObjectiveTestProblem(TestProblem):
    """Base class for multiobjective test problems.

    This class only adds functionality to sample the Pareto-front
    relatively uniformly.

    """

    def sample_pareto_front(self, num_points, oversampling_factor=100):
        """Sample the whole Pareto-front.

        This method works by sampling ``num_points * oversampling_factor``
        Pareto-optimal points in the search space, evaluating them, and
        then selecting num_points of them with a uniform distribution in
        objective space by the algorithm in
        :func:`diversipy.subset.psa_partition`.

        Parameters
        ----------
        num_points : int
            The number of points to sample on the Pareto-front.
        oversampling_factor : int or float, optional
            A parameter controlling the uniformity of the points'
            distribution on the Pareto-front.

        Returns
        -------
        selected_solutions : list of Individual

        """
        # generate Pareto-optimal solutions, oversample the search space
        solutions = self.get_optimal_solutions(int(num_points * oversampling_factor))
        for solution in solutions:
            solution.objective_values = self.objective_function(solution.phenome)
        points = [solution.objective_values for solution in solutions]
        clusters = diversipy.subset.psa_partition(points, num_points)
        selected_indices = [cluster.obtain_representative_index() for cluster in clusters]
        if self.num_objectives == 2:
            def sortkey(index):
                return points[index]
            selected_indices.sort(key=sortkey)
        selected_solutions = [solutions[i] for i in selected_indices]
        return selected_solutions
