import gffutils

def seq_test():
    db = gffutils.create_db(gffutils.example_filename('sequence-test.gff'), ':memory:')
    fasta = gffutils.example_filename('seq.fasta')
    f = db['five_prime_UTR_FBgn0031208:1_737']
    assert f.sequence(fasta) == 'AAATAGT'

def canonical_():
    db = gffutils.create_db(gffutils.example_filename('sequence-test.gff'), ':memory:')
    print(list(gffutils.helpers.canonical_transcripts(db, fasta_filename=gffutils.example_filename('seq.fasta'))))
    assert False

