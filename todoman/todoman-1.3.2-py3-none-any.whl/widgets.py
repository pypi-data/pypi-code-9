# Copyright (c) 2015 Hugo Osvaldo Barrera
# Copyright (c) 2013-2015 Christian Geier et al.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import urwid


class CPile(urwid.Pile):

    def keypress(self, size, key):
        return urwid.Pile.keypress(self, size, key)


class Choice(urwid.PopUpLauncher):

    def __init__(self, choices, active, decorate_func=None):
        self.choices = choices
        self._decorate = decorate_func or (lambda x: x)
        self.active = self._original = active

    def create_pop_up(self):
        pop_up = ChoiceList(self)
        urwid.connect_signal(pop_up, 'close',
                             lambda button: self.close_pop_up())
        return pop_up

    def get_pop_up_parameters(self):
        return {'left': 0,
                'top': 1,
                'overlay_width': 32,
                'overlay_height': len(self.choices)}

    @property
    def changed(self):
        return self._active != self._original

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, val):
        self._active = val
        self.button = urwid.Button(self._decorate(self._active))
        urwid.PopUpLauncher.__init__(self, self.button)
        urwid.connect_signal(self.button, 'click',
                             lambda button: self.open_pop_up())


class ChoiceList(urwid.WidgetWrap):
    signals = ['close']

    def __init__(self, parent):
        self.parent = parent
        buttons = []
        for c in parent.choices:
            buttons.append(
                urwid.Button(parent._decorate(c),
                             on_press=self.set_choice, user_data=c)
            )

        pile = CPile(buttons)
        fill = urwid.Filler(pile)
        urwid.WidgetWrap.__init__(self, urwid.AttrMap(fill, 'popupbg'))

    def set_choice(self, button, account):
        self.parent.active = account
        self._emit("close")
