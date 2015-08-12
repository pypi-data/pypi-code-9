import logging
import os
import pandas as pd
import numpy as np


complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
whatchange = {'A': 'nstf', 'C': 'snft', 'G': 'tfns', 'T': 'ftsn'}


def category(categs, f, l, r, newbase):
    oldbase = f
    if f in 'GT':
        f = complement[f]
        tmp = complement[r]
        r = complement[l]
        l = tmp

    for v in categs.values():
        # decide if belongs to this category
        if f in v['from'] and l in v['left'] and r in v['right']:
            # yes, it does
            if v['type'] == 'non-point':
                # for non-point mutations (indel/null), "newbase" doesn't matter
                return v['name']
            elif v['type'] == 'point':
                change = whatchange[oldbase]['ACGT'.index(newbase)]
                if change in v['change']:
                    return v['name']
    return "null+indel"


def preprocess(mutation_file, coverage_file, covariate_file, output_filestem, chr_files_directory, categ_flag):

    logging.info('Loading mutations file...\n')
    m = pd.read_csv(mutation_file, sep='\t')
    m.rename(columns={
        'Chromosome': 'chr',
        'Start_position': 'start',
        'Reference_Allele': 'ref_allele',
        'Tumor_Seq_Allele1': 'newbase'
    }, inplace=True)

    logging.info('Loading coverage file...\n')
    c = pd.read_csv(coverage_file, sep='\t')

    logging.info('Preparing for category discovery...\n')
    # STEP1
    # COVERAGE: get total on context65
    npm = len(m.patient.drop_duplicates())
    c['totcov'] = c.coverage * npm

    #     % will use only the coding mutations+coverage to do this
    #     C.is_coding = (strcmp(C.effect,'nonsilent')|strcmp(C.effect,'silent'));
    c_coding = c[c.effect.isin(['nonsilent', 'silent'])]

    #     % collapse coverage to 192
    #     X = [];
    #     [X.categ tmp C.categ_idx] = unique(C.categ);
    #     X = parse_in(X,'categ','(.).(.)..(.).(.)',{'left','from','to','right'});
    #     X.yname = cell(slength(X),1);
    #     X.N = nan(slength(X),1);
    #     for i=1:slength(X)
    #       X.yname{i} = [X.from{i} ' in ' X.left{i} '_' X.right{i}];
    #       X.N(i) = sum(C.totcov(C.is_coding & C.categ_idx==i));
    #     end
    #     X.newbase_idx = listmap(X.to,{'A','C','G','T'});
    c_192 = c_coding.groupby(['categ']).agg({'totcov': 'sum'}).reset_index()
    c_192['N'] = c.totcov
    c_192['yname'] = c_192.categ.apply(lambda v: "{0} in {1}_{2}".format(v[2], v[0], v[7]))
    c_192['newbase'] = c_192.categ.apply(lambda v: v[5])

    #     % collapse coverage to context65
    #     Y = generate_categ_context65_names();
    #     X.context65 = listmap(X.yname,Y.name);
    #     Y.N = nan(slength(Y),1);
    #     for i=1:slength(Y)
    #       Y.N(i) = sum(X.N(X.context65==i));
    #     end
    #     Y.N = round(Y.N/3);
    c_65 = c_192.groupby(['yname']).agg({'N': 'sum'}).reset_index()
    c_65['N'] = np.round(c_65.N / 3)

    #     % STEP2
    #     % MUTATIONS: get context65 by looking up from reference genome
    #     fprintf('Looking up trinucleotide contexts from chr_files...\n');
    #     M.triplet = repmat({'---'},slength(M),1);
    #     for ci=1:length(uchr), fprintf(' %d/%d',ci,length(uchr));
    #       midx = find(M.chr_idx==ci);
    #       chrfile = f2{ci};
    #       d = dir(chrfile);
    #       if isempty(d), continue; end
    #       filesize = d.bytes;
    #       ff = fopen(chrfile);
    #       for i=1:length(midx),mi=midx(i);
    #         leftpos = M.start(mi)-1;
    #         if leftpos>1 && leftpos+2<=filesize
    #           status = fseek(ff, leftpos-1, 'bof');
    #           M.triplet{mi} = fgets(ff,3);
    #         end
    #       end
    #     end, fprintf('\n');
    #     M.triplet = upper(M.triplet);
    #     M = parse_in(M,'triplet','^.(.).$','triplet_middle');
    #     midx = find(~strcmp('-',M.ref_allele)&~strcmp('-',M.newbase));
    #     matchfrac = mean(strcmpi(M.ref_allele(midx),M.triplet_middle(midx)));
    #     if matchfrac<0.9
    #       adj = 'possible'; if matchfrac<0.7, adj = 'probable'; end
    #       error('%s build mismatch between mutation_file and chr_files', adj);
    #     end
    #     M.yname = regexprep(M.triplet,'^(.)(.)(.)$','$2 in $1_$3');
    #     M.context65 = listmap(M.yname,Y.name);
    #     M.newbase_idx = listmap(regexprep(M.newbase,'^(.).*','$1'),{'A','C','G','T'});
    def get_yname(chr, start):
        with open(os.path.join(chr_files_directory, "chr{0}.txt".format(chr)), 'rb') as fd:
            fd.seek(start-2)
            triplet = fd.read(3).decode().upper()
            return "{0} in {1}_{2}".format(triplet[1], triplet[0], triplet[2])

    m['yname'] = m.apply(lambda v: get_yname(
        v[m.columns.get_loc('chr')],
        v[m.columns.get_loc('start')]
    ), axis=1)

    #     midx = find(~strcmp('-',M.ref_allele) & ~strcmp('-',M.newbase) & M.context65>=1 & M.context65<=65 & M.newbase_idx>=1 & M.newbase_idx<=4);
    #     Y.n = hist2d(M.context65(midx),M.newbase_idx(midx),1:65,1:4);
    midx = m[(m.newbase != '-') & (m.ref_allele != '-')]
    #TODO

    #     % STEP3
    #     % Category Discovery
    #     Nn = collapse_Nn_65_to_32([Y.N Y.n]);
    #     PP=[]; PP.max_k = ncategs;
    #     PP.mutcategs_report_filename = [output_filestem '.mutcateg_discovery.txt'];
    #     Ks = find_mut_categs(Nn,PP);
    #     K = Ks{ncategs};
    #     c = assign_65x4_to_categ_set(K);
    #     X.kidx = nan(slength(X),1);
    #     for i=1:slength(X)
    #       X.kidx(i) = find(c(X.context65(i),:,X.newbase_idx(i)));
    #     end
    #
    #     % STEP4
    #     % assign mutation categories
    #     fprintf('Assigning mutation categories...\n');
    #     M.categ = repmat({'---'},slength(M),1);
    #     for i=1:slength(X)
    #       idx=find(M.context65==X.context65(i) & M.newbase_idx==X.newbase_idx(i));
    #       M.categ(idx) = repmat(K.name(X.kidx(i)),length(idx),1);
    #     end
    #     % add null+indel category
    #     K2 = [];
    #     K2.left = {'ACGT'};
    #     K2.from = {'AC'};
    #     K2.change = {'in'};
    #     K2.right = {'ACGT'};
    #     K2.autoname = {'null+indel'};
    #     K2.name = {'null+indel'};
    #     K2.type = {'non-point'};
    #     K = concat_structs_keep_all_fields({K,K2});
    #     K.N(end) = sum(K.N(1:end-1));
    #     midx = find(strcmp('null',M.effect));
    #     M.categ(midx) = repmat(K2.name(end),length(midx),1);
    #     K.n(end) = length(midx);
    #     K.rate(end) = K.n(end)/K.N(end);
    #     K.relrate(end) = K.rate(end)/K.rate(1)*K.relrate(1);
    #
    #     % STEP5
    #     % collapse coverage
    #
    #     fprintf('Collapsing coverage...\n');
    #     C = sort_struct(C,{'gene','effect','categ_idx'});
    #     ug = unique(C.gene); ng = length(ug);
    #     ue = unique(C.effect); ne = length(ue);
    #     nk = slength(K);
    #
    #     idx = find(C.categ_idx<=nk);
    #     C2 = reorder_struct(C,idx);
    #     C2.categ = nansub(K.name,C2.categ_idx);
    #     C2 = keep_fields(C2,{'gene','effect','categ'});
    #
    #     np = length(coverage_patient_names);
    #     for p=1:np
    #       oldcov = reshape(C.(coverage_patient_names{p}),[192 ne ng]);
    #       newcov = nan(nk,ne,ng);
    #       for ki=1:nk
    #         if ki==nk
    #           cidx = 1:192;  % null+indel = total territory
    #         else
    #           cidx = find(X.kidx==ki);
    #         end
    #         newcov(ki,:,:) = sum(oldcov(cidx,:,:),1);
    #       end
    #       C2.(coverage_patient_names{p}) = newcov(:);
    #     end
    #     C=C2; clear C2;
    #
    #   end
    #
    #   % SAVE OUTPUT FILES
    #
    #   fprintf('Writing preprocessed files.\n');
    #
    #   % (1) mutation file
    #   M = rmfield_if_exist(M,{'newbase','chr_idx','triplet','yname','context65','newbase_idx','context65_right','triplet_middle'});
    #   save_struct(M,[output_filestem '.mutations.txt']);
    #
    #   % (2) coverage file
    #   save_struct(C,[output_filestem '.coverage.txt']);
    #
    #   % (3) categories file
    #   save_struct(K,[output_filestem '.categs.txt']);
    #
    #   fprintf('MutSig_preprocess finished.\n');
    #
    # end % end of MutSig_preprocess
