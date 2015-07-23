# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from argparse import FileType
from argparse import ArgumentDefaultsHelpFormatter
import csv
from cStringIO import StringIO
import logging
logger = logging.getLogger(__name__)


class StreamCharsetWrapper(object):

    def __init__(self, stream, charset):
        self.stream = stream
        self.charset = charset

    __iter__ = lambda self: self

    def next(self):
        raw = self.stream.next()
        if self.charset == 'utf-8':
            return raw
        return raw.decode(self.charset).encode('utf-8')


def prepare_session(session, arguments):
    session.open(db=arguments.database)
    session.ir_model_data = session.registry('ir.model.data')

    def ref(xid):
        """Monkey patch for consistency with unit tests.

        should be put in recipe, of course."""
        module, xml_id = xid.split('.')
        return session.ir_model_data.get_object_reference(session.cr, 1, module, xml_id)[1]

    session.ref = ref
    return session


class CSVImporter(object):

    def init_session(self, session, model):
        self.session = session
        self.uid = getattr(session, 'uid', 1)
        self.cr = session.cr
        self.model = model
        self.base_import = session.registry('base_import.import')

    def init_csv_reader(self, fobj, charset='utf-8', delimiter=',', quotechar='"'):
        stream = StreamCharsetWrapper(fobj, charset)
        self.csv_reader = csv.reader(stream, delimiter=delimiter, quotechar=quotechar)
        self.header = self.csv_reader.next()

    def get_files(self, nb_rows_by_import):
        rowscut = []
        fr = tr = 0
        rowscut.append((fr, fr + nb_rows_by_import, []))
        for r in self.csv_reader:
            tr += 1
            if tr >= fr + nb_rows_by_import:
                fr = tr
                rowscut.append((fr, fr + nb_rows_by_import, []))

            rowscut[-1][2].append(r)

        nblines = tr
        rows = []
        for fr, tr, rs in rowscut:
            fp = StringIO()
            csvwriter = csv.writer(fp, delimiter=',', quotechar='"')
            csvwriter.writerow(self.header)
            csvwriter.writerows(rs)
            fp.seek(0)
            res = fp.read()
            fp.close()
            rows.append((fr, tr, res))

        logger.info("loaded %r lines in %r times" % (nblines, len(rows)))
        return rows

    def make_import(self, file2import):
        bi_id = self.base_import.create(self.cr, self.uid, {
            'res_model': self.model,
            'file': file2import,
        })
        options = {
            'encoding': 'utf-8',
            'quoting': '"',
            'separator': ',',
            'headers': True,
        }
        res = self.base_import.do(self.cr, self.uid, bi_id, self.header, options)
        for r in res:
            logger.error('line %(record)d: %(message)s' % r)
        if res:
            raise Exception("Impossible d'importer le fichier")

    def make_consolidation(self, autocommit):
        c = self.session.registry('bdes.consolidation.by.ce')
        c.make_consolidation(self.cr, self.uid, autocommit=autocommit)


def run(session):
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('file', nargs='*', type=FileType('r'))
    parser.add_argument('--no-commit', action='store_true')
    parser.add_argument('--charset', default='utf-8', choices=('cp1252',
                                                               'utf-8'),
                        help="Input CSV charset encoding")
    parser.add_argument('--delimiter', default=',', help="Column delimiter")
    parser.add_argument('--quotechar', default='"', help="Column quote char")
    parser.add_argument('--nb-rows-by-import', default='100',
                        help="Number of rows between two commit")
    parser.add_argument('-d', '--database')
    parser.add_argument('-m', '--model')

    arguments = parser.parse_args()
    importer = CSVImporter()
    session = prepare_session(session, arguments)

    importer.init_session(session, arguments.model)
    for fobj in arguments.file:
        importer.init_csv_reader(fobj, charset=arguments.charset,
                                 delimiter=arguments.delimiter,
                                 quotechar=arguments.quotechar)
        files = importer.get_files(int(arguments.nb_rows_by_import))
        fobj.close()
        for fline, tline, f in files:
            logger.info('Import %r line %r:%r' % (fobj, fline, tline))
            importer.make_import(f)
            if not arguments.no_commit:
                session.cr.commit()
            else:
                session.cr.rollback()

    session.cr.close()
