import logging

from .reader import Reader
from .writer import Writer

logger = logging.getLogger("mysqltsv.functions")

def read(f, *args, **kwargs):
    return Reader(f, *args, **kwargs)

def write(rows, f, *args, **kwargs):
    writer = Writer(f, *args, **kwargs)

    for row in rows:
        writer.write(row)
