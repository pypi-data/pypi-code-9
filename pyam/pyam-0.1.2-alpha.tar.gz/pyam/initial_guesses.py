import numpy as np

"""
Class for computing initial guesses for the various solvers.

@author : David R. Pugh
@date : 2015-07-14

"""
import pycollocation


class OrthogonalPolynomialInitialGuess(object):
    """
    Class for generating initial guesses for solving an assortative matching
    boundary value problem using an orthognal polynomial collocation solver.

    """

    def __init__(self, solver):
        """
        Create an instance of the OrthogonalPolynomialInitialGuess class.

        Parameters
        ----------
        solver : pycollocation.OrthogonalPolynomialSolver

        """
        self.solver = self._validate_solver(solver)

    def _initial_mus(self, xs, exp):
        """
        Return values for mu given some x values and an exponent.

        Parameters
        ----------
        xs : numpy.ndarray
        exp: float

        Notes
        -----
        Theory tells us that the function :math: `\mu(x)` must be monotonically
        increasing (decreasing) if the model exhibits positive (negative)
        assortative matching in equilibriu. We therefore guess that mu(x) is a
        linear transform of some power function where the intercept and slope
        of the linear transform are chosen so that resulting function satisfies
        the boundary conditions.

        """
        input1 = self.solver.problem.input1
        input2 = self.solver.problem.input2

        slope = (input2.upper - input2.lower) / (input1.upper**exp - input1.lower**exp)
        if self.solver.problem.assortativity == "positive":
            intercept = input2.lower - slope * input1.lower**exp
        else:
            slope = -slope
            intercept = input2.upper - slope * input1.lower**exp

        return intercept + slope * xs**exp

    def _initial_guess_mu(self, xs, mus, kind, degree, domain):
        """Fit basis polynomial for mu of a certain kind, degree and domain."""
        coefs = self.solver._basis_polynomial_coefs({'mu': degree})
        basis_func = self.solver._basis_function_factory(coefs['mu'], kind, domain)
        return basis_func.fit(xs, mus, degree, domain)

    def _initial_guess_theta(self, xs, thetas, kind, degree, domain):
        """Fit basis polynomial for theta of a certain kind, degree and domain."""
        coefs = self.solver._basis_polynomial_coefs({'theta': degree})
        basis_func = self.solver._basis_function_factory(coefs['theta'], kind, domain)
        return basis_func.fit(xs, thetas, degree, domain)

    def _initial_thetas(self, xs, initial_guess_mu):
        """Initial guess for theta(x) should be consistent with mu(x) guess."""
        input1 = self.solver.problem.input1
        input2 = self.solver.problem.input2

        H = input1.evaluate_pdf(xs) / input2.evaluate_pdf(initial_guess_mu(xs))
        if self.solver.problem.assortativity == "positive":
            thetas = (H / initial_guess_mu.deriv()(xs))
        else:
            thetas = -(H / initial_guess_mu.deriv()(xs))
        return thetas

    @staticmethod
    def _validate_solver(solver):
        """Validates the solver attribute."""
        if not isinstance(solver, pycollocation.OrthogonalPolynomialSolver):
            raise ValueError
        else:
            return solver

    def compute_initial_guess(self, kind, degrees, N=1000, exp=1.0):
        """
        Compute initial orthogonal polynomials.

        Parameters
        ----------
        kind : string
        degrees : dict
        N : int
        exp : float (default=1.0)

        """
        # get domain values
        domain = [self.solver.problem.input1.lower,
                  self.solver.problem.input1.upper]
        xs = np.linspace(domain[0], domain[1], N)

        # initial guess for mu is some power function
        mus = self._initial_mus(xs, exp)
        initial_guess_mu = self._initial_guess_mu(xs, mus, kind, degrees['mu'], domain)

        # initial guess for theta depends on guess for mu
        thetas = self._initial_thetas(xs, initial_guess_mu)
        initial_guess_theta = self._initial_guess_theta(xs, thetas, kind, degrees['theta'], domain)

        return {'mu': initial_guess_mu, 'theta': initial_guess_theta}
