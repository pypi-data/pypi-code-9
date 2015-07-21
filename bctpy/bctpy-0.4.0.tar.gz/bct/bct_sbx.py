#	(C) Roan LaPlante 2013 rlaplant@nmr.mgh.harvard.edu
#
#	This program is BCT-python, the Brain Connectivity Toolbox for python.
#
#	BCT-python is based on BCT, the Brain Connectivity Toolbox.  BCT is the
# 	collaborative work of many contributors, and is maintained by Olaf Sporns
#	and Mikail Rubinov.  For the full list, see the associated contributors.
#
#	This program is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
import numpy as np
import bct

def comodularity_und(a1,a2):
    '''
    Returns the comodularity, an experimental measure I am developing.
    The comodularity evaluates the correspondence between two community
    structures A and B.  Let F be the set of nodes that are co-modular (in the
    same module) in at least one of these community structures.  Let f be the
    set of nodes that are co-modular in both of these community structures.
    The comodularity is |f|/|F|

    This is actually very similar to the Jaccard index which turns out not
    to be a terribly useful property. At high similarity a the variability
    of information is better. It may be that the degenerate cross modularity
    is even better though.
    '''

    ma,qa=bct.modularity_und(a1)
    mb,qb=bct.modularity_und(a2)

    n=len(ma)
    if len(mb)!=n:
        raise bct.BCTParamError('Comodularity must be done on equally sized '
            'matrices')

    E,F,f,G,g,H,h=(0,)*7

    for e1 in xrange(n):
        for e2 in xrange(n):
            if e2>=e1: continue

            #node pairs
            comod_a = ma[e1]==ma[e2] 
            comod_b = mb[e1]==mb[e2]

            #node pairs sharing a module in at least one graph
            if comod_a or comod_b:
                F+=1
            #node pairs sharing a module in both graphs
            if comod_a and comod_b:
                f+=1

            #edges in either graph common to any module
            if a1[e1,e2] != 0 or a2[e1,e2] != 0:
                #edges that exist in at least one graph which prepend a shared
                #module in at least one graph:
                #EXTREMELY NOT USEFUL SINCE THE SHARED MODULE MIGHT BE THE OTHER
                #GRAPH WITH NO EDGE!
                if comod_a or comod_b:
                    G+=1
                #edges that exist in at least one graph which prepend a shared
                #module in both graphs:
                if comod_a and comod_b:
                    g+=1

                #edges that exist at all
                E+=1

            #edges common to a module in both graphs
            if a1[e1,e2] != 0 and a2[e1,e2] != 0:
                #edges that exist in both graphs which prepend a shared module
                #in at least one graph
                if comod_a or comod_b:
                    H+=1
                #edges that exist in both graphs which prepend a shared module
                #in both graphs
                if comod_a and comod_b:
                    h+=1


    m1 = np.max(ma)
    m2 = np.max(mb)
    P=m1+m2-1

    #print f,F
    print m1,m2
    print 'f/F', f/F
    print '(f/F)*p', f*P/F
    print 'g/E', g/E
    print '(g/E)*p', g*P/E
    print 'h/E', h/E
    print '(h/E)*p', h*P/E
    print 'h/H', h/H
    print '(h/H)*p', h*P/E
    print 'q1, q2', qa, qb
    #print 'f/F*sqrt(qa*qb)', f*np.sqrt(qa*qb)/F
    return f/F

