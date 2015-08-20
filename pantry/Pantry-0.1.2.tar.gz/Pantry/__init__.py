from contextlib import contextmanager
import pickle

@contextmanager
def pantry(filename):
    # check if file exists
    try:
        with open(filename) as f:
            db = pickle.load(f)
    except IOError:
        with open(filename, 'w') as f:
            db = {}
            pickle.dump(db, f)

    yield db
    
    with open(filename,'w') as f:
        pickle.dump(db, f)

