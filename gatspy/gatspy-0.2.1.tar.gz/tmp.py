from gatspy.periodic.lomb_scargle_fast import lomb_scargle_fast
import numpy as np 


rng = np.random.RandomState(0)

t = 30 * rng.rand(100)
y = np.sin(t)
dy = 0.1 + 0.1 * rng.rand(len(t))
y += dy * rng.randn(len(t))

for center_data in [True, False]:
    for fit_offset in [True, False]:
        for use_fft in [True, False]:
            freq, P = lomb_scargle_fast(t, y, dy,
                                          center_data=center_data,
                                          fit_offset=fit_offset,
                                          use_fft=use_fft)

            print(center_data, fit_offset, use_fft, freq[0], P[0])
