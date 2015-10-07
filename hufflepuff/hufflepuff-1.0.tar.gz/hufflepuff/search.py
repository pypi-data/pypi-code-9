import json
import subprocess

def get_initial_states(command):
    stdout = subprocess.check_output(command, shell=True)
    return [
        json.loads(line)
        for line in stdout.split('\n')
        if line
    ]

def immutable(obj):
    # This only supports objects needed for JSON.
    if isinstance(obj, list):
        return tuple(immutable(item) for item in obj)
    if isinstance(obj, dict):
        return immutable(obj.items())
    return obj

def _uniq(items):
    # This has an underscore because it has weird semantics,
    # nothing more.
    seen = set()
    for item in items:
        key = immutable(item[1])
        if key not in seen:
            yield item
            seen.add(key)

class Searcher(object):
    def __init__(
        self,
        states, mutator, scorer,
        beam_width,
        expand_mantissa,
        expand_multiplier,
        target,
    ):
        self.states = states
        self.mutator = mutator
        self.scorer = scorer

        self.beam_width = beam_width
        self.expand_mantissa = expand_mantissa
        self.expand_multiplier = expand_multiplier
        assert target in ('min', 'max')
        self.target = target

        # This keeps track of the best states ever seen.
        self.best = self.score_states(states)[:self.beam_width]

    def update_best(self, scores):
        best = _uniq(self.best + scores)
        best = sorted(best, reverse=self.target == 'max')
        self.best = best[:self.beam_width]

    def expand_states(self):
        to_mutate = []
        for j, state in enumerate(self.states):
            n = (self.expand_mantissa ** -j) * self.expand_multiplier
            for k in xrange(int(n) or 1):
                to_mutate.append(state)
        return list(self.mutator.map_unordered(to_mutate))

    def score_states(self, states):
        return sorted(
            zip(
                self.scorer.map(states),
                states,
            ),
            reverse=self.target == 'max',
        )

    def step(self):
        expanded = self.expand_states()
        scores = self.score_states(expanded)
        scores = scores[:self.beam_width]
        self.update_best(scores)
        self.states = [state for _, state in scores]
        return scores