def comod_test(a1,a2):
    ma,qa=bct.modularity_und(a1)
    mb,qb=bct.modularity_und(a2)

    n=len(ma)
    if len(mb)!=n:
        raise BCTParamError('Comodularity must be done on equally sized '
            'matrices')

    f,F=(0,)*2

    for e1 in xrange(n):
        for e2 in xrange(n):
            if e2>=e1: continue

            #node pairs
            comod_a = ma[e1]==ma[e2] 
            comod_b = mb[e1]==mb[e2]

            #node pairs sharing a module in at least one graph
            if comod_a or comod_b:
                F+=1
            #node pairs sharing a module in both graphs
            if comod_a and comod_b:
                f+=1

    m1=np.max(ma)
    m2=np.max(mb)
    eta=[]
    gamma=[]
    for i in xrange(m1):
        eta.append(np.size(np.where(ma==i+1)))
    for i in xrange(m2):
        gamma.append(np.size(np.where(mb==i+1)))

    scale,conscale = (0,)*2
    for h in eta:
        for g in gamma:
            #print h,g
            conscale += (h*g)/(n*(h+g)-h*g)
            scale+= (h*h*g*g)/(n**3*(h+g)-n*h*g)

    print m1,m2
#	print conscale
    print scale
    return (f/F)/scale

def cross_modularity(a1,a2):
    '''
    return the cross modularity from estimates of optimal partitions,
    without sampling the space of degenerate partitions
    '''
    #There are some problems with my code #There are?
    ma,_=bct.modularity_louvain_und_sign(a1)
    mb,_=bct.modularity_louvain_und_sign(a2)

    ma,qa=bct.modularity_finetune_und_sign(a1, ci=ma)
    mb,qb=bct.modularity_finetune_und_sign(a2, ci=mb)

    _,qab=bct.modularity_und_sign(a1,mb)
    _,qba=bct.modularity_und_sign(a2,ma)

    return (qab+qba)/(qa+qb)

def modularity_matching(a1, a2):
    return cross_modularity(a1, a2)

def modularity_matching_degenerate(a1, a2, quiet=True):
    return cross_modularity_degenerate(a1, a2, quiet=quiet)

def entropic_similarity(a1,a2):
    ma,_=bct.modularity_und(a1)
    mb,_=bct.modularity_und(a2)

    vi,_=bct.partition_distance(ma,mb)
    return 1-vi

def dice_complete_und(a1, a2):
    a1 = bct.binarize(a1)
    a2 = bct.binarize(a2)

    np.fill_diagonal(a1, 0)
    np.fill_diagonal(a2, 0)

    return 2*np.sum(np.logical_and(a1, a2))/(np.sum(a1)+np.sum(a2))

def sample_degenerate_partitions(w, probtune_cap=.10, modularity_cutoff=.95, quiet=True):
    ntries=0
    while True:
        init_ci,_ = bct.modularity_louvain_und_sign(w)
        seed_ci, seed_q = bct.modularity_finetune_und_sign(w, ci=init_ci)	

        p = (np.random.random() * probtune_cap)
        ci,q = bct.modularity_probtune_und_sign(w, ci=seed_ci, p=p)
        if q > (seed_q * modularity_cutoff):
            if not quiet:
                print ('found a degenerate partition after %i tries with probtune ' 
                    'parameter %.3f: %.5f %.5f'%(ntries,p,q,seed_q))
            ntries=0
            yield ci,q
        else:
            #print 'failed to find degenerate partition, trying again',q, seed_q
            ntries+=1
            
def cross_modularity_degenerate(a1,a2,n=20, quiet=False):
    '''
    return the degenerate cross modularity between networks A1 and A2.
    this means, sample from the degenerate partition space for these
    networks and return the cross modularity over a parameterized number of 
    comparisons between degenerate partitions
    '''
    a_degenerator = sample_degenerate_partitions(a1, quiet=quiet)
    b_degenerator = sample_degenerate_partitions(a2, quiet=quiet)

    accum=0
    for i in xrange(n):
        a_ci, qa = a_degenerator.next()
        b_ci, qb = b_degenerator.next()
        _,qab = bct.modularity_und_sign(a1, b_ci)
        _,qba = bct.modularity_und_sign(a2, a_ci)
        res = (qab+qba)/(qa+qb)
        accum+=res
        #print 'trial %i, degenerate modularity %.3f'%(i,res)
        print 'trial %i, metric so far %.3f'%(i,accum/(i+1))

    return accum/n

