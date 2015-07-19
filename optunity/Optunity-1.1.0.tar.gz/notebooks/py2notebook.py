import sys

assert(len(sys.argv) > 2)

pyname = sys.argv[1]
nbname = sys.argv[2]

print("Converting %s to %s." % (pyname, nbname))

# http://stackoverflow.com/a/23292713
import IPython.nbformat.current as nbf

nb = nbf.read(open(pyname, 'r'), 'py')
nbf.write(nb, open(nbname, 'w'), 'ipynb')
