from scipy.stats import chisqprob


def lap_ppv(df):

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

    # x1 <- datamat[,5]
    # n1 <- datamat[,1]+datamat[,5]
    # x2 <- datamat[,6]
    # n2 <- datamat[,2]+datamat[,6]
    # x3 <- datamat[,7]
    # n3 <- datamat[,3]+datamat[,7]

    d_prime = (xAG + xBG) / (nA + nB)
    z_prime = nB / (nA + nB)

    numerator = (xBG - nB * (xAG + xBG) / (nA + nB))**2

    denominator = ((0 - d_prime)**2) * ((n1 - x1) * (1 - 2 * z_prime)**2 + (n2 - x2)*(0 - 1 * z_prime)**2+(n3 - x3)*(1 - 1 * z_prime)**2)+((1 - d_prime)**2) * (x1 * (1 - 2 * z_prime)**2 + x2 * (0 - 1 * z_prime)**2 + x3 * (1 - 1 * z_prime)**2)

    test_observation = numerator / denominator

    df["chi_sq"] = chisqprob(test_observation, 1)
    df["test_obs"] = test_observation

    return df