def makerand_representative_module_und_2parts(canon_mod, inmod_p=.25, outmod_p=.05):
    '''
    create a graph out of a representative module, with different probabilities
    for wiring inside the module and outside of it.
    '''
    n = np.size(canon_mod)
    m = np.size(np.where(canon_mod))

    cix,=np.where(canon_mod)
    ncix,=np.where(canon_mod==0)
    
    C = np.zeros((n,n))
    C[np.ix_(cix,cix)]=1
    C[np.ix_(ncix,ncix)]=2

    #inmod_ix,=np.where(np.triu(np.ones((m,m)),1).flat)
    #outmod_ix,=np.where(np.triu(np.ones((n-m,n-m)),1).flat)
    inmod_ix=np.where((np.triu(C,1)==1).flat)
    outmod_ix=np.where((np.triu(C,2)==2).flat)

    A = np.zeros((n,n))
    rp = np.random.random((m*m+m)/2)
    #A[np.ix_(cix,cix)].flat[inmod_ix]=(rp<inmod_p)
    A.flat[inmod_ix] = (rp<inmod_p)

    rp = np.random.random(((n-m)*(n-m+1))/2)
    #A[np.ix_(ncix,ncix)].flat[outmod_ix]=(rp<outmod_p)
    A.flat[outmod_ix] = (rp<outmod_p)
    A=A+A.T
    return A

def makerand_representative_module_und(canon_mod, inmod_p=.25, outmod_p=.05,
        neutral_p=.25):
    '''
    create a graph out of a representative module with separate probabilities
    for wiring within the target module, within the background module,
    and across modules
    '''
    n = np.size(canon_mod)
    m = np.size(np.where(canon_mod))

    cix,=np.where(canon_mod)
    ncix,=np.where(canon_mod==0)

    C = np.zeros((n,n))
    C[np.ix_(cix,cix)]=1
    C[np.ix_(ncix,ncix)]=3
    C[np.ix_(cix,ncix)]=2
    C[np.ix_(ncix,cix)]=2

    inmod_ix=np.where((np.triu(C,1)==1).flat)
    outmod_ix=np.where((np.triu(C,1)==2).flat)
    neutral_ix=np.where((np.triu(C,1)==3).flat)

    A = np.zeros((n,n))
    rp = np.random.random((m*m+m)/2) 
    A.flat[inmod_ix] = (rp<inmod_p)

    rp = np.random.random(((n-m)*(n-m+1))/2)
    A.flat[outmod_ix] = (rp<outmod_p)

    rp = np.random.random(m*(n-m)/2)
    A.flat[neutral_ix] = (rp<neutral_p)

    A=A+A.T
    return A

def makefixedbg_representative_module_und(canon_mod, orig, inmod_p=.4):
    '''
    create a graph out of a representative module, but keep all other
    connections identical to the original graph
    '''
    n = np.size(canon_mod)
    m = np.size(np.where(canon_mod))

    cix,=np.where(canon_mod)

    C = np.zeros((n,n))
    C[np.ix_(cix,cix)]=1

    inmod_ix = np.where((np.triu(C,1)==1).flat)

    A = orig.copy()
    A/=2
    rp = np.random.random((m*m+m)/2)
    A.flat[inmod_ix] = (rp<inmod_p)

    A=A+A.T
    return A

def make_totally_random_matrix(n, conn_p=.4):
    return bct.makerandCIJ_und(n, int((n*(n-1)/2)*conn_p))

