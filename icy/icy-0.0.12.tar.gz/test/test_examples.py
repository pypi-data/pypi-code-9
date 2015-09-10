import icy
import contextlib
import os
from datetime import datetime

if __name__ == '__main__':
    print('running examples tests ...')
    t0 = datetime.now()
    results = [0, 0, 0]
    for ex in sorted(icy.examples):
        t1 = datetime.now()
        src, read, merge = icy.examples[ex]
        try:
            data = icy.read(src, cfg=read, silent=True)
            n_keys = len(data.keys())
            if n_keys > 0:
                print('data {:<15} [SUCCESS]   {:.1f}s, {} dfs, {}'.format(
                    ex, (datetime.now()-t1).total_seconds(), n_keys, icy.mem(data)))
                results[0] += 1
            else:
                print('data {:<15} [NO IMPORT] {:.1f}s'.format(ex, (datetime.now()-t1).total_seconds()))
                results[1] += 1
        except:
            print('data {:<15} [EXCEPTION] {:.1f}s'.format(ex, (datetime.now()-t1).total_seconds()))
            results[2] += 1
    print()
    print('ran {} tests in {:.1f} seconds'.format(len(icy.examples),
        (datetime.now()-t0).total_seconds()))
    print('{} success / {} no import / {} exception'.format(
        str(results[0]), str(results[1]), str(results[2])))
        