# ------------------------------------
# python modules
# ------------------------------------

import os
import sys
import pandas
import numpy
import copy
from bisect import bisect_right,bisect_left
import motility
import pickle
from bisect import bisect_right,bisect_left
from ngslib import Bed,IO,BedList,DB,Utils,GeneBed
from ncshunter import Junction,Junctions,gversion,NonCanonicalSplicing,SplicedGene
# ------------------------------------
# constants
# ------------------------------------

# ------------------------------------
# Misc functions
# ------------------------------------

# ------------------------------------
# Classes
# ------------------------------------

# ------------------------------------
# Main
# ------------------------------------

if __name__=="__main__":
    if len(sys.argv)==1:
        sys.exit("Example:"+sys.argv[0]+" folder[,folder, ...] [hg19|mm10]\n\tRead Mapsplice output folder, and select non-canonical sites.")
    
    # Parse parameters
    genome,ganno,knownjuncfile,gtffile = gversion(sys.argv[2] if len(sys.argv) >2 else 'hg19')
    folders = sys.argv[1].rstrip(',').split(',')
    juncfiles = [folder+"/junctions.txt" for folder in folders]  # junctions.txt list
    bamfiles  = [folder+"/alignments.bam" for folder in folders] # bamfile list
    prefix    = [folder.rstrip("_output") for folder in folders] # prefix list

    # Read IDs
    if os.path.isfile(gtffile+".dump"):
        IDs = pickle.load(open(gtffile+".dump",'rb'))
    else:
        IDs = NonCanonicalSplicing.IDConverter(gtffile)
        pickle.dump(IDs,open(gtffile+".dump",'w'))
    # parse junctions.txt
    for folder in folders:
        juncf = folder+"/junctions.txt"
        bamf  = folder+"/alignments.bam"
        pref  = folder.rstrip("_output")
        stats  = folder+"/stats.txt"
        print pref+":"
        juncs = Junctions()
        juncs.readfile(juncf)
        commons = juncs
        print "\tJunctions:",len(juncs)

        # Remove know junctions
        commons2 = list(NonCanonicalSplicing.removeKnownJunctions(commons,knownjuncfile))
        print "\tAfter removing known ones:",len(commons2)
        # print common list
        ofh = open(pref+"_common.txt",'w')
        for junc in commons:
            print >>ofh, junc.allFields()
        ofh.close()
        # do annotation
        sgenes = NonCanonicalSplicing.annoJunctions(ganno,commons2) 
        # Get Junction related genes
        juncids = {}
        junctypes = {}
        for sgene in sgenes.values():
            for junc,junctype in zip(sgene.junctions,sgene.junctypes):
                juncids.setdefault(junc.id,[junc])
                juncids[junc.id].append(sgene.id)
                junctypes.setdefault(junc.id,[])
                junctypes[junc.id].append(junctype)
        print "\tJunctions affecting genes",len(juncids)
        print "\tAffected Transcripts:",len(sgenes)
    
        bamdb = DB(bamf,'bam')
        ofh = open(pref+"_junc.txt",'w')
        for key in juncids:
            junc = juncids[key][0]
            junc.otherfields.insert(0,junc.checkBam(bamdb))
            print >>ofh, junc.allFields()
        bamdb.close()
        ofh.close()
    
    # header = "chrom\tdonerEnd\tacceptorStart\tname\tcoverage\tstrand\tblockEnd\tblockStart\titemRgb\tblockCount\tblockSizes\tblockStarts\tentropy\tflank_string_case\tflank_string\tintron_score\tanchor_score\tmin_mismatch\tmax_mismatch\taverage_mismatch\tunique_read_count\tmultiple_read_count\tpaired_reads_count\tleft_paired_reads_count\tright_paired_reads_count\tmultiple_paired_reads_count\tunique_paired_reads_count\tsingle_reads_count\tminimal_anchor_difference\tbam_support\taffected_genes"
        header2 = "#chrom\tdonerEnd\tacceptorStart\tname\tcoverage\tstrand\tjunc_site\tBam_support\tGeneID\tTransID\tEns_gene_ID\tEns_trans_ID"
        ofh = open(pref+".txt",'w')
        print >>ofh, header2
        allgids = set([])
        for key,ids in juncids.iteritems():
            junc = ids[0]
            transids = [IDs[tid]['transcript_name'] for tid in ids[1:]]
            emblgids = set([IDs[tid]['gene_id'] for tid in ids[1:]])
            geneids = set([tid.split('-')[0] for tid in transids])
            allgids.update(geneids)
            print >>ofh, "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}".format(junc,junc.site,junc.otherfields[0],';'.join(geneids),';'.join(transids),';'.join(emblgids), ";".join(ids[1:]),';'.join(junctypes[key]))
        ofh.close()
        print "\tAffected Genes:",len(allgids)
