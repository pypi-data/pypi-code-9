from datetime import date as date
from datetime import timedelta
import urwid
from calendarwidget import CalendarWidget

PALETTE = [('header', 'white', 'black'),
           ('footer', 'white', 'black'),
           ('line header', 'black', 'white', 'bold'),
           ('bright', 'dark blue', 'white', ('bold', 'standout')),
           ('list', 'black', 'white'),
           ('list focused', 'white', 'light blue', 'bold'),
           ('edit', 'black', 'white'),
           ('edit focused', 'white', 'light blue', 'bold'),
           ('button', 'black', 'dark cyan'),
           ('button focused', 'white', 'light blue', 'bold'),
           ('reveal focus', 'black', 'dark cyan', 'standout'),
           ('today focus', 'white', 'dark cyan', 'standout'),
           ('today', 'black', 'light gray', 'dark cyan'),
           ('edit', 'white', 'dark blue'),
           ('alert', 'white', 'dark red'),

           ('editfc', 'white', 'dark blue', 'bold'),
           ('editbx', 'light gray', 'dark blue'),
           ('editcp', 'black', 'light gray', 'standout'),
           ('popupbg', 'white', 'black', 'bold'),

           ('black', 'black', ''),
           ('dark red', 'dark red', ''),
           ('dark green', 'dark green', ''),
           ('brown', 'brown', ''),
           ('dark blue', 'dark blue', ''),
           ('dark magenta', 'dark magenta', ''),
           ('dark cyan', 'dark cyan', ''),
           ('light gray', 'light gray', ''),
           ('dark gray', 'dark gray', ''),
           ('light red', 'light red', ''),
           ('light green', 'light green', ''),
           ('yellow', 'yellow', ''),
           ('light blue', 'light blue', ''),
           ('light magenta', 'light magenta', ''),
           ('light cyan', 'light cyan', ''),
           ('white', 'white', ''),
           ]

on_press = {}

keybindings = {
    'today': ['T'],
    'left': ['left', 'h'],
    'up': ['up', 'k'],
    'right': ['right', 'l'],
    'down': ['down', 'j'],
}

frame = CalendarWidget(on_date_change=lambda _: None,
                       keybindings=keybindings,
                       on_press=on_press,
                       firstweekday=5,
                       weeknumbers='right')

loop = urwid.MainLoop(frame, PALETTE)
today = date.today()
for diff in range(-200, 200, 1):
    day = today + timedelta(days=diff)
    frame.set_focus_date(day)
    assert frame.focus_date == day
loop.run()
