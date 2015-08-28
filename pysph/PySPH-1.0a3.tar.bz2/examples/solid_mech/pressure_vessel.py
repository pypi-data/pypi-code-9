"""

Expansion of a gas inside a vessel.  The attempt here is to couple the two
simulations, fluid and structure so the explosion of the vessel can be
simulated.

"""

# Standard library imports
from __future__ import division
import numpy as np
from numpy import pi, cos, sin

# PySPH base and carray imports
from pysph.base.utils import get_particle_array
from pysph.base.kernels import CubicSpline

# PySPH solver and integrator
from pysph.solver.application import Application
from pysph.solver.solver import Solver
from pysph.sph.integrator import PECIntegrator
from pysph.sph.integrator_step import IntegratorStep

# PySPH sph imports
from pysph.sph.equation import Group

from pysph.sph.gas_dynamics.basic import IdealGasEOS,\
                                         MPMAccelerations

from pysph.sph.gas_dynamics.basic import SummationDensity as SummationDensityMPM

from pysph.sph.basic_equations import XSPHCorrectionForLeapFrog

# SPH equations
from pysph.sph.basic_equations import IsothermalEOS, ContinuityEquation, MonaghanArtificialViscosity,\
     XSPHCorrection, VelocityGradient2D
from pysph.sph.solid_mech.basic import MomentumEquationWithStress2D, HookesDeviatoricStressRate2D,\
    MonaghanArtificialStress

from pysph.sph.integrator_step import SolidMechStep

def get_K(G, nu):
    ''' Get the bulk modulus from shear modulus and Poisson ratio '''
    return 2.0*G*(1+nu)/(3*(1-2*nu))

def add_properties(pa, *props):
    for prop in props:
        pa.add_property(name=prop)


# constants
E = 1e7
nu = 0.3975
G = E/(2.0*(1+nu))
K = get_K(G, nu)
rho0_s = 1.0
c0_s = np.sqrt(K/rho0_s)
dx_s = 0.0005
hdx_s = 1.5


def create_ring():
    dx = 0.0025
    hdx = 1.5

    # geometry
    ri = 0.12
    ro = 0.13

    x,y = np.mgrid[-ro:ro:dx, -ro:ro:dx]
    x = x.ravel()
    y = y.ravel()

    d = (x*x+y*y)
    keep = np.flatnonzero((ri*ri<=d) * (d<ro*ro))
    x = x[keep]
    y = y[keep]
    d = d[keep]

    print('Ellastic explosion with %d particles'%(x.size))
    print("Shear modulus G = %g, Young's modulus = %g, Poisson's ratio =%g"%(G,E,nu))

    #print bdry, np.flatnonzero(bdry)
    m = np.ones_like(x)*dx*dx
    h = np.ones_like(x)*hdx*dx
    rho = np.ones_like(x)
    z = np.zeros_like(x)

    p = 0.5*1.0*100*100*(1 - (x**2 + y**2))

    cs = np.ones_like(x) * 10000.0

    # u is set later
    v = z

    p *= 0
    h *= 1

    # create the particle array
    pa = get_particle_array(
        name="solid", x=x, y=y, m=m, rho=rho, h=h,
        p=p, cs=cs, u=z, v=v)

    pa.cs[:] = c0_s

    # add requisite properties

    # sound speed etc.
    add_properties(pa, 'cs', 'e' )

    # velocity gradient properties
    add_properties(pa, 'v00', 'v01', 'v10', 'v11')

    # artificial stress properties
    add_properties(pa, 'r00', 'r01', 'r02', 'r11', 'r12', 'r22')

    # deviatoric stress components
    add_properties(pa, 's00', 's01', 's02', 's11', 's12', 's22')

    # deviatoric stress accelerations
    add_properties(pa, 'as00', 'as01', 'as02', 'as11', 'as12', 'as22')

    # deviatoric stress initial values
    add_properties(pa, 's000', 's010', 's020', 's110', 's120', 's220')

    # standard acceleration variables
    add_properties(pa, 'arho', 'au', 'av', 'aw', 'ax', 'ay', 'az', 'ae')

    # initial values
    add_properties(pa, 'rho0', 'u0', 'v0', 'w0', 'x0', 'y0', 'z0', 'e0')

    # load balancing properties
    pa.set_lb_props( list(pa.properties.keys()) )
    pa.set_output_arrays(list(pa.properties.keys()))
    return [pa,]


