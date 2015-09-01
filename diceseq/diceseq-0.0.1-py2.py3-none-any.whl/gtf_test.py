from gtf_utils import *

# anno1 = load_annotation("/homes2/yuanhua/research/splicing/data/Annotation/Saccharomyces_cerevisiae.R64-1-1.77.gtf")
# print len(anno1["genes"])
# print anno1["gene_id"]

# anno1 = load_annotation("/homes2/yuanhua/research/splicing/data/Annotation/Saccharomyces_cerevisiae.R64-1-1.75_1.3.gtf", source="sander")
# print len(anno1["genes"])
# print anno1["gene_id"]
# print sum((anno1["exon_num"] == 2) * (anno1["biotype"] == "protein_coding"))

# anno1 = load_annotation("/homes2/yuanhua/research/splicing/data/Annotation/human/hg19/SE.hg19.gff3", source="miso")
# print len(anno1["genes"])
# print anno1["gene_id"]
# print anno1["tran_num"]

anno1 = load_annotation("/homes2/yuanhua/research/splicing/data/SGD/saccharomyces_cerevisiae_R64-2-1_20150113.gff", source="sgd")
print len(anno1["genes"])
print anno1["gene_id"]
print anno1["tran_num"]
print sum((anno1["exon_num"] == 2))

