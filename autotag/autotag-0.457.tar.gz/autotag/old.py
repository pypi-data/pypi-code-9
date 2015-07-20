'''
Created on Jul 20, 2015

@author: jordan
'''
import math
import itertools
from utils import nCr, Progress, get_pattern
import difflib
import codecs
from collections import Counter
import numpy

def tf(word,words):
    return words.count(word)

def idf(word,statuses,N):
#     N = len(statuses)
    n = statuses.count(word)
    return math.log(float(N)/n)
    
def cluster_words(count):
    words = set(dict(count).keys())
    comb = itertools.combinations(words,2)
    cnum = nCr(len(words),2)
    print(cnum)
    s = difflib.SequenceMatcher()
    dist = {}
    prog = Progress()
    for i,c in enumerate(comb):
        prog.progress(i, cnum)
        s.set_seq1(c[0]) 
        s.set_seq2(c[1])
        dist[c] = s.real_quick_ratio()
        
def get_patterns(count,threshold):
#     וכשתלכנה - ו, כש, ת**נה, הלך
#    להגשים - ל, ה**י*, גשמ
#    find all frequent diffs between words
#     count = dict(count)
    words = set(dict(count).keys())
    print(len(count))
    f = codecs.open('matches', 'w', 'utf-8')
    prog = Progress()
    s = difflib.SequenceMatcher()
    patterns = []
    for w1,c1 in count:
        prog.progress(count.index((w1,c1)), len(count))
#         get close words
        s.set_seq1(w1)
        matches = set()
        for w2 in words:
            s.set_seq2(w2)
            if s.real_quick_ratio() >= threshold and \
               s.quick_ratio() >= threshold and \
               s.ratio() >= threshold:
                matches.add(w2)
                pattern = get_pattern(s.get_opcodes(),w1,w2)
                if pattern:
                    patterns.append(pattern)
#         matches = set(difflib.get_close_matches(w,words,100,0.8))
#         diff is a possible pattern
        words = words - matches
        if(len(matches)>1):
            f.write(w1+' : '+', '.join(matches)+'\n')
            pattern_count = Counter(patterns)
            pattern_count = pattern_count.most_common()
            f2 = codecs.open('patterns', 'w', 'utf-8')
            f2.writelines([unicode(p)+' : '+str(c)+'\n' for p,c in pattern_count])
            f2.close()
#     combos = list(itertools.combinations(count.keys(),2))
#     print(len(combos))
    f.close()
    pass 

def split_pattern(count):
#     ואת -> ו את
    words = set(dict(count).keys())
    print(len(words))    
    for w,c in count:
        if w[0] in u'ולכשמבה' and w[1:] in words:
            words.remove(w)
            count.remove((w,c))
    print(len(words))
    f = codecs.open('split_words', 'w', 'utf-8')
    for w,c in count:
        f.write(unicode(w) +' : '+ str(c)+'\n')
    f.close()    
    return words 
        
# def bag_of_words(data, words):
#     print(len(data))
#     print(len(words))
#     m = scipy.sparse.lil_matrix((len(data),len(words)))
#     prog = Progress()
#     for i,d in enumerate(data):
#         prog.progress(i, len(data))
#         dwords = d.split()
#         sum = 0
#         for w in dwords:
#             if w in words:
#                 sum+=1
#                 j = words.index(w)
#                 m[i,j] = 1
#         m[i,:] = m[i,:]/sum
#     return m

def get_distances(bag):
    bag = bag.tocsr()
    distmat = bag*bag.transpose()
    distmat = distmat.todense()
    numpy.fill_diagonal(distmat, 0)
    with file('distmat.txt', 'w') as outfile:
        numpy.savetxt(outfile, distmat)
    return distmat 

#    max similarity clustered together
def cluster_sentences(distmat):
    clusters = {}
    clustersN = 0
    for i in range(100):
        closest = distmat.argmax()
        closest = numpy.unravel_index(closest, distmat.shape)
        if closest[0] not in clusters and closest[1] not in clusters:
            clusters[closest[0]] = clustersN
            clusters[closest[1]] = clustersN
            clustersN += 1
        elif closest[0] not in clusters:
            clusters[closest[0]] = clusters[closest[1]]
        elif closest[1] not in clusters:
            clusters[closest[1]] = clusters[closest[0]]
        else:
            for j in clusters:
                if clusters[j] == clusters[closest[1]]:
                    clusters[j] = clusters[closest[0]]
        distmat[closest[0],closest[1]] = 0
    print(clusters)
    return clusters


def main():
#     print(tags)
#     bag = bag_of_words(statuses,word_features)
#     distmat = get_distances(bag)
#     clusters = cluster_sentences(distmat)
#     for i in clusters:
#         print()
#         print(statuses[i])
#     cluster_words(count)
#     words = split_pattern(count)
#     patterns = get_patterns(count,0.8)
#     get_tags(statuses, count)
    pass

if __name__ == '__main__':
    main()
