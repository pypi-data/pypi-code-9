"""

create_table2 produces some results from table 2 found in the paper
"""
import pandas as pd


def get_table2():
    import dream7_challenge1
    d = dream7_challenge1.D7C1(path_to_files='parest')
    d.compute_parameters_distances()
    for k, v in d.parameters_distances.items():
        print(k, v)

    df = pd.DataFrame(d.parameters_distances)
    df.index = ['distance']
    df = df.transpose()
    df = df.sort('distance')
    return df
