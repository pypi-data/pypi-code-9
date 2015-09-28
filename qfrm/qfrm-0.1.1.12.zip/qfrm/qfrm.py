
class Util():
    """ A collection of utility functions, most of which are static methods, i.e. can be called as Util.isiterable().

    FYI: Decorator @staticmethod allows use of functions without initializing an object
    Ex. we can use Util.demote(x) instead of Util().demote(x). It's faster.

    .. sectionauthor:: Oleg Melnikov
    """
    @staticmethod
    def is_iterable(x):
        """
        Checks if x is iterable.
        :param x: any object
        :type x: object
        :return: True if x is iterable, False otherwise
        :rtype: bool
        :Exmaple:

        >>> Util.is_iterable(1)
        False

        >>> Util.is_iterable((1,2,3))
        True

        >>> Util.is_iterable([1,'blah',3])
        True
        """
        try:
            (a for a in x)
            return True
        except TypeError:
            return False

    @staticmethod
    def is_number(x):
        """
        Checks if x is numeric (float, int, complex, ...)
        :param x: any object
        :type x: object
        :return:  True, if x is numeric; False otherwise.
        :rtype: bool
        ..seealso:: Stackoverflow: how-can-i-check-if-my-python-object-is-a-number
        """
        from numbers import Number
        return isinstance(x, Number)

    @staticmethod
    def are_numbers(x):
        """ Checks if x is an iterable of numbers.
        :param x: any object
        :type x: object
        :return: True if x is iterable, False otherwise
        :rtype: bool

        :Example:

        >>> Util.arenumbers(5)
        False

        >>> Util.arenumbers([1,'blah',3.])
        False

        >>> Util.arenumbers([1,'2',3.])
        False

        >>> Util.arenumbers((1, 2., 3. + 4j, 5.4321))
        True

        >>> Util.arenumbers({1, 2., 3. + 4j, 5.4321})
        True

        """
        try:
            return all(Util.is_number(n) for n in x)
        except TypeError:
            return False

    @staticmethod
    def are_bins(x):
        return Util.are_non_negative(x) and Util.is_monotonic(x)

    @staticmethod
    def to_tuple(x):
        """ Converts an iterable (of numbers) or a number to a tuple of floats.

        :param x: any iterable object of numbers or a number
        :type x:  numeric|iterable
        :return:  tuple of floats
        :rtype: tuple
        """
        assert Util.is_number(x) or Util.is_iterable(x), 'to_tuple() failed: input must be iterable or a number.'
        return (float(x),) if Util.is_number(x) else tuple((float(y)) for y in x)

    @staticmethod
    def round_tuple(t, ndigits=5):
        """ Rounds tuple of numbers to ndigits.
        returns a tuple of rounded floats. Used for printing output.
        :param t: tuple
        :type t:
        :param ndigits: number of decimal (incl. period) to keep
        :type ndigits: int
        :return: tuple of rounded numbers
        :rtype: Tuple[float,...,float]
        """
        return tuple(round(float(x), ndigits) for x in t)

    @staticmethod
    def cpn2cf(cpn=6, freq=2, ttm=2.1):
        """ Converts regular coupon payment specification to a series of cash flows indexed by time to cash flow (ttcf).

        :param cpn:     annual coupon payment in $
        :type cpn:      float|int
        :param freq:    payment frequency, per anum
        :type freq:     float|int
        :param ttm:     time to maturity of a bond, in years
        :type ttm:      float|int
        :return:        dictionary of cash flows (tuple) and their respective times to cf (tuple)
        :rtype:         dict('ttcf'=tuple, 'cf'=tuple)
        .. seealso:: stackoverflow.com/questions/114214/class-method-differences-in-python-bound-unbound-and-static
        :Example:

        >>> # convert $6 semiannula (SA) coupon bond payments to indexed cash flows
        >>> Util.cpn2cf(6,2,2.1)  # returns {'cf': (3.0, 3.0, 3.0, 3.0, 103.0),  'ttcf': (0.1, 0.6, 1.1, 1.6, 2.1)}
        """
        from numpy import arange

        if cpn == 0: freq = 1  # set frequency to annual for zero coupon instruments
        period = 1./freq            # time (in year units) period between coupon payments
        end = ttm + period / 2.          # small offset (anything less than a period) to assure expiry is included
        start = period if (ttm % period) == 0 else ttm % period  # time length from now till next cpn, yrs
        c = float(cpn)/freq   # coupon payment per period, $

        ttcf = tuple((float(x) for x in arange(start, end, period)))        # times to cash flows (tuple of floats)
        cf = tuple(map(lambda i: c if i < (len(ttcf) - 1) else c + 100, range(len(ttcf)))) # cash flows (tuple of floats)
        return {'ttcf': ttcf, 'cf': cf}

    @staticmethod
    def demote(x):
        """ Attempts to convert iterable object x to tuple or return just the value of a singleton x.
        Basically, demotes to a simpler object, if possible.

        :param x:   any object
        :type x:    any
        :return:    original object or tuple or value of a singleton
        """

        if Util.is_iterable(x):
            x = tuple(e for e in x)
            if len(x) == 1: x = x[0]
        return x

    @staticmethod
    def is_monotonic(x, direction=1, strict=True):
        # http://stackoverflow.com/questions/4983258/python-how-to-check-list-monotonicity
        assert direction in (1,-1), 'Direction must be 1 for up, -1 for down'

        x = Util.to_tuple(x)[::direction]
        y = (x + (max(x) + 1,))
        return all(a < b if strict else a <= b for a, b in zip(y, y[1:]))

    @staticmethod
    def are_same_sign(x, sign=1, ignore_zero=True):
        assert sign in (1,-1), 'sign must be 1 (for positive) or -1 (for negatives)'
        return all(a*sign >= 0 if ignore_zero else a*sign >0 for a in Util.to_tuple(x))

    @staticmethod
    def are_positive(x):
        return Util.are_same_sign(x, 1, False)

    @staticmethod
    def are_non_negative(x):
        return Util.are_same_sign(x, 1, True)


