from __future__ import absolute_import 

from .love import main

import sys

argv = sys.argv
if len(argv)>=2:
    main(argv[1])
else:
    main()


