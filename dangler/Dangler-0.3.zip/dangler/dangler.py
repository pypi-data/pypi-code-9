r"""
Dangler v0.3
"""
import argparse
from .blocks import make_block 
from .blockprocessors.html import Html
from .blockprocessors.jinja2 import Jinja2

BLOCK_PROCESSORS = [Html(), Jinja2()]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    block = make_block(open(args.filename, 'r'))
    for processor in BLOCK_PROCESSORS:
        block = processor.process(block)
    print(str(block))
