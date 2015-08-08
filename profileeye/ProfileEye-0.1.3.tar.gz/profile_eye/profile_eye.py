"""
Library backend of profile_eye. While you can use this directly, unless you're sure of what 
    you're doing, you should probably use the utility version.
"""


import os
import sys
import re
import json
import subprocess
import argparse
import six

import jinja2


__version__ = '0.1.3'


def _to_str(s):
    if six.PY2:
        return s
    if isinstance(s, bytes):
        return s.decode()
    return s


def gprof2dot_to_dot_plain(gprof2dot_output):
    """
    Pipes gprof2dot output through dot with plain output specified.

    Args:
        gprof2dot_output: Bytes consisting of gprof2dot output.

    Returns:
        Output of ``dot -Tplain`` operating on gprof2dot_output.
    """

    process = subprocess.Popen(
        ('dot', '-Tplain') if six.PY2 else ('dot', '-Tplain', '-Gcharset=latin1'), 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE)

    out, err = process.communicate(input=gprof2dot_output)
    # Tmp Ami check err
    return out


def append_slash_ends(lines):
    cur_line = ''
    for line in lines:
        if line.rstrip() and line.rstrip()[-1] == '\\':
            cur_line += line.rstrip()[:-1]
        else:
            cur_line += line.lstrip()
            yield cur_line
            cur_line = ''


class DotPlainParser(object):
    """
    A parser for dot's output.
    """

    _node_re = re.compile(r'node ([^ ]+) ([^ ]+) ([^ ]+) [^ ]+ [^ ]+ "(.+?)\\n(.+?)%\\n\((.*?)%\)(\\n(\d+))?')
    _cprofile_re = re.compile(r'([^:]*):(\d+):([^:]+)')
    _edge_label_re = re.compile(r'"((.+?)%\\n)?(\d+)')

    def __init__(self, file_colon_line_colon_label_format=False):
        """
        Ctor.

        Args:
            file_colon_line_colon_label_format: An indication whether the labels are of the form
                <file>:<line>:<label>.
        """

        self._nodes, self._edges = {}, []
        self._file_colon_line_colon_label_format = file_colon_line_colon_label_format

    def add(self, l):   
        """
        Feeds a line into the parser.

        Args:
            l: Line fed.
        """

        if type(l) != six.text_type:
            l = l.decode('utf-8')

        words = l.split(' ')        
        if words[0] == 'graph':
            pass
        elif words[0] == 'node':
            self._parse_node_line(l)
        elif words[0] == 'edge':
            self._parse_edge_words(words)
        elif not words:
            pass
        elif len(words) == 1 and (words[0] == 'stop' or not words[0]):
            pass
        else:
            raise RuntimeError('Cannot parse line' + l)

    def _parse_node_line(self, l):
        match = DotPlainParser._node_re.search(l)
        if match is None:
            raise RuntimeError('Failed to regex ' + l)
        groups = match.groups()
        name, x, y, label, total, internal = \
            int(groups[0]), float(groups[1]), float(groups[2]), groups[3], float(groups[4]), float(groups[5])

        try:
            times_called = int(groups[7])
        except:
            times_called = 1

        file, line = '', -1
        match = DotPlainParser._cprofile_re.search(label) if self._file_colon_line_colon_label_format else None
        if match: 
            groups = match.groups()
            file, line, label = groups[0], int(groups[1]), groups[2]

        self._nodes[name] = {
            'name':  _to_str(name),
            'label': _to_str(label),
            'total': _to_str(total),
            'file': _to_str(file),
            'line': _to_str(line),
            'internal': _to_str(internal),
            'x': _to_str(x),
            'y': _to_str(y),
            'times_called': _to_str(times_called),
            'dummy': False,
        }

    def _parse_edge_words(self, words):
        target, source = int(words[1]), int(words[2])   
        num = int(words[3])
        points = reversed([(float(words[4 + 2 * i]), float(words[5 + 2 * i])) for i in range(num)])
        label = words[4 + 2 * num]
        match = DotPlainParser._edge_label_re.search(label)
        groups = match.groups()
        self._edges.append({
            'source': _to_str(source), 
            'target': _to_str(target),
            'points': list(points),
            'times_called': _to_str(groups[2])})

    def prepare_all(self):
        """
        Prepares a dictionary of all parsed and processed data.

        Returns:
            A dictionary mapping 'nodes' to the nodes, and 'edges' to the edges.
        """
        nodes = []
        for i in range(max(self._nodes.keys()) + 1):
            if i in self._nodes:    
                nodes.append(self._nodes[i])
            else:
                nodes.append({
                    'name':  _to_str(i),
                    'dummy': True,
                    })

        by_total = \
            sorted(nodes, key=lambda node: 0 if node['dummy'] else node['total'], reverse=True)  
        internal_start, total_start = 0, 0
        for i, node in enumerate(by_total):
            node['byTotalInd'] = i
            if not node['dummy']:
                node['totalStartByTotalInd'] = total_start
                total_start += node['total']
                node['internalStartByTotalInd'] = internal_start
                internal_start += node['internal']
        by_internal = sorted(nodes, key=lambda node: 0 if node['dummy'] else node['internal'], reverse=True)  
        internal_start, total_start = 0, 0
        for i, node in enumerate(by_internal):
            node['byInternalInd'] = i
            if not node['dummy']:
                node['totalStartByInternalInd'] = total_start
                total_start += node['total']
                node['internalStartByInternalInd'] = internal_start
                internal_start += node['internal']

        total_outgoing_time = sum([node['total'] for node in nodes if not node['dummy']])
        node_total_ougoing_time = [0] * len(nodes)
        node_total_incoming_time = [0] * len(nodes)
        for e in self._edges:
            e['back'] = nodes[e['source']]['y'] >= nodes[e['target']]['y']
            if e['back']:
                total_outgoing_time += nodes[e['target']]['total']
            node_total_ougoing_time[e['target']] += nodes[e['target']]['total']

        for e in self._edges:
            e['outgoingFrac'] = nodes[e['target']]['total'] / float(total_outgoing_time)

        return {
                'nodes': nodes,
                'edges': self._edges,
            }


def render_parsed(d):
    """
    Renders HTML for parsed gprof2dot + dot output.

    Args:
        d: the results of a DotPlainParser's prepare_all() 

    Returns:
        A bytes object of HTML.
    """

    this_dir = os.path.split(__file__)[0]

    template_loader = jinja2.FileSystemLoader(searchpath=this_dir)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template('_tmpl/index.html.jinja2')

    return six.b(template.render({
        'data': json.dumps(json.dumps(d)),
        'd3': open(os.path.join(this_dir, '_js', 'd3.v3.min.js')).read(),
        'fisheye': open(os.path.join(this_dir, '_js', 'fisheye.js')).read(),
        'profileEye': open(os.path.join(this_dir, '_js', 'profile_eye.js')).read(),
        }))


def main(): 
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--file-colon-line-colon-label-format', 
        dest='file_colon_line_colon_label_format', 
        action='store_true', 
        default=False)
    args = parser.parse_args()

    input = ''.join(list(sys.stdin))
    out = gprof2dot_to_dot_plain(input)

    p = DotPlainParser(args.file_colon_line_colon_label_format)
    for l in append_slash_ends(out.split('\n')):
        p.add(l)

    six.print_(render_parsed(p.prepare_all()))


if __name__ == '__main__':
    main()