########################################

# problem constants
dim = 2
gamma = 1.4
gamma1 = gamma - 1.0

# scheme constants
cfl = 0.3

# numerical constants
dt = 1e-8
tf = 1e-4

# kernels
kernel = CubicSpline(dim=dim)
kernel_factor = 1.5

# initial values
rho0_f = 1630.0 # TNT density
e0 = 4.29e6 # sp. internal energy
p0 = gamma1 * rho0_f * e0 # pressure
vr = 0.0 # radial velocity

################################

def get_normal_particles(**kwargs):

    """ uniform distribution
    Taken from noh_cylindrical SPH2D and adapted accordingly for this.
    """
    # domain and particle spacings

    rad = 0.1 # radius of TNT
    nt, nr = 60, 20 # no. of particles in tangential & radial direction
    avg_volume = pi * rad**2 / (nt*nr)
    dx = avg_volume ** 0.5
    h0 = kernel_factor * dx

    radius = 0.1
    npnts0 = 6
    n = 20
    npnts_tot = npnts0 * ( n*(n+1)/2. )

    dr = radius/n
    h0 = dr
    rho0 = 1630.0
    m1 = pi*dr*dr*rho0/4

    x = np.zeros(0)
    y = np.zeros(0)
    m = np.zeros(0)

    rad = 0.0

    for j in range(1, n+1):
        npnts = npnts0 * j
        dtheta = 2*pi/npnts

        theta = np.arange(0, 2*pi-1e-10, dtheta)
        rad = rad + dr

        _x = rad*cos(theta)
        _y = rad*sin(theta)

        """setting varying mass for particles"""
        #_m = np.ones_like(_x) * (2.0*j - 1.0)/(j) * m1

        """setting same mass to all particles based on
        rho0, total volume and total number of particles"""
        m1 = rho0 * pi*radius**2 / npnts_tot
        _m = np.ones_like(_x) * m1

        x = np.concatenate( (x, _x) )
        y = np.concatenate( (y, _y) )
        m = np.concatenate( (m, _m) )

    """Till here. x, y, m are formed accordingly"""

    rho = np.ones_like(x) * rho0
    h = np.ones_like(x) * kernel_factor*h0

    u = np.ones_like(x) * 0.0
    v = np.ones_like(x) * 0.0

    flag = np.ones_like(x) * 0.0

    e = np.ones_like(x) * e0
    p = gamma1*rho*e

    theta = np.ones_like(x)

    "MPM specific initializations"
    alpha1 = np.ones_like(x) * 1.0
    alpha2 = np.ones_like(x) * 0.1
    # Change kernel_factor above !!!
    #h = kernel_factor *  (m/rho)**(1./dim)

    required_props = [
        'x', 'y', 'z', 'u', 'v', 'w', 'rho', 'h', 'm', 'cs', 'p', 'e',
        'au', 'av', 'aw', 'arho', 'ae', 'ah', 'x0', 'y0', 'z0',
        'u0', 'v0', 'w0', 'rho0', 'e0', 'h0', 'div', 'gid', 'pid', 'tag',
        'ax', 'ay', 'az',
        'rho_temp',
        'theta', 'h_has_converged', 'h_old', 'dhbydt', 'theta_old',
        'alpha2', 'alpha1', 'converged', 'alpha10', 'omega', 'alpha20',
        'aalpha1', 'aalpha2', 'del2e', 'dwdh', 'grhox', 'grhoy', 'am',
        ]

    fluid = get_particle_array(
                name='fluid', additional_props=required_props,
                x=x, y=y, m=m, rho=rho, h=h, h0=h.copy(), h_old=h.copy(),
                u=u, v=v, p=p, e=e, flag=flag, theta=theta,
                alpha1=alpha1, alpha2=alpha2,
                constants={'cfl':cfl, 'dt_cfl':dt},
                )

    fluid.set_output_arrays(['x','y','m','rho','h','u','v','p','cs',
                             'e','flag', 'h0'])


    print "Pressure cylinder problem with %d particles"%(fluid.get_number_of_particles())
    return [fluid]

