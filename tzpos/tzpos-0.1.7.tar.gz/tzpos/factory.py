from searcher import Searcher
from os.path import dirname, abspath, join


continents = frozenset([None,
    'America', 'Asia', 'Oceania',
    'Europe', 'Africa', 'Atlantic',
])

def searcher_in_continent(continent):
    searcher = Searcher()
    #assert continent in continents
    with open_db_file() as f:
        for line in f:
            parsed = line.split()
            t = (float(parsed[0]), float(parsed[1]))
            if parsed[2].startswith(continent):
                searcher.rawdb.append(t)
                searcher.tznames.append(parsed[2])
    return searcher

def make_searcher():
    searcher = Searcher()

    with open_db_file() as f:
        for line in f:
            parsed = line.split()
            t = (float(parsed[0]), float(parsed[1]))
            searcher.rawdb.append(t)
            searcher.tznames.append(parsed[2])
    return searcher

def open_db_file():
    base_dir = dirname(abspath(__file__))
    filename = join(base_dir, "tzposdb.data")
    return open(filename, 'rb')


if __name__ == '__main__':
    import time
    n = 100
    searcher = searcher_in_continent('America/Hermosillo')
    #searcher = make_searcher()
    print("Loaded %d zones" % len(searcher.rawdb))
    t = time.time()
    for i in range(n):
        tz = searcher.timezone_at(29.757512, -111.070278)

    print("time spent: %.4f" % (time.time() - t))
    print(tz)
