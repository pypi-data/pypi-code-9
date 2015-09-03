from scipy.stats import hypergeom, rankdata, chisqprob, fisher_exact
import logging

from joblib import Memory

MEMORY = Memory(cachedir="./")


@MEMORY.cache(verbose=0)
def compute_statistics(df, gene_vectors):

    """Compute statistics for the gene lists overlap counts."""

    logging.info("Performing hypergeometric tests.")
    df = compute_go_overrepresentation_analysis(df)
    df = compute_odds_ratio(df)

    stat_method = find_appropriate_statistical_test(gene_vectors)

    if stat_method == "LAP":

        logging.info("Computing the Leisering, Alonzo and Pepe test.")
        df = lap_ppv(df)
        fdr_cols = ["a_hpgm_go", "b_hpgm_go", "chi_sq"]

    elif stat_method == "FE":

        logging.info("Computing the Fisher Exact test.")
        df = fishers_exact(df)
        fdr_cols = ["a_hpgm_go", "b_hpgm_go", "fisher"]


    elif stat_method == "FE_SUB":
        logging.info("Computing the Fisher Exact for subsets.")
        df = fishers_exact_sub(df)
        fdr_cols = ["a_hpgm_go", "b_hpgm_go", "fisher"]

    elif stat_method == "NA":

        fdr_cols = ["a_hpgm_go"]

    logging.info("Computing FDR.")
    df = compute_fdr(df, fdr_cols)

    return df


def compute_odds_ratio(df):

    df["a_odds"] = (df["a_I_go"] / df["a"]) / \
                   ((df["U"] - (df["a"] + df["go_subtree"] - df["a_I_go"])) / (df["U"] - df["a"]))


    if "b" in df:
        df["b_odds"] = (df["b_I_go"] / df["b"]) / \
                    ((df["U"] - (df["b"] + df["go_subtree"] - df["b_I_go"])) / (df["U"] - df["b"]))
    return df


def fishers_exact(df):

    """Compute Fisher Exact for diff in a and b go overlap."""

    df["fisher"] = df.apply(lambda row:
                            fisher_exact([
                                [row["a_I_go"], row["a"] - row["a_I_go"]],
                                [row["b_I_go"], row["b"] - row["b_I_go"]]
                            ], alternative="two-sided")[1],
                            axis=1)

    return df


def fishers_exact_sub(df):

    """Fisher Exact for diff in a and b go overlap when b subset of a.

    Requires |A| > |B|, which is ensured when parsing the input lists."""

    assert df.iloc[0].a > df.iloc[0].b, "Gene set a not bigger than b; this is due to a" \
        " bug - please report it."

    df["fisher"] = df.apply(lambda row:
                            fisher_exact([
                                [row.b_I_go, row.b - row.b_I_go],
                                [row.a_I_go - row.b_I_go,
                                 row.a - row.b - row.a_I_go + row.b_I_go]
                            ], alternative="two-sided")[1],
                            axis=1)

    return df


@MEMORY.cache(verbose=0)
def compute_go_overrepresentation_analysis(df):

    """Compute p-val for gene list representation in GO category.

    Uses hypergeometric test, supposed to be similar to GOstats.
    """

    df["a_hpgm_go"] = df.apply(lambda row: hypergeom.sf(row["a_I_go"] - 1,
                                                 row["U"],
                                                 row["go_subtree"],
                                                 row["a"]), axis=1)

    if "b" in df:
        df["b_hpgm_go"] = df.apply(lambda row: hypergeom.sf(row["b_I_go"] - 1,
                                                            row["U"],
                                                            row["go_subtree"],
                                                            row["b"]), axis=1)

    return df


def compute_fdr(df, columns):
    """Computes the false discovery rate for a list of columns."""

    for column in columns:
        cp = df[column]
        fdr_col = column + "_fdr"

        # Using the length of the vector without NAs because NAs indicate
        # that an experiment wasn't performed so you do not have to adjust
        # for it.
        df[fdr_col] = cp * len(cp.dropna()) / rankdata(cp)

        df.loc[df[fdr_col] > 1, fdr_col] = 1

    return df


