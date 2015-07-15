from __future__ import unicode_literals

from six.moves import zip_longest
from prompt_toolkit.filters import HasCompletions, IsDone, Always
from prompt_toolkit.utils import get_cwidth
from pygments.token import Token

from .controls import UIControl
from .containers import Window
from .dimension import LayoutDimension
from .screen import Screen

import math

__all__ = (
    'CompletionsMenu',
    'MultiColumnCompletionsMenu',
)


class CompletionsMenuControl(UIControl):
    """
    Helper for drawing the complete menu to the screen.
    """
    def __init__(self):
        self.token = Token.Menu.Completions

    def has_focus(self, cli):
        return False

    def preferred_width(self, cli, max_available_width):
        complete_state = cli.current_buffer.complete_state
        if complete_state:
            menu_width = self._get_menu_width(500, complete_state)
            menu_meta_width = self._get_menu_meta_width(500, complete_state)

            return menu_width + menu_meta_width + 1
        else:
            return 0

    def preferred_height(self, cli, width):
        complete_state = cli.current_buffer.complete_state
        if complete_state:
            return len(complete_state.current_completions)
        else:
            return 0

    def create_screen(self, cli, width, height):
        """
        Write the menu to the screen object.
        """
        screen = Screen(width)

        complete_state = cli.current_buffer.complete_state
        if complete_state:
            completions = complete_state.current_completions
            index = complete_state.complete_index  # Can be None!

            # Calculate width of completions menu.
            menu_width = self._get_menu_width(width - 1, complete_state)
            menu_meta_width = self._get_menu_meta_width(width - 1 - menu_width, complete_state)
            show_meta = self._show_meta(complete_state)

            if menu_width + menu_meta_width + 1 < width:
                menu_width += width - (menu_width + menu_meta_width + 1)

            # Decide which slice of completions to show.
            if len(completions) > height and (index or 0) > height / 2:
                slice_from = min(
                    (index or 0) - height // 2,  # In the middle.
                    len(completions) - height  # At the bottom.
                )
            else:
                slice_from = 0

            slice_to = min(slice_from + height, len(completions))

            # Create a function which decides at which positions the scroll button should be shown.
            def is_scroll_button(row):
                items_per_row = float(len(completions)) / min(len(completions), height)
                items_on_this_row_from = row * items_per_row
                items_on_this_row_to = (row + 1) * items_per_row
                return items_on_this_row_from <= (index or 0) < items_on_this_row_to

            # Write completions to screen.
            tokens = []

            for i, c in enumerate(completions[slice_from:slice_to]):
                is_current_completion = (i + slice_from == index)

                if is_scroll_button(i):
                    button_token = self.token.ProgressButton
                else:
                    button_token = self.token.ProgressBar

                if tokens:
                    tokens += [(Token, '\n')]
                tokens += (self._get_menu_item_tokens(c, is_current_completion, menu_width) +
                           (self._get_menu_item_meta_tokens(c, is_current_completion, menu_meta_width)
                               if show_meta else []) +
                           [(button_token, ' '), ])

            screen.write_data(tokens, width)

        return screen

    def _show_meta(self, complete_state):
        """
        Return ``True`` if we need to show a column with meta information.
        """
        return any(c.display_meta for c in complete_state.current_completions)

    def _get_menu_width(self, max_width, complete_state):
        """
        Return the width of the main column.
        """
        return min(max_width, max(get_cwidth(c.display)
                   for c in complete_state.current_completions) + 2)

    def _get_menu_meta_width(self, max_width, complete_state):
        """
        Return the width of the meta column.
        """
        if self._show_meta(complete_state):
            return min(max_width, max(get_cwidth(c.display_meta)
                       for c in complete_state.current_completions) + 2)
        else:
            return 0

    def _get_menu_item_tokens(self, completion, is_current_completion, width):
        if is_current_completion:
            token = self.token.Completion.Current
        else:
            token = self.token.Completion

        text, tw = _trim_text(completion.display, width - 2)
        padding = ' ' * (width - 2 - tw)
        return [(token, ' %s%s ' % (text, padding))]

    def _get_menu_item_meta_tokens(self, completion, is_current_completion, width):
        if is_current_completion:
            token = self.token.Meta.Current
        else:
            token = self.token.Meta

        text, tw = _trim_text(completion.display_meta, width - 2)
        padding = ' ' * (width - 2 - tw)
        return [(token, ' %s%s ' % (text, padding))]


def _trim_text(text, max_width):
    """
    Trim the text to `max_width`, append dots when the text is too long.
    Returns (text, width) tuple.
    """
    width = get_cwidth(text)

    # When the text is too wide, trim it.
    if width > max_width:
        # When there are no double width characters, just use slice operation.
        if len(text) == width:
            trimmed_text = (text[:max(1, max_width-3)] + '...')[:max_width]
            return trimmed_text, len(trimmed_text)

        # Otherwise, loop until we have the desired width. (Rather
        # inefficient, but ok for now.)
        else:
            trimmed_text = ''
            for c in text:
                if get_cwidth(trimmed_text + c) <= max_width - 3:
                    trimmed_text += c
            trimmed_text += '...'

            return (trimmed_text, get_cwidth(trimmed_text))
    else:
        return text, width


