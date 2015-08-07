import os
import mmap
import bgdata

HG19 = bgdata.get_path('datasets', 'genomereference', 'hg19')
HG19_MM = {}


def get_mmap(chromosome):
    if chromosome not in HG19_MM:
        fd = open(os.path.join(HG19, "chr{0}.txt".format(chromosome)), 'rb')
        HG19_MM[chromosome] = mmap.mmap(fd.fileno(), 0, access=mmap.ACCESS_READ)
    
    return HG19_MM[chromosome]


def get_ref(chromosome, start, size=1):
    mm_fd = get_mmap(chromosome)
    mm_fd.seek(start)
    return mm_fd.read(size).decode().upper()


def get_ref_triplet(chromosome, start):
    return get_ref(chromosome, start-1, size=3)


