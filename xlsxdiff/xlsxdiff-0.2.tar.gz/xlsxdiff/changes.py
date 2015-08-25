''' Instead of finding what is different, try to find what is similar
in two workbooks. Only works if the books have a similar structure

Steps:
    1. inspect files structure, and only process similar worksheets (same headers)
    2. store each line in the database using the user-provided unique key
    3. for each virtual line with more than one actual line, extract the diffs
    4. return a list of changes, grouped by key

'''
import openpyxl
import logging
import os

logger = logging.getLogger(__name__)


def _empty(value):
    '''empty lines are the same thing as None,
    comparison wise, so just merge them'''
    if value in ('', None):
        return None
    return value


def as_array(row):
    return tuple(map(_empty, [x.value for x in row]))


class Storage(object):
    def __init__(self, ref_source, keys, headers):
        self.ref_source = ref_source
        self.storage = {}
        self.keys = keys
        self.headers = headers
        self.indexes = self._key_indexes(headers[0])
        self.hits = {}

    def _key_indexes(self, header):
        indexes = []
        for key in self.keys:
            indexes.append(header.index(key))
        return indexes

    def _build_keys(self, values):
        return tuple([values[i] for i in self.indexes])

    def store(self, source, line):
        key = self._build_keys(line)
        if not key in self.hits:
            self.hits[key] = 0
        self.hits[key] += 1
        lines = self.storage.setdefault(key, [])
        if not line in [l[1] for l in lines]:
            lines.append((source, line))
            logger.debug('adding line %s with key %s from %s' % (line,
                                                                 key,
                                                                 source))

    def changed(self):
        return dict([(k, v) for k, v in
                     self.storage.iteritems() if len(v) > 1])

    def added(self):
        return dict([(key, lines) for key, lines in self.storage.iteritems()
                     if lines[0][0] != self.ref_source])

    def removed(self):
        return dict([(k, v) for k, v in
                     self.storage.iteritems() if self.hits[k] <= 1])

    def alternatives(self, line):
        key = self._build_keys(line)
        candidates = self.changed().get(key, [])
        return candidates[1:]

    def __len__(self):
        added_keys = set(self.added().keys())
        changed_keys = set(self.changed().keys())
        removed_keys = set(self.removed().keys())
        return len(added_keys | changed_keys | removed_keys)

    def __repr__(self):
        return '<%s object with %d changes>' % (self.__class__.__name__,
                                                len(self))


class WorkbookMerger(object):
    def __init__(self, ref, others, keys, nb_headers=None):
        self.ref = ref
        self.others = others
        self._keys = keys

        if nb_headers is None:
            nb_headers = {'*': 1}
        self._nb_headers = nb_headers

    def _open(self, filename):
        return openpyxl.load_workbook(filename,
                                      use_iterators=True,
                                      data_only=True)

    def keys(self, sheet_name):
        keys = self._keys.get(sheet_name)
        if keys is None:
            keys = self._keys.get('*')
            if keys is None:
                return ()
        return keys

    def header_rows(self, sheet_name):
        maxrow = self._nb_headers.get(sheet_name)
        if maxrow is None:
            maxrow = self._nb_headers.get('*')
            if maxrow is None:
                return xrange(1)
        return xrange(maxrow)

    def mergeable_sheets(self, other):
        wb_ref = self._open(self.ref)
        wb_other = self._open(other)
        common_sheets = (set(wb_ref.get_sheet_names())
                         & set(wb_other.get_sheet_names()))
        result = []

        for sheet_name in common_sheets:
            ref_header = as_array(wb_ref[sheet_name].rows.next())
            other_header = as_array(wb_other[sheet_name].rows.next())
            if ref_header != other_header:
                diff_ref_headers = set(ref_header) - set(other_header)
                diff_other_headers = set(other_header) - set(ref_header)
                common_header_len = len(set(other_header) & set(ref_header))
                ref_filename = os.path.basename(self.ref)
                other_filename = os.path.basename(other)
                msg = ('Column names are different in sheet %s.\n'
                       '%s common headers.\n'
                       'Additional headers in %s: %s\n'
                       'Additional headers in %s: %s')
                logger.warning(msg % (sheet_name, common_header_len,
                                      ref_filename, list(diff_ref_headers),
                                      other_filename, list(diff_other_headers)))
                continue
            sheet_keys = set(self.keys(sheet_name))
            if not sheet_keys:
                logger.warning('no keys defined for sheet %s '
                               'and no wildcard either' % sheet_name)
                continue
            missing_keys = sheet_keys - set(ref_header)
            if missing_keys:
                msg = 'looking for keys %s, but could not find them in %s'
                logger.warning(msg % (missing_keys, sheet_name))
                continue
            result.append(sheet_name)
        return result

    def extra_sheets(self, other):
        wb_ref = self._open(self.ref)
        wb_other = self._open(other)
        common = set(wb_other.get_sheet_names()) - set(wb_ref.get_sheet_names())
        return list(common)

    def gather(self, filter=lambda x: x):
        similar_lines = {}
        wb_ref = self._open(self.ref)

        for other in self.others:
            common_sheets = self.mergeable_sheets(other)
            other_sheets = common_sheets + self.extra_sheets(other)

            workbooks = ((self.ref, wb_ref, common_sheets),
                         (other, self._open(other), other_sheets))

            for source, wb, sheets in workbooks:
                for sheet_name in sheets:
                    rows = wb[sheet_name].rows
                    headers = [as_array(rows.next())
                               for _idx in self.header_rows(sheet_name)]
                    keys = self.keys(sheet_name)
                    storage = similar_lines.setdefault(sheet_name,
                                                       Storage(self.ref,
                                                               keys,
                                                               headers))
                    for row in rows:
                        row = as_array(row)
                        if any(row):  # protect from emtpy lines
                            if filter(row):  # allow user-defined filter
                                storage.store(source, row)

        return dict([(k, v) for k, v in similar_lines.iteritems() if v])