def cross_modularity_index(a1, canonical_ci, n=100, inmod_p=.25, outmod_p=.05,
        neutral_p=.25, probtune_cap=.1, modularity_cutoff=.95, quiet=True):
    '''
    returns the cross modularity between repeated samples of degenerate
    partitions for the network A1, with a canonical ground truth partition.

    This partition is typically expected to be a single module, such as a
    canonically constructed module of the default mode network, along with
    another general module that includes everything else.

    We construct a network with high density within the single module, and
    low density elsewhere. Then we sample from the degenerate partition space
    between the true network and the representative module network. For each
    degenerate partition in the real network, we create a new high density
    representative-module network.
    '''
    a_degenerator = sample_degenerate_partitions(a1, probtune_cap=probtune_cap,
        modularity_cutoff=modularity_cutoff)

    accum=0
    for i in xrange(n):
        a_ci, qa = a_degenerator.next()

        b = makerand_representative_module_und(canonical_ci, inmod_p=inmod_p,
           outmod_p=outmod_p, neutral_p=neutral_p)
        #b = makefixedbg_representative_module_und(canonical_ci, a1, 
        #    inmod_p=inmod_p)
        #b = make_totally_random_matrix(len(a1), inmod_p)
        raw_b_ci,_ = bct.modularity_louvain_und_sign(b)
        b_ci, qb = bct.modularity_finetune_und_sign(b, ci=raw_b_ci)
        #_,qb = bct.modularity_und_sign(b,canonical_ci)
            #doing this with the canonical_ci every time is really bad
            #qba turns out to be zero always and 
            #qb turns out to be constant and small
            #doing this instead causes low values but is more consistent
        _,qab = bct.modularity_und_sign(a1, b_ci)
        _,qba = bct.modularity_und_sign(b, a_ci)
        eth_q = (qab+qba)/(qa+qb)
        accum += eth_q 

        if not quiet:
            print 'trial %i, metric so far %.3f'%(i,accum/(i+1))
        
    return accum/n     

def simple_modularity_index(a1, canonical_ci, n=100, probtune_cap=.1,
        modularity_cutoff=.95, quiet=True, normalize_by='data'):
    '''
    returns the simple modularity
    this is the ratio of the modularity of the network with the default mode
    network, over the modularity of repeatedly sampled degenerate partitions
    '''

    _, qac = bct.modularity_und_sign(a1, canonical_ci)
    if normalize_by in ('canonical network','canon','canonical'):
        n = np.size(canonical_ci)
        m = np.size(np.where(canonical_ci)) 
        norm = 2*m*(n-m)/(n*n)
        ewe_q = qac/norm
        print qac,ewe_q
        return ewe_q
    elif normalize_by == 'data':
        a_degenerator = sample_degenerate_partitions(a1, 
            probtune_cap=probtune_cap, modularity_cutoff=modularity_cutoff,
            quiet=True)

        accum=0
        for i in xrange(n):
            _, qa = a_degenerator.next()
            norm = qa
            ewe_q = qac/norm
            # ewe is the pan-nigerian letter for alveolar implosive
            accum += ewe_q

            if not quiet:
                print 'trial %i, metric so far %.3f'%(i,accum/(i+1))

        return accum/n
    else:
        raise ValueError('invalid normalization type, use "data" or "canon"')

def cross_modularity_degenerate_rate(a1,a2,omega,n=100):
    ''' 
    checks the number of trials that the degenerate cross modularity between
    networks A1 and A2 is greater than some hyperparameter omega
    '''
    a_degenerator = sample_degenerate_partitions(a1)
    b_degenerator = sample_degenerate_partitions(a2)

    #rate=0
    for i in xrange(n):
        a_ci,qa = a_degenerator.next()
        b_ci,qb = b_degenerator.next()
        _,qab = bct.modularity_und_sign(a1, b_ci)
        _,qba = bct.modularity_und_sign(a2, a_ci)
        eth_q = (qab+qba)/(qa+qb)
        if eth_q > omega:
            rate+=1
        print 'trial %i, ethq=%.3f, estimated p-value %.3f for omega %.2f'%(
            i,eth_q,(i+1-rate)/(i+1),omega)

    return (n-rate)/n

def cross_modularity_degenerate_raw(a1,a2,n=25,mc=.95,pc=.1):
    a_degenerator = sample_degenerate_partitions(a1,modularity_cutoff=mc,
        probtune_cap=pc)
    b_degenerator = sample_degenerate_partitions(a2,modularity_cutoff=mc,
        probtune_cap=pc)

    raw = []
    for i in xrange(n):
        a_ci,qa = a_degenerator.next()
        b_ci,qb = b_degenerator.next()
        _,qab = bct.modularity_und_sign(a1, b_ci)
        _,qba = bct.modularity_und_sign(a2, a_ci)
        eth_q = (qab+qba)/(qa+qb)

        print 'trial %i, ethq=%.3f'%(i,eth_q)
        raw.append(eth_q)

    return raw