def create_particles():
    fluid, = get_normal_particles()
    solid, = create_ring()
    return [fluid, solid]

class GasDFluidStepXSPH(IntegratorStep):
    """Predictor Corrector integrator for Gas-dynamics with XSPH"""
    def initialize(self, d_idx, d_x0, d_y0, d_z0, d_x, d_y, d_z, d_h,
                   d_u0, d_v0, d_w0, d_u, d_v, d_w, d_e, d_e0, d_h0,
                   d_converged, d_omega, d_rho, d_rho0, d_alpha1, d_alpha2,
                   d_alpha10, d_alpha20):

        d_x0[d_idx] = d_x[d_idx]
        d_y0[d_idx] = d_y[d_idx]
        d_z0[d_idx] = d_z[d_idx]

        d_u0[d_idx] = d_u[d_idx]
        d_v0[d_idx] = d_v[d_idx]
        d_w0[d_idx] = d_w[d_idx]

        d_e0[d_idx] = d_e[d_idx]

        d_h0[d_idx] = d_h[d_idx]
        d_rho0[d_idx] = d_rho[d_idx]

        # set the converged attribute to 0 at the beginning of a Group
        d_converged[d_idx] = 0

        # likewise, we set the default omega (grad-h) terms to 1 at
        # the beginning of this Group.
        d_omega[d_idx] = 1.0

        d_alpha10[d_idx] = d_alpha1[d_idx]
        d_alpha20[d_idx] = d_alpha2[d_idx]

    def stage1(self, d_idx, d_x0, d_y0, d_z0, d_x, d_y, d_z,
               d_u0, d_v0, d_w0, d_u, d_v, d_w, d_e0, d_e, d_au, d_av,
               d_aw, d_ae, d_rho, d_rho0, d_arho, d_h, d_h0, d_ah,
               d_alpha1, d_aalpha1, d_alpha10,
               d_alpha2, d_aalpha2, d_alpha20,
               d_ax, d_ay, d_az,
               dt):

        dtb2 = 0.5*dt

        d_u[d_idx] = d_u0[d_idx] + dtb2 * d_au[d_idx]
        d_v[d_idx] = d_v0[d_idx] + dtb2 * d_av[d_idx]
        d_w[d_idx] = d_w0[d_idx] + dtb2 * d_aw[d_idx]

        d_x[d_idx] = d_x0[d_idx] + dtb2 * (d_u[d_idx] + d_ax[d_idx])
        d_y[d_idx] = d_y0[d_idx] + dtb2 * (d_v[d_idx] + d_ay[d_idx])
        d_z[d_idx] = d_z0[d_idx] + dtb2 * (d_w[d_idx] + d_az[d_idx])

        # update thermal energy
        d_e[d_idx] = d_e0[d_idx] + dtb2 * d_ae[d_idx]

        # predict density and smoothing lengths for faster
        # convergence. NNPS need not be explicitly updated since it
        # will be called at the end of the predictor stage.
        d_h[d_idx] = d_h0[d_idx] + dtb2 * d_ah[d_idx]
        d_rho[d_idx] = d_rho0[d_idx] + dtb2 * d_arho[d_idx]

        # update viscosity coefficients
        d_alpha1[d_idx] = d_alpha10[d_idx] + dtb2*d_aalpha1[d_idx]
        d_alpha2[d_idx] = d_alpha20[d_idx] + dtb2*d_aalpha2[d_idx]

    def stage2(self, d_idx, d_x0, d_y0, d_z0, d_x, d_y, d_z,
               d_u0, d_v0, d_w0, d_u, d_v, d_w, d_e0, d_e, d_au, d_av,
               d_alpha1, d_aalpha1, d_alpha10,
               d_alpha2, d_aalpha2, d_alpha20,
               d_ax, d_ay, d_az,
               d_aw, d_ae, dt):

        d_u[d_idx] = d_u0[d_idx] + dt * d_au[d_idx]
        d_v[d_idx] = d_v0[d_idx] + dt * d_av[d_idx]
        d_w[d_idx] = d_w0[d_idx] + dt * d_aw[d_idx]

        d_x[d_idx] = d_x0[d_idx] + dt * (d_u[d_idx] + d_ax[d_idx])
        d_y[d_idx] = d_y0[d_idx] + dt * (d_v[d_idx] + d_ay[d_idx])
        d_z[d_idx] = d_z0[d_idx] + dt * (d_w[d_idx] + d_az[d_idx])

        # Update densities and smoothing lengths from the accelerations
        d_e[d_idx] = d_e0[d_idx] + dt * d_ae[d_idx]

        # update viscosity coefficients
        d_alpha1[d_idx] = d_alpha10[d_idx] + dt*d_aalpha1[d_idx]
        d_alpha2[d_idx] = d_alpha20[d_idx] + dt*d_aalpha2[d_idx]