def lap_ppv(df):

    """Computes the Generalized Score Statistic for Comparison of PPVs

    (The generalized score statistic was proposed by Leisenring, Alonzo and Pepe
    (2000), hence the name lap_ppv.)

    This is a test used to compare the positive predictive value (PPV) of
    two gene lists with regards to the gene list associated with an ontology.

    That is, for three gene lists A and B and O (the genes associated
    with an ontology term), it computes the PPV for A and B with regards to O,
    then compares the two PPVs to see whether they are significantly different.

    For a gene list A and an ontology gene list O, the PPV is just

    PPV = TP/(TP + FP)

    where

    TP = A set subtract O

    while

    FP = A set intersect O.

    This method should be used when lists A and B are not disjoint and one list
    is not a proper subset of the other.

    Alternative description:

    'Performs a test for differences in (positive and negative) predictive
    values of two binary diagnostic tests using a generalized score statistic
    proposed by Leisenring, Alonzo and Pepe'
    ( From https://cran.r-project.org/web/packages/DTComPair/DTComPair.pdf )

    Literature:

    Leisenring, W., Alonzo, T., and Pepe, M. S. (2000). Comparisons of
    predictive values of binary medical diagnostic tests for paired designs.
    Biometrics, 56(2):345-51.

    Clara-Cecilie Gunther, Mette Langaas and Stian Lydersen, 2006: Statistical
    Hypothesis Testing of Association Between Two Lists of Genes for a Given
    Gene Class

    Beisvaag et al 2006: GeneTools - application for functional annotation
    and statistical hypothesis testing.
    (The Leisering test is described there as "the intersecting target-target
    situation" and used in the exactly same way as here.)

    ------------------------------------------------------------------------
    This is the R code this function is based on (thanks Mette Langaas!)

    LAPtestPPV <- function(datamat)
    {
    #faar inn data paa formen n1,n2,n3,...,n8
    x1 <- datamat[,5]
    n1 <- datamat[,1]+datamat[,5]
    x2 <- datamat[,6]
    n2 <- datamat[,2]+datamat[,6]
    x3 <- datamat[,7]
    n3 <- datamat[,3]+datamat[,7]

    nA <- n1+n2
    nB <- n1+n3

    xAG <- x1+x2
    xBG <- x1+x3

    Dstrek <- (xAG+xBG)/(nA+nB)
    Zstrek <- nB/(nA+nB)

    teller2 <- (xBG-nB*(xAG+xBG)/(nA+nB))^2
    # 6 sums: first 3 with G*: AsnittB, AsnittB*, A*snittB, then with G
    nevner2 <-
((0-Dstrek)^2)*((n1-x1)*(1-2*Zstrek)^2+(n2-x2)*(0-1*Zstrek)^2+(n3-x3)*(1-1*Zstrek)^2)+((1-Dstrek)^2)*(x1*(1-2*Zstrek)^2+x2*(0-1*Zstrek)^2+x3*(1-1*Zstrek)^2)


    testobs <- teller2/nevner2
    pvalchisq <- pchisq(testobs,1,lower.tail=F)
    return(list(pval=pvalchisq,testobs=testobs))

    }

    """

    x1 = df["a_I_b"]
    n1 = x1 + df["a_I_b_I_go"]
    x2 = df["a_M_b_I_go"]
    n2 = x2 + df["a_I_b_I_go"]
    x3 = df["b_M_a_I_go"]
    n3 = df["a_I_b_I_go"] + x3

    nA = n1 + n2
    nB = n1 + n3

    xAG = x1 + x2
    xBG = x1 + x3

    d_prime = (xAG + xBG) / (nA + nB)
    z_prime = nB / (nA + nB)

    numerator = (xBG - nB * (xAG + xBG) / (nA + nB))**2

    denominator = ((0 - d_prime)**2) * \
                  ((n1 - x1) * (1 - 2 * z_prime)**2 + (n2 - x2)* \
                   (0 - 1 * z_prime)**2+(n3 - x3)*(1 - 1 * z_prime)**2)+ \
                   ((1 - d_prime)**2) * \
                   (x1 * (1 - 2 * z_prime)**2 + x2 * (0 - 1 * z_prime)**2 + \
                    x3 * (1 - 1 * z_prime)**2)

    test_observation = numerator / denominator

    df["chi_sq"] = chisqprob(test_observation, 1)
    df["test_obs"] = test_observation

    return df


def find_appropriate_statistical_test(gene_vectors):

    """Find the appropriate statistical test.

    The statistical test to use to decide whether there is a statistically
    significant difference between the overrepresentation of 1) gene list a in GO
    and 2) gene list b in GO.

    If there is only one input gene list, or the lists contain the same genes,
    do not perform a significance test of the difference.

    If one input gene list is a subset of the other, or they are disjoint,
    use Fisher's Exact.

    If the lists are intersecting, but they are not proper subsets/supersets of
    each other, use the LAP test.
    """

    if len(gene_vectors) == 1:
        return "NA"

    genes_a, genes_b = gene_vectors
    genes_a, genes_b = set(genes_a), set(genes_b)

    if genes_a == genes_b:
        logging.warning("Gene list A is equal to B. Only hypergeometric tests"
                        " are performed.")
        return "NA"
    elif genes_b.issubset(genes_a): # a subset of b is impossible, |a| > |b|
        return "FE_SUB"
    elif not genes_a.intersection(genes_b):
        return "FE"
    else:
        # The gene lists are intersecting, but not proper
        # subsets so Fishers Exact can't be used.
        return "LAP"
