# pylint: disable=E0611
from netshow.netshow import i18n_app
from tabulate import tabulate

_ = i18n_app('netshow-linux-lib')


def legend():
    """
    :return: print a legend explaining what the carrier state and bond information means
    """
    _table = []
    _table.append([_('legend') + ':', ''])
    _table.append([_('UP') + ':',
                   _('carrier up')])
    _table.append([_('UN') + ':',
                   _('carrier up, bond member not in bond')])
    _table.append([_('DN') + ':',
                   _('carrier down')])
    _table.append([_('ADMDN') + ':',
                   _('admin down use "ip link set <iface> up" to initialize')])
    _table.append([_('DRMNT') + ':',
                   _('carrier up, link dormant')])
    return '\n' + tabulate(_table) + '\n'


def one_line_legend(show_legend=False):
    """
    :return: string informing user where to find legend.
    only shown if legend option is not enabled
    """
    if not show_legend:
        return tabulate([[_('Legend: for abbrev example use -l opt in netshow cmd')]]) + \
            '\n'
    return ''


def full_legend(show_legend=False):
    """
    :return: print full legend at the bottom of the screen
    if legend option is enabled
    """
    if show_legend:
        return legend()
    else:
        return ''


def legend_wrapped_cli_output(_output, show_legend=False):
    """
    :param: _output - string from cli call before wrapping legend around it.
    :return: print cli output with legend wrapper
    """
    _pre_header = one_line_legend(show_legend)
    _footer = full_legend(show_legend)
    return _pre_header + _output + _footer