class PVCF():
    """ Present value of cash flows model (aka NPV, TVM, IRR, ...)

    PVCF class allows computing NPV and IRR via discounted cash flows model.

    These are meant to be read-only. Don't set these directly to avoid nonsense :)
    :cvar cf: individual cash flows ($ or some currency), tuple of numbers
    :cvar ttcf: times to cash flows (year units), tuple of numbers
    :cvar z: zero yields (rates or decimals), tuple of floats. I.e. yields at times corresponding to ttcf.
    :cvar desc: any user-defined bond descriptors (ratings, ticker, isin, cusip, issuer, issue date,...)

    .. sectionauthor:: Oleg Melnikov
    .. warning::
    Class-scope variables are read-only. Use __init__() or set_pyz() to set them.
    """
    cf = ();    ttcf = ();    z = ();    desc = {}

    def __init__(self, cf=(3,3,3,103), ttcf=(.5,1.,1.5,2.), pyz:'optional'=(.05,.058,.064,.068), \
                 ttz:'optional'=None, desc={'note':'Hull, p.83'}):
        """
        Initializes an object with cash flows and a relevant yield curve.

        :param cf:      cash flow payments, in $ of $100 par
        :type cf:       tuple[float,...,float]
        :param ttcf:    time remaining to each payment, in years
        :type ttcf:     tuple[float,...,float]
        :param pyz:     Dollar price (if >1), return rate (if <=1), or zero rate curve (if tuple of floats).
        :type pyz:      tuple[float,...,float]
        :param ttz:     times to zero rates. If left None, ttcf times are assumed for pyz rates.
        :type ttz:      None or tuple[float,...,float]
        :param desc:    any information use may want to save with this object
        :type desc:     dict

        ..seealso:: set_pyz() method
        """

        assert Util.is_number(cf) or Util.is_iterable(cf), 'cf must be a number or a tuple'
        assert Util.is_number(ttcf) or Util.is_iterable(ttcf), 'cf must be a number or a tuple'

        self.ttcf, self.cf, self.desc = Util.to_tuple(ttcf), Util.to_tuple(cf), desc
        self.set_pyz(pyz, ttz)  # yc, tty are tuples in the form accepted by set_pyz() method

    def tvm(self, t=0):
        """ Computes time value of money (TVM) for specified time(s) t, (usually) in a time interval [0,ttm].
        This function is vectorized over t, i.e. a tuple of times can be passed; tvm for each is generated as a tuple of floats.

        :param t:   time(s) in years at which to compute monetary value of cash flows
        :type t:    scalar (float, int, ...) or any iterable (i.e. tuple, list, Series,...)
        :return:    time value of money at time t (in years)
        :rtype:     float for numeric t; tuple for iterable t

        :Example:

        >>> Bond().tvm(1)
        105.21029388626387

        >>> Bond().tvm((0.5,1,1.5,2))
        (101.74030821388631, 105.21029388626387, 108.79895205021664, 112.51034995570011)

        """

        # Vectorize your computation. Ex. implicit vectorization (lecture slides for ch.4), list comprehension, ...
        from numpy import exp
        assert self.z is not None, 'Set zero curve (even if flat at ytm level) before computing price. '

        # vectorization with np.ndarray and with list comprehension. t1 is a scalar here.
        tvm1 = lambda t1: float(sum(1/exp(self.z) ** [ttcf1 - t1 for ttcf1 in self.ttcf] * self.cf))

        return tvm1(t) if Util.is_number(t) else tuple([tvm1(t1) for t1 in t]) # tuple([tvm1(t1) for t1 in Util.to_tuple(t)])

    def IRR(self, npv_target=100):
        """  Internal Rate of Return (same as Yield to Maturity for a bond). See p.83.
        This function is vectorized over npv_target.

        :param npv_target:  target price for which to compute
        :type npv_target:   float or tuple
        :return:            internal rate of return for each of input npv
        :rtype:             float for numeric argument, tuple for iterable argument
        .. seealso::
            docs.scipy.org/doc/scipy/reference/tutorial/optimize.html#sets-of-equations
            docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root.html#scipy.optimize.root

        :Example:

        >>> PVCF().IRR(99)
        0.06436839861575007

        >>> PVCF().IRR((99,100,101))
        (0.06436839861575007, 0.059117604483088844, 0.053920381838347846)

        """
        from scipy.optimize import root
        from numpy import exp

        def IRR1(npv1):
            npv_diff = lambda r: sum(self.cf * (1/exp(r))**self.ttcf) - npv1
            return float(root(npv_diff, x0=0).x)
        return IRR1(npv_target) if Util.is_number(npv_target) else tuple([IRR1(v) for v in npv_target])

    def set_pyz(self, pyz=(.05,.058,.064,.068), ttz:'optional'=(.5,1.,1.5,2.)):
        """         Sets a zero rate (yield) curve for discounting cash flows.

        A float pyz implies a flat curve. If pyz is a price (pyz > 1), then irr is computed and saved as flat curve.
        Any right excess rates are truncated. Right-extrapolated, if needed.
        If ttz is omitted, ttcf are assumed. If ttz is supplied, z rates are interpolated at ttcf and input info is discarded.
            pyz=(.05,.058,.064,.068) - a full yield curve
            pyz=.05 - for flat curve
            pyz=98.35 - for a PVCF

        :param pyz:     pvcf, ytm rate or tuple of zero rates
        :type pyz:      float or tuple
        :param ttz:     times of zero rates
        :type ttz:      None or tuple (the size of pyz tuple)
        :return:        self
        :rtype:         self
        .. seealso::
            interp          docs.scipy.org/doc/numpy/reference/generated/numpy.interp.html
        """
        from numpy import interp

        assert ttz is None or Util.is_number(ttz) or Util.is_iterable(ttz), \
            'Times to yields (tty_new) must be a number, tuple, or None (to use ttcf)'
        ttz = Util.to_tuple(self.ttcf if ttz is None else ttz) # we still need to assure len(ttm) = len(yld)

        assert pyz is None or Util.is_number(pyz) or Util.is_iterable(pyz), \
            'pyz must be None, numeric (px or ytm) or tuple of zero yields'

        if pyz is not None:
            if Util.is_number(pyz):
                if pyz > 1:
                    pyz = self.IRR(pyz)  # for price input, compute ytm. A flat zero curve will be set to it.
            z = Util.to_tuple(pyz)

            min_len = (min(len(ttz), len(z)))
            z, t = z[0:min_len], ttz[0:min_len]
            self.z = Util.to_tuple(interp(self.ttcf, t, z, left=z[0], right=z[len(z) - 1]))
        return self

    def plot_cf(self, ax=None):
        """ Either plots cash flow diagram on new subplot or on subplot argument
        Positive CF are in green. Negative: in red.

        :param ax:  plot axis object
        :type ax:   matplotlib.axes._subplots.AxesSubplot
        :return:    prints plot

        .. seealso:: Stackoverflow: pyplot-bar-chart-of-positive-and-negative-values
        """
        import matplotlib.pyplot as plt
        from pandas import Series, DataFrame

        if min(self.ttcf) > 0: t, c, z = (0,) + self.ttcf, (-self.tvm(),) + self.cf, (min(self.z),) + self.z

        pos = DataFrame({'Positive cf':Series([x*(x>=0) for x in c], t)})
        neg = DataFrame({'Negative cf':Series([x*(x<=0) for x in c], t)})

        if ax == None: fig, ax = plt.subplots(nrows=1, ncols=1)
        pos.plot(ax=ax, grid=1, kind='bar', color=['green'], title='CF diagram', align='center', width=.5)
        neg.plot(ax=ax, grid=1, kind='bar', color=['red'], align='center', width=.5)

        ax.set_xlabel('Time to maturity (ttm), years')
        ax.set_ylabel('Cash flow, $')
        plt.tight_layout()

    dirty_px = npv = tvm   # These are the same. Conceptually, TVM is more general. See Net present value @ Wikipedia


