# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from routefs import main as routefs_main
from mongofs.mongofs import MongoFS
import sys

def main(): 
    sys.argv[1] = "-ohost="+sys.argv[1]
    routefs_main(MongoFS)


if __name__ == "__main__":
    main()