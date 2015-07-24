# coding: utf-8
from __future__ import unicode_literals
import pandas as pd
import codecs
import cStringIO


def main_(xls_, csv_, out, enc1, enc2):
    xls = pd.read_excel(xls_, 0)
    xls.columns = [
        'id',
        'request date',
        'issue date',
        'count',
        'request sum',
        'issue sum'
    ]

    data = None
    with open(csv_, 'r') as f:
        data = f.read()
    decoded = codecs.decode(data, enc1, 'ignore')
    encoded = codecs.encode(decoded, enc2, 'ignore')
    f = cStringIO.StringIO(encoded)
    csv = pd.read_csv(f, header=None, encoding=enc2)

    csv.columns = [0, 'd1', 'd2', 'id', 4]

    df = pd.merge(xls, csv, on='id')

    extra_cols = ['source', 'campaign', 'term', 'content', 'medium']
    for ec in extra_cols:
        df[ec] = ''

    def add_to_row(k1, k2, k, v, i, col):
        if ((k1 in k) or (k2 in k)) and len(v) > 0 and v not in df[col].ix[i]:
            val = ', '.join([df[col].ix[i], v])
            df[col].ix[i] = val if len(df[col].ix[i]) > 0 else v

    for i in xrange(len(df)):
        if hasattr(df.d1.ix[i], 'split'):
            tokens1 = df.d1.ix[i].split('|')
        else:
            tokens1 = []
        if hasattr(df.d2.ix[i], 'split'):
            tokens2 = df.d2.ix[i].split('&')
        else:
            tokens2 = []
        tokens = tokens1 + tokens2
        for token in tokens:
            pos = token.find('=')
            v = token[pos+1:]
            k = token[:pos]
            add_to_row('utmcsr', 'utm_source', k, v, i, 'source')
            add_to_row('utmccn', 'utm_campaign', k, v, i, 'campaign')
            add_to_row('utmctr', 'utm_term', k, v, i, 'term')
            add_to_row('utmcct', 'utm_content', k, v, i, 'content')
            add_to_row('utmcmd', 'utm_medium', k, v, i, 'medium')
        token = None
        token1 = None
        token2 = None

    import csv
    df.to_csv(out, encoding=enc2,
              columns=list(xls.columns) + extra_cols, index=False,
              quoting=csv.QUOTE_NONNUMERIC)


def main():
    import argparse
    parser = argparse.ArgumentParser('Concatincate two files by id\n')
    parser.add_argument('xls', type=str, help='XLS file')
    parser.add_argument('--csv', type=str, help='CSV file',
                        default='seotime_stats.csv')
    parser.add_argument('--enc1', type=str, help='CSV saved encoding',
                        default='utf8')
    parser.add_argument('--enc2', type=str, help='CSV real encoding',
                        default='cp1252')
    parser.add_argument('--output', '-o', type=str, help='output file',
                        default='out.csv')
    args = parser.parse_args()
    main_(args.xls, args.csv, args.output, args.enc1, args.enc2)


if __name__ == '__main__':
    main()