def nonparametric_similarity_test(similarity_metric,a1,a2,null_model_gen_a1,
        null_model_gen_a2,nshuff=1000):
    '''
    null_model_gen_a[1-2] are generators that produce appropriate null models.
    you can manually use stupid null models like randmio if you want.
    '''
    true_similarity = similarity_metric(a1,a2)	

    count=0.
    for shuff in xrange(1,nshuff+1):
        flip = np.random.random() > .5
        if flip:
            #a1_surr,_ = bct.null_model_und_sign(a1,bin_swaps=1)
            #a1_surr,_ = bct.null_model_und_sign(a1)
            #a1_surr = bct.randmio_und(a1, 1)[0]
            a1_surr = null_model_gen_a1.next()
            a2_surr = a2
        else:
            a1_surr = a1
            #a2_surr = bct.randmio_und(a2, 1)[0]
            #a2_surr,_ = bct.null_model_und_sign(a2,bin_swaps=1)
            #a2_surr,_ = bct.null_model_und_sign(a2)
            a2_surr = null_model_gen_a2.next()
        
        surrogate_similarity = similarity_metric(a1_surr,a2_surr)
        if surrogate_similarity > true_similarity:
            count+=1
        print 'surrogate similarity %.3f, true similarity %.3f'%(
            surrogate_similarity, true_similarity)
        print 'trial %i, p-value estimate so far %.4f'%(shuff, count/shuff)

    p = count/nshuff
    print 'test complete, p-value %.4f'%p
    return p 

#def null_covariance(e,v,ed,n):
def null_covariance(W, sd):
    '''
Uses the Hirschberg-Qi-Steuer algorithm to generate a null correlation matrix
appropriate for use as a null model that is matched to the given correlation 
matrix in node mean and variance, as well as average covariance.

Inputs:	W, the NxN adjacency matrix which should be a correlation matrix of
            R timepoints or observations
        sd, An Nx1 vector of standard deviations for each ROI timeseries 

Output: C, a null model adjacency matrix

see Zalesky et al. (2012) "On the use of correlation as a measure of network
    connectivity"
    '''
    #transform correlation matrix to covariances
    a = np.diag(sd)
    W = np.dot(a, np.dot(W, a)) 

    n = len(W)
    sdd = np.diag(sd)
    w = np.dot(sdd, np.dot(W, sdd))
    e = np.mean(np.triu(w, 1))
    v = np.var(np.triu(w, 1))
    ed = np.mean(np.diag(w))

    m = np.max( (2, np.floor((e**2 - ed**2)/v)) )
    mu = np.sqrt(e/m)
    sigma = np.sqrt(-mu**2 + np.sqrt(mu**4 + v/m))

    from scipy import stats
    x = stats.norm.rvs(loc=mu, scale=sigma, size=(n,m))
    c = np.dot(x, x.T)

    #transform result to correlation matrix
    a = np.diag(1 / np.diag(c))
    return np.dot(a, np.dot(c, a))

def mantel(a,b,n=1000):
    np.fill_diagonal(a,0)
    np.fill_diagonal(b,0)
    k = len(a)

    an = bct.normalize(a)
    bn = bct.normalize(b)

    true_mantel = bct.corr_flat_und(a,b)   
    hits = 0
    for i in xrange(n):
        rand_a = a[:, np.random.permutation(k)]
        test_mantel = bct.corr_flat_und(rand_a, b)
        if test_mantel > true_mantel:
            hits+=1

        print 'permutation %i, hits %i'%(i,hits)

    return hits/n

###############################################################################
# SMALL WORLD
###############################################################################