app = Application()

integrator = PECIntegrator(fluid=GasDFluidStepXSPH(), solid=SolidMechStep())
wdeltap = kernel.kernel(rij=dx_s, h=hdx_s*dx_s)

solver = Solver(kernel=kernel, dim=dim, integrator=integrator, cfl=cfl,
                n_damp=100, pfreq=100, dt=dt, tf=tf,
                adaptive_timestep=False)

equations = [
    # Properties computed set from the current state
    Group(
        equations=[
            # p
            IsothermalEOS(dest='solid', sources=None, rho0=rho0_s, c0=c0_s),

            # vi,j : requires properties v00, v01, v10, v11
            VelocityGradient2D(dest='solid', sources=['solid',]),

            # rij : requires properties r00, r01, r02, r11, r12, r22,
            #                           s00, s01, s02, s11, s12, s22
            MonaghanArtificialStress(
             dest='solid', sources=None, eps=0.3),
            ],
        ),

############################# MPM
    Group(
        equations=[
            SummationDensityMPM(dest='fluid', sources=['fluid', 'solid'],
                             k=kernel_factor,
                             dim=dim, htol=1e-6,
                             density_iterations=True,)
            ], update_nnps=True, iterate=True, max_iterations=50,
        ),
#############################
    Group( equations=[
           IdealGasEOS(dest='fluid', sources=None, gamma=gamma),
                     ], ),
#############################
    Group(
        equations=[
            MPMAccelerations(
                dest='fluid', sources=['fluid',], beta=10.0,
                update_alapha1=True, update_alapha2=False,
                alpha1_min=0.1, alpha2_min=0.1, sigma=0.1),
            ], update_nnps=False
        ),

    # Acceleration variables are now computed
    Group(
        equations=[

            # arho
            ContinuityEquation(dest='solid', sources=['solid',]),

            # au, av
            MomentumEquationWithStress2D(
                dest='solid', sources=['solid',], n=4, wdeltap=wdeltap),

            # au, av
            MonaghanArtificialViscosity(
                dest='solid', sources=['solid',], alpha=1.0, beta=1.0),

            # a_s00, a_s01, a_s11
            HookesDeviatoricStressRate2D(
                dest='solid', sources=None, shear_mod=G),

            # ax, ay, az
            XSPHCorrection(
                dest='solid', sources=['solid',], eps=0.5),

            ]

        ), # End Acceleration Group

#############################
    Group( equations=[
           XSPHCorrectionForLeapFrog(dest='fluid', sources=['fluid',],
                                     eps=0.5),
                     ], ),

    ]

app.setup(solver=solver, equations=equations,
          particle_factory=create_particles)

app.run()
