#!/usr/bin/env python
import csv
import sys
import pandas as pd

outfmt6 = ['qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen',
           'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore']



hmmscan_cols = ['target_name', 'target_accession', 'tlen', 'query_name', 
        'query_accession', 'query_len', 'full_evalue', 'full_score', 
        'full_bias', 'domain_num', 'domain_total', 'domain_c_value', 
        'domain_i_evalue', 'domain_score', 'domain_bias', 'hmm_coord_from', 
        'hmm_coord_to', 'ali_coord_from', 'ali_coord_to', 'env_coord_from', 
        'env_coord_to', 'accuracy', 'description']

gff3_transdecoder_cols = ['seqid', 'feature_type', 'start', 'end', 'strand']

def blast_to_df(fn, names=outfmt6, delimiter='\t', index_col=0):
    return pd.read_table(fn, header=None, index_col=index_col, names=names,
                             delimiter=delimiter, skipinitialspace=True,
                             dtype={'qstart': int, 'qend': int, 'sstart': int, 'send': int})



def parse_busco(fn):
    res = {}
    with open(fn) as fp:
        for ln in fp:
            if ln.strip().startswith('C:'):
                tokens = ln.split(',')
                for token in tokens:
                    key, _, val = token.partition(':')
                    key = key.strip()
                    val = val.strip().strip('%')
                    if key == 'C':
                        valc, _, vald = val.partition('%')
                        valc = valc.strip()
                        vald = vald.strip('D:][%')
                        res['C(%)'] = valc
                        res['D(%)'] = vald
                    else:
                        if key != 'n':
                           key += '(%)'
                        res[key] = val.strip().strip('%')
    return res


def busco_to_df(fn_list, dbs=['metazoa', 'vertebrata']):

    data = []
    for fn in fn_list:
        data.append(parse_busco(fn))

    df = pd.DataFrame(data)
    df['fn'] = [os.path.basename(fn)[14:-14].strip('.') for fn in fn_list]
    df['db'] = None
    for db in dbs:
        idx = df.fn.str.contains(db)
        df.loc[idx,'db'] = db
        df.loc[idx,'fn'] = df.loc[idx, 'fn'].apply(lambda fn: fn[:fn.find(db)].strip('. '))
    return df


def gtf_to_df(filename):

    # Converter func for the nonstandard attributes column
    def attr_col_func(col):
        d = {}
        for item in col.strip(';').split(';'):
            pair = item.strip().split(' ')
            d[pair[0]] = pair[1].strip('"')
        return d

    def strand_func(col):
        if col =='+':
            return 1
        else:
            return -1

    names=['contig_id', 'source', 'feature', 'start', 'end',
           'score', 'strand', 'frame', 'attributes']

    # Read everything into a DataFrame
    gtf_df = pd.read_table(filename, delimiter='\t', comment='#',
                           header=False, names=names,
                           converters={'attributes': attr_col_func, 'strand': strand_func})
    
    # Generate a new DataFrame from the attributes dicts, and merge it in
    gtf_df = pd.merge(gtf_df,
                      pd.DataFrame(list(gtf_df.attributes)),
                      left_index=True, right_index=True)
    del gtf_df['attributes']
    
    # Switch from [start, end] to [start, end)
    gtf_df.end = gtf_df.end + 1

    return gtf_df


def hmmscan_to_df(fn):
    def split_query(item):
        q, _, _ = item.partition('|')
        return q
    data = []
    with open(fn) as fp:
        for ln in fp:
            if ln.startswith('#'):
                continue
            tokens = ln.split()
            data.append(tokens[:len(hmmscan_cols)-1] + [' '.join(tokens[len(hmmscan_cols)-1:])])
    df = pd.DataFrame(data, columns=hmmscan_cols)
    df.query_name = df.query_name.apply(split_query)
    df.set_index('query_name', inplace=True)
    return df

def gff3_transdecoder_to_df(fn):
    data = []
    with open(fn) as fp:
        for ln in fp:
            if ln == '\n':
                continue
            tokens = ln.split('\t')
            try:
                data.append([tokens[0]] + tokens[2:5] + [tokens[6]])
            except IndexError as e:
                print e
                print tokens
                break
    df = pd.DataFrame(data, columns=gff3_transdecoder_cols)
    df.set_index('seqid', inplace=True)
    return df

def maf_to_df(fn):
    
    data = []
    with open(fn) as fp:
        while (True):
            try:
                line = fp.next().strip()
            except StopIteration:
                break
            if not line or line.startswith('#'):
                continue
            if line.startswith('a'):
                cur_aln = {}

                # Alignment info
                tokens = line.split()
                for token in tokens[1:]:
                    key, _, val = token.strip().partition('=')
                    cur_aln[key] = val
                
                # First sequence info
                line = fp.next()
                tokens = line.split()
                cur_aln['s_name'] = tokens[1]
                cur_aln['s_start'] = tokens[2]
                cur_aln['s_aln_len'] = tokens[3]
                cur_aln['s_strand'] = tokens[4]
                cur_aln['s_len'] = tokens[5]
                
                # First sequence info
                line = fp.next()
                tokens = line.split()
                cur_aln['q_name'] = tokens[1]
                cur_aln['q_start'] = tokens[2]
                cur_aln['q_aln_len'] = tokens[3]
                cur_aln['q_strand'] = tokens[4]
                cur_aln['q_len'] = tokens[5]

                data.append(cur_aln)
    
    return pd.DataFrame(data)

