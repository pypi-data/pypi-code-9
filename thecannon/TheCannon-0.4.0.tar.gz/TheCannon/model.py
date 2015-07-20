from .dataset import Dataset
from .train_model import _train_model 
from .infer_labels import _infer_labels
from .helpers.triangle import corner
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from copy import deepcopy

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

LARGE = 200.
SMALL = 1. / LARGE

class CannonModel(object):
    def __init__(self, order):
        self.coeffs = None
        self.scatters = None
        self.chisqs = None
        self.pivots = None
        self.order = order


    @property
    def model(self):
        """ Return the model definition or raise an error if not trained """
        if self.coeffs is None:
            raise RuntimeError('Model not trained')
        else:
            return self.coeffs


    def train(self, data):
        """ Run training step: solve for best-fit spectral model """
        self.coeffs, self.scatters, self.chisqs, self.pivots = _train_model(data)


    def diagnostics(self):
        """ Produce a set of diagnostics plots about the model. """
        _model_diagnostics(self.dataset, self.model)


    def infer_labels(self, dataset):
        """
        Uses the model to solve for labels of the test set, updates Dataset

        Parameters
        ----------
        dataset: Dataset
            Dataset that needs label inference

        Returns
        -------
        errs_all: ndarray
            Covariance matrix of the fit
        """
        return _infer_labels(self, dataset)


    def draw_spectra(self, dataset):
        """
        Create a new dataset whose test flux and ivar values correspond to the
        fitted-for test spectra

        Parameters
        ----------
        dataset: Dataset
            Dataset that needs label inference

        Returns
        -------
        cannon_set: Dataset
            Dataset with best-fit fluxes and variances as test_flux and test_ivar
        """
        coeffs_all, covs, scatters, red_chisqs, pivots, label_vector = self.model
        nstars = len(dataset.test_SNR)
        cannon_fluxes = np.zeros(dataset.test_flux.shape)
        cannon_ivars = np.zeros(dataset.test_ivar.shape)
        for i in range(nstars):
            x = label_vector[:,i,:]
            spec_fit = np.einsum('ij, ij->i', x, coeffs_all)
            cannon_fluxes[i,:] = spec_fit
            bad = dataset.test_ivar[i,:] == SMALL
            cannon_ivars[i,:][~bad] = 1. / scatters[~bad] ** 2
        cannon_set = deepcopy(dataset)
        cannon_set.test_flux = cannon_fluxes
        cannon_set.test_ivar = cannon_ivars
        return cannon_set


    def plot_contpix(x, y, contpix_x, contpix_y, figname):
        """ Plot baseline spec with continuum pix overlaid 

        Parameters
        ----------
        """
        fig, axarr = plt.subplots(2, sharex=True)
        plt.xlabel(r"Wavelength $\lambda (\AA)$")
        plt.xlim(min(x), max(x))
        ax = axarr[0]
        ax.step(x, y, where='mid', c='k', linewidth=0.3,
                label=r'$\theta_0$' + "= the leading fit coefficient")
        ax.scatter(contpix_x, contpix_y, s=1, color='r',
                label="continuum pixels")
        ax.legend(loc='lower right', 
                prop={'family':'serif', 'size':'small'})
        ax.set_title("Baseline Spectrum with Continuum Pixels")
        ax.set_ylabel(r'$\theta_0$')
        ax = axarr[1]
        ax.step(x, y, where='mid', c='k', linewidth=0.3,
             label=r'$\theta_0$' + "= the leading fit coefficient")
        ax.scatter(contpix_x, contpix_y, s=1, color='r',
                label="continuum pixels")
        ax.set_title("Baseline Spectrum with Continuum Pixels, Zoomed")
        ax.legend(loc='upper right', prop={'family':'serif', 
            'size':'small'})
        ax.set_ylabel(r'$\theta_0$')
        ax.set_ylim(0.95, 1.05)
        print("Diagnostic plot: fitted 0th order spec w/ cont pix")
        print("Saved as %s_%s.png" % (baseline_spec_plot_name, i))
        plt.savefig(baseline_spec_plot_name + "_%s" %i)
        plt.close()


    def diagnostics_contpix(self, dataset, n=10, fig = "baseline_spec_with_cont_pix"):
        """ Call plot_contpix once for each nth of the spectrum """
        if dataset.contmask is None:
            print("No contmask set")
        else:
            coeffs_all = model.coeffs
            wl = dataset.wl
            baseline_spec = coeffs_all[:,0]
            contmask = dataset.contmask
            contpix_x = wl[contmask]
            contpix_y = baseline_spec[contmask]
            


    def diagnostics(
            self, dataset,
            leading_coeffs_plot_name = "leading_coeffs.png",
            chisq_dist_plot_name = "modelfit_chisqs.png"):
        """ Produce a set of diagnostic plots for the model 

        Parameters
        ----------
        (optional) baseline_spec_plot_name: str
            Filename of output saved plot
        (optional) leading_coeffs_plot_name: str
            Filename of output saved plot
        (optional) chisq_dist_plot_name: str
            Filename of output saved plot
        """
        label_names = dataset.get_plotting_labels()
        npixels = len(lams)
        nlabels = len(pivots)
        chisqs = model.chisqs
        coeffs = model.coeffs
        scatters = model.scatters

        # Leading coefficients for each label & scatter
        fig, axarr = plt.subplots(nlabels+1, figsize=(8,8), sharex=True)
        ax1 = axarr[0]
        plt.subplots_adjust(hspace=0.001)
        nbins = len(ax1.get_xticklabels())
        for i in range(1,nlabels+1):
            axarr[i].yaxis.set_major_locator(
                    MaxNLocator(nbins=nbins, prune='upper'))
        plt.xlabel(r"Wavelength $\lambda (\AA)$", fontsize=14)
        plt.xlim(np.ma.min(lams), np.ma.max(lams))
        plt.tick_params(axis='x', labelsize=14)
        axarr[0].set_title(
                "First-Order Fit Coeffs and Scatter from the Spectral Model",
                fontsize=14)
        ax.locator_params(axis='x', nbins=10)
        first_order = np.zeros((len(coeffs_all[:,0]), nlabels))
        for i in range(0, nlabels):
            ax = axarr[i]
            lbl = r'$%s$'%label_names[i]
            ax.set_ylabel(lbl, fontsize=14)
            ax.tick_params(axis='y', labelsize=14)
            ax.xaxis.grid(True)
            y = np.ma.array(coeffs_all[:,i+1], mask=bad)
            first_order[:, i] = y
            ax.step(lams, y, where='mid', linewidth=0.5, c='k')
            ax.locator_params(axis='y', nbins=4)
        ax = axarr[nlabels]
        ax.tick_params(axis='y', labelsize=14)
        ax.set_ylabel("scatter", fontsize=14)
        top = np.max(scatters[scatters < 0.8])
        stretch = np.std(scatters[scatters < 0.8])
        ax.set_ylim(0, top + stretch)
        ax.step(lams, scatters, where='mid', c='k', linewidth=0.7)
        ax.xaxis.grid(True)
        ax.locator_params(axis='y', nbins=4)
        print("Diagnostic plot: leading coeffs and scatters across wavelength.")
        print("Saved as %s" %leading_coeffs_plot_name)
        fig.savefig(leading_coeffs_plot_name)
        plt.close(fig)

        # triangle plot of the higher-order coefficients
        labels = [r"$%s$" % l for l in label_names]
        fig = corner(first_order, labels=labels, show_titles=True,
                     title_args = {"fontsize":12})
        filename = "leading_coeffs_triangle.png"
        print("Diagnostic plot: triangle plot of leading coefficients")
        fig.savefig(filename)
        print("Saved as %s" %filename)
        plt.close(fig)

        # Histogram of the chi squareds of ind. stars
        plt.hist(np.sum(chisqs, axis=0), color='lightblue', alpha=0.7)
        dof = len(lams) - coeffs_all.shape[1]   # for one star
        plt.axvline(x=dof, c='k', linewidth=2, label="DOF")
        plt.legend()
        plt.title("Distribution of " + r"$\chi^2$" + " of the Model Fit")
        plt.ylabel("Count")
        plt.xlabel(r"$\chi^2$" + " of Individual Star")
        print("Diagnostic plot: histogram of the red chi squareds of the fit")
        print("Saved as %s" %chisq_dist_plot_name)
        plt.savefig(chisq_dist_plot_name)
        plt.close()

    # convenient namings to match existing packages
    predict = _infer_labels
    fit = train
