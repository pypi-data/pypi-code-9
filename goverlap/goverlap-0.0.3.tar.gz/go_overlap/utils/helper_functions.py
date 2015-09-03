
import signal

def init_worker():
    """Helper method that allows cntrl-cing despite multiprocessing."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)
