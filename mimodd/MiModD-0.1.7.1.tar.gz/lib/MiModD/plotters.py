import itertools

from decimal import Decimal
from math import floor, log10


try:
    import rpy2.rinterface as rinterface
    import rpy2.robjects as robjects
    from rpy2.robjects.packages import importr
    RPY_EXCEPTION = None
except Exception as e:
    RPY_EXCEPTION = e


def contig_plotter (ofile, **plot_params):
    #robjects.r.postscript(ofile, paper='special', width=9, height=8)
    robjects.r.pdf(ofile, 8, 8)
    try:
        plot_func, data, current_plot_params = yield True
    except GeneratorExit:
        robjects.r["dev.off"]()
        return
    while True:
        merged_params = {k:v for k,v in plot_params.items()}
        merged_params.update(current_plot_params)
        try:
            plot_func(data, **merged_params)
        except rinterface.RRuntimeError as e:
            print (e)
            print ("There was an error creating the location plot pdf... Please try again")
        try:
            plot_func, data, current_plot_params = yield True
        except GeneratorExit:
            robjects.r["dev.off"]()
            return


def plot_scatter(data, title = '', xlab = '',
                 loess_span = None, xlim = None, ylim = None,
                 points_color = None, loess_color = None,
                 major_tick_unit = None,
                 draw_secondary_grid_lines = True,
                 no_warnings = False):    

    x_axis_scale = Decimal(10**6) # plot in Megabases

    if xlim:
        xlim = xlim / x_axis_scale
    else:
        xlim = max(d[0] for d in data) / x_axis_scale
    if major_tick_unit is None:
        major_tick_unit = x_axis_scale
        
    break_unit = major_tick_unit / x_axis_scale
    half_break_unit = break_unit / 2
    break_penta_unit = break_unit * 5

    # does the translation into R
    robjects.r('x <- c({0})'.format(','.join(str(d[0]) for d in data)))
    robjects.r('x <- x / {0}'.format(x_axis_scale))
    robjects.r('y <- c({0})'.format(','.join(str(d[1]) for d in data)))

    optional_str = ''.join(part for part in
        [
        ', col="{color}"' if points_color is not None else '',
        ', ylim=c(0,{ylim})' if ylim is not None else '',
        ])
    robjects.r(
    ('plot(x, y, cex=0.60, main="LG {title}", xlim=c(0,{xlim}), xlab="{xlab}", \
ylab="apparent rate of marker segregation", \
pch=0' + optional_str + ')'
     ).format(title=title or '?',
              xlab=xlab,
              xlim=xlim,
              ylim=ylim,
              color=points_color)
    )
    if loess_span:
        # loess line
        optional_str = ''.join(part for part in
            [
            ', col="{color}"' if points_color is not None else ''
            ])
        robjects.r(
            ('result <- try(lines(loess.smooth(x, y, span={span}), lwd=5' + optional_str + '), silent=TRUE)'
             ).format(span=loess_span, color=loess_color)
            )
        loess_failure = robjects.r('class(result)')[0] == 'try-error'
        if loess_failure and not no_warnings:
            print('Could not generate a Loess regression line for', title)
            print('R reported this problem:')
            print(robjects.r('attributes(result)$condition'))
            # TO DO: write a message to the plot
            # explaining that there is no regression line because of
            # a too small span
    # axes
    robjects.r('axis(1, at=seq(0,{xlim},by={xunits}), labels=FALSE, tcl=-0.5)'
      .format(xlim=xlim, xunits=break_unit)
      )
    robjects.r('axis(1, at=seq(0,{xlim},by={xunits}), labels=FALSE, tcl=-0.25)'
      .format(xlim=xlim, xunits=half_break_unit)
      )
    robjects.r('axis(2, at=seq(0,1,by=0.1), labels=FALSE, tcl=-0.2)')

    # optional grid lines
    if draw_secondary_grid_lines:
        robjects.r('abline(h=seq(0,1,by=0.1), v=seq(0,{xlim},by=1), col="gray")'
                   .format(xlim=xlim))



def plot_histogram(data, title = '',
                   xlab = '', ylab = '',
                   xlim = None, ylim = None,
                   major_tick_unit = None,
                   hist_colors = None
                  ):
    x_axis_scale = Decimal(10**6) # plot in Megabases
    if major_tick_unit is None:
        major_tick_unit = x_axis_scale
    if xlim:
        xlim = xlim / x_axis_scale

    break_unit = major_tick_unit / x_axis_scale
    half_break_unit = break_unit / 2
    break_penta_unit = break_unit * 5

    if hist_colors is None:
        hist_colors = ['darkgrey', 'red']
    color_cycle = itertools.cycle(hist_colors)
    
    # does the translation into R
    for n, binned_data in enumerate(data.items()):
        bin_width, data_series = binned_data
        varname = 'series' + str(n)
        robjects.r('{var} <- c({data})'
                   .format(var=varname,
                           data=','.join(str(d)
                                         for d in data_series.values())
                           )
          )
        if ylim is None:
            # use the maximum value observed in the data for this plot
            max_observed_y = max(value for series in data.values()
                                       for value in series.values())
            ylim = pretty_round(max_observed_y)

        bin_width = Decimal(bin_width) / x_axis_scale
        if not xlim:
            xlim = bin_width * len(data_series)
        if n == 0:
            # first fresh plot
            robjects.r('barplot({var}, main="LG {title}", \
xlim=c(0,{xlim}), ylim=c(0,{ylim}), width={width}, space=0, \
col="{color}", xlab="{xlab}", ylab="{ylab}")'
                       .format(var=varname,
                               ylim=ylim,
                               xlim=xlim,
                               width=bin_width,
                               xlab=xlab,
                               ylab=ylab,
                               title=title or '?',
                               color=next(color_cycle))
                )
            # axes
            robjects.r('axis(1, hadj=1, at=seq(0,{xlim},by={width}), labels=FALSE, tcl=-0.5)'
              .format(xlim=xlim, width=break_unit)
              )
            robjects.r('axis(1, at=seq(0,{xlim},by={width}), labels=TRUE, tcl=-0.5)'
              .format(xlim=xlim, width=break_penta_unit)
              )
            robjects.r('axis(1, at=seq(0,{xlim},by={width}), labels=FALSE, tcl=-0.25)'
              .format(xlim=xlim, width=half_break_unit)
              )
        else:
            # additional histograms are just added to the first plot
            robjects.r(
                ('barplot({var}, \
add=TRUE, space=0, col="{color}", width={width})'
                 ).format(var=varname,
                          width=bin_width,
                          color=next(color_cycle))
              )


def pretty_round(max_observed_y, scale = 1.1):
    scale = type(max_observed_y)(scale)
    if max_observed_y < 10:
        return int(scale*max_observed_y) or 1
    max_observed_y = int(scale*int(max_observed_y))
    return int(round(max_observed_y, 1-floor(log10(max_observed_y)) or -1))
