# -*- coding: utf-8 -*-


import pygame


VALID_EFFECTS = (
    'enlarge-font-on-focus',
    'raise-line-padding-on-focus',
    'raise-col-padding-on-focus',
)


class KezMenuEffectAble(object):
    """Base class used from KezMenu."""

    def __init__(self):
        self._effects = {}

    def enableEffect(self, name, **kwargs):
        """Enable an effect in the KezMenu."""
        if name not in VALID_EFFECTS:
            raise KeyError("KezMenu doesn't know an effect of type %s" % name)
        self.__getattribute__(
            '_effectinit_{}'.format(name.replace("-", "_"))
        )(name, **kwargs)

    def disableEffect(self, name):
        """Disable an effect."""
        try:
            del self._effects[name]
            self.__getattribute__(
                '_effectdisable_%s' % name.replace("-", "_")
            )()
        except KeyError:
            pass
        except AttributeError:
            pass

    def _updateEffects(self, time_passed):
        """Update method for the effects handle"""

        for name in self._effects:
            update_func = getattr(
                self,
                '_effectupdate_{}'.format(name.replace("-", "_")),
            )
            update_func(time_passed)

    def _effectinit_enlarge_font_on_focus(self, name, **kwargs):
        """Init the effect that enlarge the focused menu entry.
        Keyword arguments can contain enlarge_time and enlarge_factor.
        """

        self._effects[name] = kwargs
        if "font" not in kwargs:
            raise TypeError(
                "enlarge_font_on_focus: font parameter is required"
            )
        if "size" not in kwargs:
            raise TypeError(
                "enlarge_font_on_focus: size parameter is required"
            )
        if "enlarge_time" not in kwargs:
            kwargs['enlarge_time'] = 0.5
        if "enlarge_factor" not in kwargs:
            kwargs['enlarge_factor'] = 2.0

        kwargs['raise_font_ps'] = (
            kwargs['enlarge_factor'] / kwargs['enlarge_time']  # pixel-per-sec
        )
        for option in self.options:
            option['font'] = pygame.font.Font(kwargs['font'], kwargs['size'])
            option['font_current_size'] = kwargs['size']
            option['raise_font_factor'] = 1.0

    def _effectupdate_enlarge_font_on_focus(self, time_passed):
        """Gradually enlarge the font size of the focused line."""

        data = self._effects['enlarge-font-on-focus']
        fps = data['raise_font_ps']
        final_size = data['size'] * data['enlarge_factor']
        for i, option in enumerate(self.options):
            if i == self.option:
                # Raise me
                if option['font_current_size'] < final_size:
                    option['raise_font_factor'] += fps * time_passed
                elif option['font_current_size'] > final_size:
                    option['raise_font_factor'] = data['enlarge_factor']
            elif option['raise_font_factor'] != 1.0:
                # decrease
                if option['raise_font_factor'] > 1.0:
                    option['raise_font_factor'] -= fps * time_passed
                elif option['raise_font_factor'] < 1.0:
                    option['raise_font_factor'] = 1.0

            new_size = int(data['size'] * option['raise_font_factor'])
            if new_size != option['font_current_size']:
                option['font'] = pygame.font.Font(data['font'], new_size)
                option['font_current_size'] = new_size

    def _effectdisable_enlarge_font_on_focus(self):
        """Restore the base font."""

        self.font = self._font

    def _effectinit_raise_line_padding_on_focus(self, name, **kwargs):
        """Init the effect for the empty space around the focused entry.
        Keyword arguments can contain enlarge_time and padding.
        """

        self._effects[name] = kwargs
        if "enlarge_time" not in kwargs:
            kwargs['enlarge_time'] = 0.5
        if "padding" not in kwargs:
            kwargs['padding'] = 10
        kwargs['padding_pps'] = kwargs['padding'] / kwargs['enlarge_time']
        # Now, every menu voices need additional infos
        for o in self.options:
            o['padding_line'] = 0.0

    def _effectupdate_raise_line_padding_on_focus(self, time_passed):
        """Gradually enlarge the padding of the focused line."""

        data = self._effects['raise-line-padding-on-focus']
        pps = data['padding_pps']
        for i, option in enumerate(self.options):
            if i == self.option:
                # Raise me
                if option['padding_line'] < data['padding']:
                    option['padding_line'] += pps * time_passed
                elif option['padding_line'] > data['padding']:
                    option['padding_line'] = data['padding']
            elif option['padding_line']:
                if option['padding_line'] > 0:
                    option['padding_line'] -= pps * time_passed
                elif option['padding_line'] < 0:
                    option['padding_line'] = 0

    def _effectdisable_raise_line_padding_on_focus(self):
        """Delete all line paddings."""

        for option in self.options:
            del option['padding_line']

    def _effectinit_raise_col_padding_on_focus(self, name, **kwargs):
        """Init the column padding on focus effect.
        Keyword arguments can contain enlarge_time and padding.
        """

        self._effects[name] = kwargs
        if "enlarge_time" not in kwargs:
            kwargs['enlarge_time'] = 0.5
        if "padding" not in kwargs:
            kwargs['padding'] = 10
        kwargs['padding_pps'] = kwargs['padding'] / kwargs['enlarge_time']

        for option in self.options:
            option['padding_col'] = 0.0

    def _effectupdate_raise_col_padding_on_focus(self, time_passed):
        """Gradually enlarge the padding of the focused column."""

        data = self._effects['raise-col-padding-on-focus']
        pps = data['padding_pps']
        for i, option in enumerate(self.options):
            if i == self.option:
                # Raise me
                if option['padding_col'] < data['padding']:
                    option['padding_col'] += pps * time_passed
                elif option['padding_col'] > data['padding']:
                    option['padding_col'] = data['padding']
            elif option['padding_col']:
                if option['padding_col'] > 0:
                    option['padding_col'] -= pps * time_passed
                elif option['padding_col'] < 0:
                    option['padding_col'] = 0

    def _effectdisable_raise_col_padding_on_focus(self):
        """Delete all column paddings."""

        for option in self.options:
            del option['padding_col']
