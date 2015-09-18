"""
Copyright (C) 2013-2015 Stefan Pfenninger.
Licensed under the Apache 2.0 License (see LICENSE file).

time_funcs.py
~~~~~~~~~~~~~

A time function must take ``data`` and ``timesteps`` and optionally any
additional keyword arguments. It modifies the timesteps in the data and
returns the timestep weights for the modified timesteps.

"""

import pandas as pd

from . import time_tools


def kmeans_typical_days(data, timesteps, variable, days=5):
    import scipy.cluster.vq as vq

    # FIXME need to make the hardcoded timestep lengths dynamic
    # and dependent on ts_length_static or whatever

    if timesteps is None:
        timesteps = data._dt.index  # All timesteps

    df = data.get_key(variable)

    # Get a (m,24) matrix where m is number of days in the matrix
    d = df.loc[timesteps, :].sum(1)
    d = d.reshape(len(d) / 24, 24)
    # Run k-means algorithm for the desired number of days (clusters)
    centroids, distortion = vq.kmeans(d, days)

    # Determine the cluster membership of each day
    day_clusters = vq.vq(d, centroids)[0]

    # Create mapping of timesteps to clusters
    ts_clusters = pd.Series(day_clusters, index=timesteps[::24])

    # Get date of each cluster
    clusters = sorted(ts_clusters.unique())
    dates = [data._dt[ts_clusters[ts_clusters == cluster].index].iat[0]
             for cluster in clusters]
    dates = pd.Series(dates, index=clusters)

    # Return a 'timestep to chosen day' map
    clusters = ts_clusters.map(lambda x: dates[x])

    # Modify the timesteps and get timestep weights
    weights = time_tools._apply_day_summarizer(data, clusters)
    return weights