class CompletionsMenu(Window):
    def __init__(self, max_height=None, extra_filter=Always()):
        super(CompletionsMenu, self).__init__(
            content=CompletionsMenuControl(),
            width=LayoutDimension(min=8),
            height=LayoutDimension(min=1, max=max_height),
            # Show when there are completions but not at the point we are
            # returning the input.
            filter=HasCompletions() & ~IsDone() & extra_filter)


class MultiColumnCompletionMenuControl(UIControl):
    """
    Completion menu that displays all the completions in several columns.
    When there are more completions than space for them to be displayed, an
    arrow is shown on the left or right side.

    `min_rows` indicates how many rows will be available in any possible case.
    When this is langer than one, in will try to use less columns and more
    rows until this value is reached.
    Be careful passing in a too big value, if less than the given amount of
    rows are available, more columns would have been required, but
    `preferred_width` doesn't know about that and reports a too small value.
    This results in less completions displayed and additional scrolling.
    (It's a limitation of how the layout engine currently works: first the
    widths are calculated, then the heights.)
    """
    _required_margin = 3  # One extra padding on the right + space for arrows.

    def __init__(self, min_rows=3):
        assert isinstance(min_rows, int) and min_rows >= 1

        self.token = Token.Menu.Completions
        self.min_rows = min_rows
        self.scroll_offset = 0

    def reset(self):
        self.scroll_offset = 0

    def has_focus(self, cli):
        return False

    def preferred_width(self, cli, max_available_width):
        """
        Preferred width: prefer to use at least min_rows, but otherwise as much
        as possible horizontally.
        """
        complete_state = cli.current_buffer.complete_state
        column_width = self._get_column_width(complete_state)
        result = int(column_width * math.ceil(len(complete_state.current_completions) / float(self.min_rows)))

        # When the desired width is still more than the maximum available,
        # reduce by removing columns until we are less than the available
        # width.
        while result > column_width and result > max_available_width - self._required_margin:
            result -= column_width
        return result + self._required_margin

    def preferred_height(self, cli, width):
        """
        Preferred height: as much as needed in order to display all the completions.
        """
        complete_state = cli.current_buffer.complete_state
        column_width = self._get_column_width(complete_state)
        column_count = max(1, (width - self._required_margin) // column_width)

        return int(math.ceil(len(complete_state.current_completions) / float(column_count)))

    def create_screen(self, cli, width, height):
        """
        Write the menu to the screen object.
        """
        complete_state = cli.current_buffer.complete_state
        column_width = self._get_column_width(complete_state)

        screen = Screen(width)

        def grouper(n, iterable, fillvalue=None):
            " grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx "
            args = [iter(iterable)] * n
            return zip_longest(fillvalue=fillvalue, *args)

        def is_current_completion(completion):
            " Returns True when this completion is the currently selected one. "
            return complete_state.complete_index is not None and c == complete_state.current_completion

        if complete_state:
            column_width = min(width, column_width)
            visible_columns = (width - self._required_margin) // column_width

            columns_ = list(grouper(height, complete_state.current_completions))
            rows_ = list(zip(*columns_))

            # Make sure the current completion is always visible: update scroll offset.
            selected_column = (complete_state.complete_index or 0) // height
            self.scroll_offset = min(selected_column, max(self.scroll_offset, selected_column - visible_columns + 1))

            # Write completions to screen.
            tokens = []

            for row_index, row in enumerate(rows_):
                middle_row = row_index == len(rows_) // 2

                # Draw left arrow if we have hidden completions on the left.
                if self.scroll_offset > 0:
                    tokens += [(self.token.ProgressBar, '<' if middle_row else ' ')]

                # Draw row content.
                for column_index, c in enumerate(row[self.scroll_offset:][:visible_columns]):
                    if c is not None:
                        tokens += self._get_menu_item_tokens(c, is_current_completion(c), column_width)
                    else:
                        tokens += [(self.token.Completion, ' ' * column_width)]

                # Draw trailing padding. (_get_menu_item_tokens only returns padding on the left.)
                tokens += [(self.token.Completion, ' ')]

                # Draw right arrow if we have hidden completions on the right.
                if self.scroll_offset < len(rows_[0]) - visible_columns:
                    tokens += [(self.token.ProgressBar, '>' if middle_row else ' ')]

                # Newline.
                tokens += [(self.token.ProgressBar, '\n')]

            screen.write_data(tokens, width)

        return screen

    def _get_column_width(self, complete_state):
        """
        Return the width of each column.
        """
        return max(get_cwidth(c.display) for c in complete_state.current_completions) + 1

    def _get_menu_item_tokens(self, completion, is_current_completion, width):
        if is_current_completion:
            token = self.token.Completion.Current
        else:
            token = self.token.Completion

        text, tw = _trim_text(completion.display, width)
        padding = ' ' * (width - tw - 1)

        return [(token, ' %s%s' % (text, padding))]


class MultiColumnCompletionsMenu(Window):
    def __init__(self, min_rows=3, extra_filter=Always()):
        super(MultiColumnCompletionsMenu, self).__init__(
            content=MultiColumnCompletionMenuControl(min_rows=min_rows),
            width=LayoutDimension(min=8),
            height=LayoutDimension(min=1),
            # Show when there are completions but not at the point we are
            # returning the input.
            filter=HasCompletions() & ~IsDone() & extra_filter)
