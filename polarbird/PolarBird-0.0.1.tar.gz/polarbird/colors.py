def get_color_seq(code):
    color_seq = '\001\033[38;5;{code}m\002'

    return color_seq.format(code=code)

colors = {
    'black': get_color_seq(0),
    'red': get_color_seq(1),
    'green': get_color_seq(2),
    'yellow': get_color_seq(3),
    'blue': get_color_seq(4),
    'magenta': get_color_seq(5),
    'cyan': get_color_seq(6),
    'white': get_color_seq(7),
    'light_black': get_color_seq(8),
    'light_red': get_color_seq(9),
    'light_green': get_color_seq(10),
    'light_yellow': get_color_seq(11),
    'light_blue': get_color_seq(12),
    'light_magenta': get_color_seq(13),
    'light_cyan': get_color_seq(14),
    'light_white': get_color_seq(15),
}
