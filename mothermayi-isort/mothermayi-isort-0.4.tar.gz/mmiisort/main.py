from isort import SortImports
import mothermayi.colors
import mothermayi.errors

def plugin():
    return {
        'name'          : 'isort',
        'pre-commit'    : pre_commit,
    }

def do_sort(filename):
    results = SortImports(filename)
    return results.in_lines != results.out_lines

def get_status(had_changes):
    return mothermayi.colors.red('unsorted') if had_changes else mothermayi.colors.green('sorted')

def pre_commit(config, staged):
    changes = [do_sort(filename) for filename in staged]
    messages = [get_status(had_change) for had_change in changes]
    lines = ["  {0:<30} ... {1:<10}".format(filename, message) for filename, message in zip(staged, messages)]
    result = "\n".join(lines)
    if any(changes):
        raise mothermayi.errors.FailHook(result)
    return result
