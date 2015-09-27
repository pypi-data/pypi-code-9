import numpy as np
import cosmolopy as cp

crossections = np.loadtxt('radiator/datafiles/crossdata.dat')
crossectionsHe = np.loadtxt('radiator/datafiles/crossdataHe.dat')
crossectionsO = np.loadtxt('radiator/datafiles/crossdataO.dat')
crossectionsHe2 = np.loadtxt('radiator/datafiles/photoionHe.dat')

def photon_absorption(cs, E_ph_initial, z_start, bins=100, total_mocks=1000, z_end = 0.0):
    '''
    Function assumes fully neutral medium with 0 overdensity.
    :param E_ph_initial:
    :param z_start:
    :param bins:
    :param total_mocks:
    :param z_end:
    :return:
    '''
    nb = cp.cden.baryon_densities(**cp.fidcosmo)[0] / cp.constants.Mpc_cm**3 * cp.constants.M_sun_g / cp.constants.m_p_g * 0.04
    c = 2.9979e10 # cm/s

    z_list = np.logspace(np.log10(z_start+1-0.01), np.log10(z_end+1), bins-1)-1.0
    z_list = np.append([z_start], z_list)
    age_list = cp.distance.age(z_list, **cp.fidcosmo)
    results = np.zeros(len(z_list))
    resultsH = np.zeros(len(z_list))
    resultsHe = np.zeros(len(z_list))

    E_redshift_total = np.zeros(bins)
    E_other_total = np.zeros(bins)
    E_other_total_H = np.zeros(bins)
    E_other_total_He = np.zeros(bins)
    E_remaining_total = np.zeros(bins)

    for iii in range(total_mocks):
        randomii = np.random.random([len(z_list), 10])
        E_ph = 1.0*E_ph_initial
        E_redshift = 0.
        E_other = 0.
        ii=0
        while (E_ph>0) and (ii < (len(z_list)-2)):
            ii = ii+1
            E_ph_0 = 1.0*E_ph
            z = z_list[ii]
            tau = age_list[ii+1] - age_list[ii]
            dt = tau
            # column density
            N_naked = nb*c*tau*(1+z)**3
            N_H = N_naked*0.76
            N_He = N_naked*0.23/4
            N_O = N_naked*0.01/8 # experimental
            # pair production
            temp_factor = (10**np.interp(np.log10(E_ph/1e6), np.log10(crossections[:,0]), np.log10(crossections[:,4]+crossections[:,5]))*1e-24*N_naked)
            if np.isnan(temp_factor):
                chance_pp = 0
            else:
                chance_pp = 1.0 - np.exp(-temp_factor)

            # photoion
            opt_dep_photoion_H = (cs.sigmaX([E_ph], 1, 1)[0]*1e-18*N_H)
            opt_dep_photoion_He = (cs.sigmaX([E_ph], 2, 2)[0]*1e-18*N_He)
            opt_dep_photoion_O = (cs.sigmaX([E_ph], 8, 8)[0]*1e-18*N_O)
            chance_photoion_H = 1.0 - np.exp(-opt_dep_photoion_H)
            chance_photoion_He = 1.0 - np.exp(-opt_dep_photoion_He)
            chance_photoion_O = 1.0 - np.exp(-opt_dep_photoion_O)

            # collisional ion
            temp_factor_H = (10**np.interp(np.log10(E_ph/1e6), np.log10(crossections[:,0]), np.log10(crossections[:,2]))*1e-24*N_H)
            chance_coll_ion_H = 1.0 - np.exp(-temp_factor_H)
            temp_factor_He = (10**np.interp(np.log10(E_ph/1e6), np.log10(crossectionsHe[:,0]), np.log10(crossectionsHe[:,2]))*1e-24*N_H)
            chance_coll_ion_He = 1.0 - np.exp(-temp_factor_He)

            E_other = 0
            E_other_H = 0
            E_other_He = 0

            if randomii[ii, 0] < chance_pp+chance_photoion_H+chance_coll_ion_H+chance_photoion_He+chance_coll_ion_He:
                # print iii, ii
                tempH = chance_pp+chance_photoion_H+chance_coll_ion_H
                tempHe = chance_photoion_He+chance_coll_ion_He
                tempHHe = tempH + tempHe
                tempH /= tempHHe
                tempHe /= tempHHe
                resultsH[ii] += tempH
                resultsHe[ii] += tempHe
                results[ii] += 1
                E_other_H = tempH * E_ph
                E_other_He = tempHe * E_ph
                E_other = 1.0 * E_ph
                E_ph = 0

            # redshift
            E_ph = E_ph * (z_list[ii+1]+1) / (z_list[ii]+1)
            # print np.log10(E_ph),
            E_redshift = E_ph_0 - E_ph

            E_redshift_total[ii] += E_redshift
            E_remaining_total[ii] += E_ph
            E_other_total[ii] += E_other
            E_other_total_H[ii] += E_other_H
            E_other_total_He[ii] += E_other_He
    return z_list, results, E_redshift_total, E_remaining_total, E_other_total, E_other_total_H, E_other_total_He
