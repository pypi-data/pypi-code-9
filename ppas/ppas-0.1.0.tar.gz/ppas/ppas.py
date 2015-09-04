"""Postprocess Answer Sets.

This program accepts clingo 4.x and clasp 3.x log files and an ASP script for
postprocessing. The result is a rewritten log file.

Each answer is assigned a sequence number starting from 1 and it's atoms are
wrapped in the special predicate _as(Atom, SequenceNum). The answer sets are
replaced with atoms read from a special predicate _pp(Atom, SequenceNum).

Note that the sequence number does not necessarily correspond to <num> in the
"Answer: <num>" line in the input log file; for example when multiple solve
calls were used.

Usage:
  ppas <script> <infile> <outfile> [--clingo-bin=<path>, --quiet]
  ppas -h | --help
  ppas --version

Options:
  --clingo-bin=<path>       Path to clingo binary.
  --quiet                   Disable stdout messages.
  -h --help                 Show this screen.
  --version                 Show version.
"""

from __future__ import print_function

import subprocess
import json
import re

from docopt import docopt

# Regexp for detecting the answer number line in the input log.
answerNumberLineRe = re.compile(
    r'^Answer: \d+$'
)
# Regexp for reading atoms out of the clingo result.
postprocessAtomRe = re.compile(
    r'^_pp\((?P<atom>.+),(?P<sequenceNum>\d+)\)$'
)

def main():
    # Parse arguments.
    args = docopt(__doc__, version='0.1.0')

    # We have to keep all the answer sets in memory, and these should represent the
    # largest portion of the logfile in bytes, so might as well keep the full file
    # in memory.
    lines = []
    answerSetLineNums = []

    if not args['--quiet']: print('Reading input file', args['<infile>'], '...')
    # Read the file and flag answer set line numbers
    lineNum = 0
    with open(args['<infile>'], 'r') as f:
        for line in f:
            lines.append(line)
            lineNum += 1
            if answerNumberLineRe.match(line) is not None:
                answerSetLineNums.append(lineNum) # lineNum points to next line now

    # Wrap atoms to predicate _as(Atom, AsCurrent)
    wrappedAtoms = []
    asCount = len(answerSetLineNums)
    for asCurrent in range(0, asCount):
        curLine = lines[answerSetLineNums[asCurrent]].strip()
        wrappedAtoms.extend([ '_as(' + atom + ',' + str(asCurrent+1) + ')' for atom in curLine.split()])

    wrappedAtomsStr = '. '.join(wrappedAtoms)
    if len(wrappedAtoms) > 0:
        wrappedAtomsStr += '.' # add final dot
    executable = args['--clingo-bin'] if args['--clingo-bin'] is not None else 'clingo'

    if not args['--quiet']: print('Calling', executable, 'with script', args['<script>'], '...')

    # Execute clingo, make it read script and also read from stdin
    cl = subprocess.Popen([executable, '--outf=2', '-c asCount='+str(asCount), '-', args['<script>']], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    cl.stdin.write(wrappedAtomsStr.encode('utf-8'))
    cl.stdin.close()

    if not args['--quiet']: print('Reading from clingo...')
    clingoOutput = str(cl.stdout.read())
    # Read clingo messages and pass them on
    jsonStart = clingoOutput.find("\n{") # Trust that first { will be start of JSON.
    if jsonStart == -1:
        jsonStart = clingoOutput.find('{')
    jsonPart = clingoOutput[jsonStart:]
    messages = clingoOutput[:jsonStart]

    if len(messages) > 1:
        print("\nMessages from postprocessing", args['<infile>'], 'with', args['<script>'] + ':')
        print('----------')
        print(messages)

    outJson = json.loads(jsonPart)
    outAtoms = outJson['Call'][0]['Witnesses'][0]['Value']

    relevantAtoms = []
    for i in range(0, asCount):
        relevantAtoms.append([])

    for atom in outAtoms:
        m = postprocessAtomRe.match(atom)
        if m is not None and int(m.group('sequenceNum')) <= asCount:
            relevantAtoms[int(m.group('sequenceNum'))-1].append(m.group('atom'))

    # Output rewritten log
    if not args['--quiet']: print("Outputting rewritten log...")
    lineNum = 0
    with open(args['<outfile>'], 'w') as f:
        for line in lines:
            if lineNum in answerSetLineNums:
                f.write(' '.join(relevantAtoms[answerSetLineNums.index(lineNum)]).encode('utf-8'))
                f.write("\n")
            else:
                f.write(line.encode('utf-8'))
            lineNum += 1

    if not args['--quiet']: print('Written to', args['<outfile>'])
    if not args['--quiet']: print('Done')


if __name__ == "__main__":
    main()