from bct import breadthdist,charpath,invert
from bct import (clustering_coef_bd, clustering_coef_bu, clustering_coef_wd,
    clustering_coef_wu, distance_wei)

def small_world_bd(W):

    '''
    An implementation of small worldness. Returned is the coefficient cc/lambda,
    the ratio of the clustering coefficient to the characteristic path length.
    This ratio is >>1 for small world networks.

    inputs: W		weighted undirected connectivity matrix
    
    output: s		small world coefficient
    '''
    cc = clustering_coef_bd(W)
    _,dists = breadthdist(W)
    _lambda,_,_,_,_ = charpath(dists)
    return np.mean(cc)/_lambda

def small_world_bu(W):
    '''
    An implementation of small worldness. Returned is the coefficient cc/lambda,
    the ratio of the clustering coefficient to the characteristic path length.
    This ratio is >>1 for small world networks.

    inputs: W		weighted undirected connectivity matrix
    
    output: s		small world coefficient
    '''
    cc = clustering_coef_bu(W)
    _,dists = breadthdist(W)
    _lambda,_,_,_,_ = charpath(dists)
    return np.mean(cc)/_lambda

def small_world_wd(W):
    '''
    An implementation of small worldness. Returned is the coefficient cc/lambda,
    the ratio of the clustering coefficient to the characteristic path length.
    This ratio is >>1 for small world networks.

    inputs: W		weighted undirected connectivity matrix
    
    output: s		small world coefficient
    '''
    cc = clustering_coef_wd(W)
    _,dists = breadthdist(W)
    _lambda,_,_,_,_ = charpath(dists)
    return np.mean(cc)/_lambda

def small_world_wu(W):
    '''
    An implementation of small worldness. Returned is the coefficient cc/lambda,
    the ratio of the clustering coefficient to the characteristic path length.
    This ratio is >>1 for small world networks.

    inputs: W		weighted undirected connectivity matrix
    
    output: s		small world coefficient
    '''
    cc = clustering_coef_wu(W)
    #_,dists = breadthdist(W)
    dists,_ = distance_wei(invert(W))
    _lambda,_,_,_,_ = charpath(dists)
    return np.mean(cc)/_lambda

def small_sigma(W, weighted=False):
    '''
    An implementation of small world coefficient (C/Crand)/(L/Lrand)
    '''
    from bct import randmio_und, clustering_coef_wu, distance_wei, charpath

    equiv_rand,_ = randmio_und(W, 5)
    c = np.mean(clustering_coef_wu(W))
    cr = np.mean(clustering_coef_wu(equiv_rand))

    #_,dists = breadthdist(W)
    if weighted:
        dists,_ = distance_wei(W)
        dists_r,_ = distance_wei(equiv_rand)
    else:
        _,dists = distance_wei(W)
        _,dists_r = distance_wei(equiv_rand)

    _lambda,_,_,_,_ = charpath(dists)
    lambda_r,_,_,_,_ = charpath(dists_r)
    
    print c,cr,_lambda,lambda_r
    sigma = (c/cr)/(_lambda/lambda_r)
    return sigma

def small_omega(W, weighted=False):
    '''
    An implementation of small world coefficient (L/Lrand - C/Clatt)
    '''
    from bct import (randmio_und, latmio_und, clustering_coef_wu, distance_wei, 
        charpath)

    equiv_rand,_ = randmio_und(W, 5)
    equiv_latt,_,_,_ = latmio_und(W, 5)

    c = np.mean(clustering_coef_wu(W))
    cl = np.mean(clustering_coef_wu(equiv_latt))

    if weighted:
        dists,_ = distance_wei(W)
        dists_r,_ = distance_wei(equiv_rand)
    else:
        _,dists = distance_wei(W)
        _,dists_r = distance_wei(equiv_rand)

    _lambda,_,_,_,_ = charpath(dists)
    lambda_r,_,_,_,_ = charpath(dists_r)
    
    omega = (lambda_r/_lambda) - (c/cl)
    return omega
