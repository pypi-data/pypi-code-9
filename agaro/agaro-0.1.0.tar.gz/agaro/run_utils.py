from __future__ import print_function, division
from functools import partial
from ciabatta.parallel import run_func
from agaro import runner


def run_model(t_output_every, output_dir=None, m=None, force_resume=True,
              **iterate_args):
    """Convenience function to combine making a Runner object, and
    running it for some time.

    Parameters
    ----------
    m: Model
        Model to run.
    iterate_args:
        Arguments to pass to :meth:`Runner.iterate`.
    Others:
        see :class:`Runner`.

    Returns
    -------
    r: Runner
        runner object after it has finished running for the required time.
    """
    r = runner.Runner(output_dir, m, force_resume)
    print(r)
    r.iterate(t_output_every=t_output_every, **iterate_args)
    return r


def resume_runs(dirnames, t_output_every, t_upto, parallel=False):
    """Resume many models, and run.

    Parameters
    ----------
    dirnames: list[str]
        List of output directory paths from which to resume.
    output_every: int
        see :class:`Runner`.
    t_upto: float
        Run each model until the time is equal to this
    parallel: bool
        Whether or not to run the models in parallel, using the Multiprocessing
        library. If `True`, the number of concurrent tasks will be equal to
        one less than the number of available cores detected.
    """
    run_model_partial = partial(run_model, t_output_every, force_resume=True,
                                t_upto=t_upto)
    run_func(run_model_partial, dirnames, parallel)


class _TaskRunner(object):

    """Replacement for a closure, which I would use if
    the multiprocessing module supported them.

    Imagine `__init__` is the captured outside state,
    and `__call__` is the closure body.
    """

    def __init__(self, ModelClass, t_output_every, t_upto, force_resume=True):
        self.ModelClass = ModelClass
        self.t_output_every = t_output_every
        self.t_upto = t_upto
        self.force_resume = force_resume

    def __call__(self, model_kwargs):
        m = self.ModelClass(**model_kwargs)
        run_model(self.t_output_every, m=m, force_resume=self.force_resume,
                  t_upto=self.t_upto)


def run_kwarg_scan(ModelClass, model_kwarg_sets,
                   t_output_every, t_upto,
                   force_resume=True, parallel=False):
    """Run many models with the same parameters but variable `field`.

    For each `val` in `vals`, a new model will be made, and run up to a time.
    The output directory is automatically generated from the model arguments.

    Parameters
    ----------
    ModelClass: type
        A class or factory function that returns a model object by
        calling `ModelClass(model_kwargs)`
    model_kwarg_sets: list[dict]
        List of argument sets, each of which can instantiate a model.
    t_output_every: float
        see :class:`Runner`.
    t_upto: float
        Run each model until the time is equal to this
    parallel: bool
        Whether or not to run the models in parallel, using the Multiprocessing
        library. If `True`, the number of concurrent tasks will be equal to
        one less than the number of available cores detected.
    """
    task_runner = _TaskRunner(ModelClass, t_output_every, t_upto, force_resume)
    run_func(task_runner, model_kwarg_sets, parallel)


def run_field_scan(ModelClass, model_kwargs, t_output_every, t_upto, field,
                   vals, force_resume=True, parallel=False):
    """Run many models with a range of parameter sets.

    Parameters
    ----------
    ModelClass: callable
        A class or factory function that returns a model object by
        calling `ModelClass(model_kwargs)`
    model_kwargs: dict
        See `ModelClass` explanation.
    t_output_every: float
        see :class:`Runner`.
    t_upto: float
        Run each model until the time is equal to this
    field: str
        The name of the field to be varied, whose values are in `vals`.
    vals: array_like
        Iterable of values to use to instantiate each Model object.
    parallel: bool
        Whether or not to run the models in parallel, using the Multiprocessing
        library. If `True`, the number of concurrent tasks will be equal to
        one less than the number of available cores detected.
    """
    model_kwarg_sets = [dict(model_kwargs, field=val) for val in vals]
    run_kwarg_scan(ModelClass, model_kwarg_sets,
                   t_output_every, t_upto, force_resume, parallel)
