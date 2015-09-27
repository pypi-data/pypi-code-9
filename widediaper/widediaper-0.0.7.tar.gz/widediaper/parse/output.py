import re


def remove_repl_output_prefix(output):

    r_repl_output_prefix = re.compile("^\s*\[\d+\]\s*", flags=re.MULTILINE)

    return re.sub(r_repl_output_prefix, "", output).strip()



def return_correct_type(pruned_repl_string):

    try:
        return int(pruned_repl_string)
    except ValueError:
        pass
    try:
        return float(pruned_repl_string)
    except ValueError:
        pass

    return pruned_repl_string