class Bond(PVCF):
    """ Derived (parent or super) class Bond inherits from a child (sub) class PVCF

    .. sectionauthor:: Oleg Melnikov
    .. warning::
    Class-scope variables are read-only. Use __init__() or PVCF.set_pyz() to set them.
    """

    def __init__(self, cpn=6, freq=2, ttm=2, pyz=(.05,.058,.064,.068), ttz:'optional'=None, desc={}):
        """ Initializes a new Bond object with coupon, frequency, ttm and optional zero curve parameters (see PVCF.set_z).

        :param cpn:     annual (periodic) coupon payment, in $ of $100 par
        :type cpn:      numeric (i.e. int or float)
        :param freq:    number of payments per year
        :type freq:     numeric
        :param ttm:     time to maturity, years
        :type ttm:      numeric
        :param pyz, ttz:    see PVCF.set_z
        :param desc:    dictionary of any meta information user wants to store with this object.
        :Example:

        See analytics() method for lots of examples.
        """
        assert cpn >= 0 if Util.is_number(cpn) else 0, 'Annual coupon payment (cpn,$) must be a number >=0'

        if cpn == 0:  freq = 1  # set freq of a zero bond to 1
        assert freq >= 0 if Util.is_number(freq) else 0, 'Payment frequency (times per anum) must be a number >=0'
        assert ttm >= 0 if Util.is_number(ttm) else 0, 'Time to maturity (ttm, yrs) must be a number >0'

        c = Util.cpn2cf(cpn=cpn, freq=freq, ttm=ttm)
        self.cpn, self.freq, self.ttm = cpn, freq, ttm
        PVCF.__init__(self, cf=c['cf'], ttcf=c['ttcf'], pyz=pyz, ttz=ttz, desc=desc)  # initialize subclass

    def analytics(self, iter=1):
        """ Run all bond analytics and print these on screen. Plot diagrams. Time the execution.

        :param iter: number of iterations to draw from
        :type iter: int

        :Example:

        >>> # textbook example (default) of 6% SA bond with 2 years/time to maturity (TTM), see p.83 in Hull's OFOD/9ed
        >>> Bond().analytics()
        >>> # 3% annually-paying bond with 3.1 TTM (in years), evaluated at 5% continuously compounded (CC) yield-to-maturity (YTM),
        >>> # i.e. flat yield curve (YC)
        >>> Bond(3,1,3.1, pyz=.05).analytics()
        >>> # 4% semi-annually (SA) bond with 4.25 ttm (4 years and 3 mo), evaluated at $97.5 PVCF (which computes to 4.86% ytm or flat YC)
        >>> b = Bond(4,2,4.25, pyz=97.5)
        >>> b.ytm()
        >>> b.analytics()
        >>> # The same 4% SA bond evaluated with a specific YC.
        >>> # Zero rates are assumed to have TTM matching those of cash flows (CF), left to right.
        >>> # Insufficient rates are extrapolated with a constant.
        >>> b.set_pyz(pyz=(.05,.06,.07,.08)).analytics()
        >>> # The same 4% SA bond evaluated with a specific YC. User provides zero rates with corresponding TTM.
        >>> # TTM required to evaluate CF are extra/inter-polated from existing curve with constant rates on each side.
        >>> b.set_pyz(pyz=(.05,.06,.04,.03), ttz=(.5,1,2,6)).analytics()

        >>> Bond(desc={'Default bond specs'}).analytics()
        >>> Bond(0,1,0.25, pyz=97.5, desc={'Zero coupon bond from Hull p.83'}).analytics(iter=100)
        >>> Bond(6,2,2, pyz=(.05,.058,.064,.068), desc={'Analyze with a zero curve, Hull p.83'}).analytics(iter=100)
        >>> Bond(6,2,2, pyz=98.38506277293962, desc={'Analyze with a dollar price, Hull p.83'}).analytics(iter=100)
        >>> Bond(6,2,2, pyz=0.06762438716028712, desc={'Analyze with a ytm (flat zero curve), Hull p.83'}).analytics(iter=100)
        >>> Bond(10,2,3, pyz=.12, desc={'Analyze with a ytm (flat zero curve), Hull p.93'}).analytics(iter=100)
        >>> Bond(10,2,3.1, pyz=.12, desc={'Bond in mid-coupon payment period'}).analytics(iter=100)
        >>> Bond(15,2,7.7, pyz=.12, desc={'Px convergence to par, assuming zero curve never changes.'}).analytics()
        >>> Bond(8,2,1.5, pyz=.08, desc={'Problem 4.3.'}).analytics()
        >>> Bond(5,2,1, pyz=.1).analytics()

        """
        from time import clock
        from statistics import median

        def run_analytics(timeit=False):
            out = '------------------ Bond analytics: ------------------------\n' \
            + '* Annual coupon, $: ' + str(self.cpn) + '\n'\
            + '* Coupon frequency, p.a.: ' + str(self.freq) + '\n'\
            + '  Time to maturity (ttm), yrs: ' + str(self.ttm) + '\n'\
            + '* Cash flows, $ p.a.: ' + str(self.cf) + '\n'\
            + '  Time to cash flows (ttcf), yrs: ' + str(self.ttcf) + '\n'\
            + '  Dirty price (PVCF), $: ' + str(round(self.pvcf(), 5)) + '\n'\
            + '* Clean price (PVCF - AI), $: ' + str(round(self.clean_px(), 5)) + '\n'\
            + '  YTM, CC rate: ' + str(round(self.ytm(), 5)) + '\n'\
            + '  YTM, rate at coupon frequency: ' + str(round(self.convert_rate(self.ytm(),0,self.freq), 5)) + '\n'\
            + '  Current yield, rate at coupon frequency: ' + str(round(self.cur_yld(), 5)) + '\n'\
            + '* Par yield, rate at coupon frequency: ' + str(round(self.par_yld(), 5)) + '\n'\
            + '  Yield curve, CC rate: ' + str(Util.round_tuple(self.z)) + '\n'\
            + '  Macaulay duration, yrs: ' + str(round(self.mac_dur(), 5)) + '\n'\
            + '  Modified duration, yrs: ' + str(round(self.mod_dur(), 5)) + '\n'\
            + '  Effective duration, yrs: ' + str(round(self.eff_dur(), 5)) + '\n'\
            + '* Convexity, yrs^2: ' + str(round(self.convexity(), 5)) + '\n'\
            + '  Desc: ' + str(self.desc) + '\n'\
            + '------------------------------------------------------------------------------'
            return clock() if timeit else out

        t = tuple((-(clock() - run_analytics(1)) for i in range(iter)))
        print(run_analytics())
        print('Median run time (microsec) for ' + str(iter) + ' iteration(s): ' + str(median(t) * 10**6))
        self.plot()

    @staticmethod
    def convert_rate(r=.05, from_freq=2, to_freq=0):
        """ Converts return rate from finite frequency or continued to finite frequency or continued.

        Function is vectorized over r, i.e. it will produce a tuple of converted rates, if r is a tuple of rates.

        :param r:       interest rate to convert (all rates here are fractions, i.e. in decimal)
        :type r:        float or tuple[float,...,float]
        :param from_freq:   initial frequency. 0 represents continued compounding
        :type from_freq:    int
        :param to_freq:     ending frequency. 0 represents cc.
        :type to_freq:      int
        :return:            new interest rate
        :rtype:             float if r is numeric; tuple if r is iterable of floats
        """
        from math import exp, log
        m, n = from_freq, to_freq

        def cr_helper(r=.05):
            if m == 0 and n > 0:
                r_out = n * (exp(r / n) - 1)
            elif n == 0 and m > 0:
                r_out = m * log(1 + r / m)
            elif n > 0 and m > 0:
                r_out = (((1 + r/m) ** m/n) - 1) * n
            else:
                r_out = r
            return r_out

        return Util.demote(cr_helper(r1) for r1 in Util.to_tuple(r))

        # return r_out if Util.isnumber(r_out) else r_
        # if Util.isnumber(r): r_new = cr_helper(r,)

    def pvcf(self, ttm=None):
        """ Computes present value of cash flows. See p. 83.
        Check if zero curve is set already. It's required for computation. Function is vectorized for ttm.

        :param ttm: time to maturity in yrs. If None, current is used. Otherwise, compute pvcf for bond
                    with the same cpn/freq/ytm, but user-defined ttm.
        :type ttm:  None, numeric, or tuple
        :return:    pvcf for present bond or for provided tuple of ttm values.
        :rtype:     float ttm=None|numeric; tuple for ttm=iterable

        :Example:

        >>> Bond(6,2,2).pvcf()
        98.38506277293972

        >>> y = Bond(6,2,2).ytm()     # fix yield curve at flat rate, ytm
        >>> y
        0.06762438716028674

        >>> Bond(6,2,2,pyz=y).pvcf(ttm=.75)
        100.85598835020366

        >>> Bond(6,2,.75,pyz=y).pvcf()
        100.85598835020365

        >>> Bond().pvcf(1)
        99.16523950122058

        >>> Bond().pvcf((0.5,1,1.5,2))
        (99.5755641519043, 99.16523950122058, 98.76855689367433, 98.38506277293972)

        """
        assert self.z is not None, 'Set zero curve (even if flat at ytm level) before computing price. '

        if ttm is None: ttm = self.ttm
        ytm_fixed = self.IRR(self.tvm())
        ttm = Util.to_tuple(ttm)
        p = Util.demote(Bond(self.cpn, self.freq, t0, ytm_fixed).tvm() for t0 in ttm)
        return p

    def clean_px(self, ttm=None):
        """ Computes clean bond price as pvcf - accrued interest (ai).
        See pvcf, which has similar definition. Vectorized for ttm. Returns float or tuple of clean price(s).

        :param ttm:
        :type ttm:
        :return:
        :rtype:
        .. seealso::
            default rate assumes flat yield curve to the left of the shortest rate
            www.riskencyclopedia.com/articles/bond-accrued-interest/
        """
        if ttm is None: ttm = self.ttm
        ttm = Util.to_tuple(ttm)

        def cp_helper(ttm1):
            prd = 1/self.freq                                 # a period between coupon payments (in years)
            tt_next_cpn = ttm1 % prd        # time to next coupon
            # tt_next_cpn = (self.ttm - array(t)) % prd        # time to next coupon
            tt_last_cpn = prd - tt_next_cpn                   # time to (from) last coupon
            ai = self.cpn / self.freq * tt_last_cpn / prd     # accrued interest or artificial intelligence (whichever :))
            return self.pvcf(ttm1) - ai                         # dirty price adjusted for ai

        # return px if Util.isnumber(px) else tuple(px)    # return a float or a tuple of floats
        return Util.demote(cp_helper(ttm1) for ttm1 in ttm)

    def ytm(self, px_target=None, out_freq=0):
        """ Compute yield to maturity. Vectorized for px_target, but not for out_freq.
        Returns float for input float px_target; tuple of floats for vector of px_target.
        If px_target=None, then pvcf() is used instead.

        :param px_target: Price that results in sought yield to maturity (YTM), via optimization. In $ of $100 par.
        :type px_target:  float|tuple[float,...,float]
        :param out_freq:    compounding frequency of the returned rate.
            0 - continuousely compounded (CC)
            1 - once a year or annual
            2 - twice a year, or semiannual, etc.
        :type out_freq:  numeric (int, float,...)
        :return: ytm corresponding to the target price.
        :rtype: float|tuple[float,...,float]
        :Example:

        >>> Bond().ytm(98.385)      # computes continuousely compounded (CC) yield to maturity (YTM) for PVCF=98.385
        0.0676247205968211

        >>> Bond().ytm((97,98.385,99))
        (0.07503517851147629, 0.0676247205968211, 0.06436839861575007)

        >>> Bond().ytm()   # uses default price, i.e. pvcf(), assuming yield curve was provided; output is CC rate
        0.06762438716028674

        >>> Bond().ytm(out_freq=4)  # use default PVCF to compute YTM with quarterly compounding
        0.06819925439547614

        >>> Bond().ytm(out_freq=Bond().freq) # use default PVCF to compute YTM with compounding frequency of the bond's coupon
        0.06878064668298833
        """
        if px_target is None: px_target = self.pvcf()
        return self.convert_rate(self.IRR(px_target), from_freq=0, to_freq=out_freq)

    def par_yld(self):
        """ Compute par yield rate. Par yield is an annual coupon rate (in decimal) that makes PVCF=$100.

        :return:    par yield rate (in decimal) for this bond object.
        :rtype:     float

        .. seealso::
        John C. Hull, OFOD, p.83.
        """
        from numpy import exp
        d = 1 / exp(self.z[len(self.z) - 1]) ** self.ttm
        A = sum((1/exp(self.z))** self.ttcf)
        return (1 - d) * self.freq / A

    def cur_yld(self):
        """  Compute current yield rate, i.e annual coupon of $100 par/ clean price of $100 par.

        :return: current yield rate
        :rtype: float

        .. seealso:: https://en.wikipedia.org/wiki/Current_yield
        """
        return self.cpn / self.clean_px()

    def mac_dur(self):
        """ Computes Macaulay duration, ranging from 0 to ttm.

        :return: Macaulay duration, in years
        :rtype:  float
        """
        from numpy import exp
        return sum(1/exp(self.z) ** self.ttcf * self.ttcf * self.cf) / self.pvcf()

    def mod_dur(self):
        """ Computes modified duration.

        :return: modified duration, in years
        :rtype: float
        """

        y = self.convert_rate(self.ytm(), 0, self.freq)
        return self.mac_dur() / (1 + y / self.freq)

    def eff_dur(self, dz=.01):
        """ Computes effective duration, as price changes resulting from +/- deviation (dz) in ytm.
        Default deviation, dz, is 1%.

        :param dz:  assumed change in yield, in decimal. I.e. this is a shock (up/down shift) to flat interest rate curve.
        :type dz:   float
        :return:    effective duration, in years
        :rtype:     float

        .. seealso::
        http://www.investopedia.com/exam-guide/cfa-level-1/fixed-income-investments/effective-modified-macaulay-duration.asp
        """
        u = Bond(cpn=self.cpn, freq=self.freq, ttm=self.ttm, pyz=self.ytm())
        d = Bond(cpn=self.cpn, freq=self.freq, ttm=self.ttm, pyz=self.ytm())
        u.set_pyz(u.ytm() - dz)
        d.set_pyz(d.ytm() + dz)
        return (u.pvcf() - d.pvcf()) / (2 * self.pvcf() * dz) # (px_up - px_dn) / (2 * self.clean_px() * dz)

    def convexity(self):
        """ Compute convexity of this bond.

        :return:    this bond's convexity, in years
        :rtype:     float
        """
        from numpy import exp
        return sum(1/exp(self.z) ** self.ttcf * self.ttcf * self.ttcf * self.cf) / self.pvcf()

    def plot(self):
        """  Produce a plot like the one sampled in the HW.
        :return:    nothing
        """
        from numpy import linspace, array
        from pandas import DataFrame, Series
        import matplotlib.pyplot as plt

        t = linspace(self.ttm, self.ttm/1000, 1000)
        b = DataFrame({'dirty_px': Series(self.pvcf(ttm=t), t), 'clean_px': Series(self.clean_px(ttm=t), t)})

        axcf = plt.subplot2grid((2,2), (0, 0), colspan=1)
        axp = plt.subplot2grid((2,2), (1, 0))
        axpy = plt.subplot2grid((2,2), (0, 1), rowspan=2)

        self.plot_cf(axcf)  # draw cash flos in top-left plot

        # bottom left: dirty/clean price convergence
        b.plot(ax=axp, grid=1, title='Price converges to par, as time -> epxiry.', style=['r','g'])
        axp.set_xlabel('Time to maturity (ttm), years')
        axp.set_ylabel('Price, $')

        # right: price-yield relationship
        b = self.pvcf()
        B = linspace(b * 2, b * .5, 100)
        Y = array(self.ytm(px_target=B))
        dY = Y - self.ytm()

        d = DataFrame({'PVCF':Series(B, Y)})
        d['Slope with Macaulay duration'] = Series(b * (1 - self.mac_dur() * dY), Y)
        d['Slope with Macaulay duration and convexity adjustment'] = \
            Series(b * (1 + dY * (dY * self.convexity() *.5 - self.mac_dur())), Y)
            # Series(b * (1 - (Y - y) * (self.mac_dur() - (Y - y) * self.convexity() / 2)), Y)
        d['Slope with modified duration'] = Series(b * (1 - self.mod_dur() * dY), Y)
        d['Slope with effective duration'] = Series(b * (1 - self.eff_dur() * dY), Y)
        d.plot(ax=axpy, grid=1, style=['r-','g--','r--','k--','y--'], title='Price-yield-duration relationship')

        plt.plot(self.ytm(), self.pvcf(),marker='o', color='r', ls='')  # (98.38506277293962, 0.06762438716028712)
        axpy.set_xlabel('Yield to maturity (ytm), rate')
        axpy.set_ylabel('PVCF, $')

        plt.tight_layout()
        plt.show()

    quoted_px = clean_px



