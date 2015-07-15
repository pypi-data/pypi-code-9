from __future__ import unicode_literals

from pygments.lexers import BashLexer
from pygments.token import Token

from ..enums import IncrementalSearchDirection

from .processors import BeforeInput

from . import Window
from .dimension import LayoutDimension
from .controls import BufferControl, TokenListControl, UIControl
from .utils import token_list_len
from .screen import Screen
from prompt_toolkit.filters import HasFocus, HasArg, HasCompletions, HasValidationError, HasSearch, Never, Always, IsDone
from prompt_toolkit.enums import SEARCH_BUFFER, SYSTEM_BUFFER


__all__ = (
    'ArgToolbar',
    'CompletionsToolbar',
    'SearchToolbar',
    'SystemToolbar',
    'ValidationToolbar',
)


class TokenListToolbar(Window):
    def __init__(self, get_tokens, default_char=None, filter=Always()):
        super(TokenListToolbar, self).__init__(
            TokenListControl(get_tokens, default_char=default_char),
            height=LayoutDimension.exact(1),
            filter=filter)


class SystemToolbarControl(BufferControl):
    def __init__(self):
        super(SystemToolbarControl, self).__init__(
            lexer=BashLexer,
            buffer_name=SYSTEM_BUFFER,
            show_line_numbers=Never(),
            input_processors=[BeforeInput.static('Shell command: ', Token.Toolbar.System.Prefix)],)


class SystemToolbar(Window):
    def __init__(self):
        super(SystemToolbar, self).__init__(
            SystemToolbarControl(),
            height=LayoutDimension.exact(1),
            filter=HasFocus(SYSTEM_BUFFER) & ~IsDone())


class ArgToolbarControl(TokenListControl):
    def __init__(self):
        def get_tokens(cli):
            return [
                (Token.Toolbar.Arg, 'Repeat: '),
                (Token.Toolbar.Arg.Text, str(cli.input_processor.arg)),
            ]

        super(ArgToolbarControl, self).__init__(get_tokens)


class ArgToolbar(Window):
    def __init__(self):
        super(ArgToolbar, self).__init__(
            ArgToolbarControl(),
            height=LayoutDimension.exact(1),
            filter=HasArg())


class SearchToolbarControl(BufferControl):
    """
    :param vi_mode: Display '/' and '?' instead of I-search.
    """
    def __init__(self, vi_mode=False):
        token = Token.Toolbar.Search

        def get_before_input(cli):
            if not cli.is_searching:
                text = ''
            elif cli.search_state.direction == IncrementalSearchDirection.BACKWARD:
                text = ('?' if vi_mode else 'I-search backward: ')
            else:
                text = ('/' if vi_mode else 'I-search: ')

            return [(token, text)]

        super(SearchToolbarControl, self).__init__(
            buffer_name=SEARCH_BUFFER,
            input_processors=[BeforeInput(get_before_input)],
        )


class SearchToolbar(Window):
    def __init__(self, vi_mode=False):
        super(SearchToolbar, self).__init__(
            SearchToolbarControl(vi_mode=vi_mode),
            height=LayoutDimension.exact(1),
            filter=HasSearch() & ~IsDone())


class CompletionsToolbarControl(UIControl):
    token = Token.Toolbar.Completions

    def create_screen(self, cli, width, height):
        complete_state = cli.current_buffer.complete_state
        if complete_state:
            completions = complete_state.current_completions
            index = complete_state.complete_index  # Can be None!

            # Width of the completions without the left/right arrows in the margins.
            content_width = width - 6

            # Booleans indicating whether we stripped from the left/right
            cut_left = False
            cut_right = False

            # Create Menu content.
            tokens = []

            for i, c in enumerate(completions):
                # When there is no more place for the next completion
                if token_list_len(tokens) + len(c.display) >= content_width:
                    # If the current one was not yet displayed, page to the next sequence.
                    if i <= (index or 0):
                        tokens = []
                        cut_left = True
                    # If the current one is visible, stop here.
                    else:
                        cut_right = True
                        break

                tokens.append((self.token.Completion.Current if i == index else self.token.Completion, c.display))
                tokens.append((self.token, ' '))

            # Extend/strip until the content width.
            tokens.append((self.token, ' ' * (content_width - token_list_len(tokens))))
            tokens = tokens[:content_width]

            # Return tokens
            all_tokens = [
                (self.token, ' '),
                (self.token.Arrow, '<' if cut_left else ' '),
                (self.token, ' '),
            ] + tokens + [
                (self.token, ' '),
                (self.token.Arrow, '>' if cut_right else ' '),
                (self.token, ' '),
            ]
        else:
            all_tokens = []

        screen = Screen(width)
        screen.write_data(all_tokens, width)
        return screen


class CompletionsToolbar(Window):
    def __init__(self, extra_filter=Always()):
        super(CompletionsToolbar, self).__init__(
            CompletionsToolbarControl(),
            height=LayoutDimension.exact(1),
            filter=HasCompletions() & ~IsDone() & extra_filter)


class ValidationToolbarControl(TokenListControl):
    def __init__(self, show_position=False):
        token = Token.Toolbar.Validation

        def get_tokens(cli):
            buffer = cli.current_buffer

            if buffer.validation_error:
                row, column = buffer.document.translate_index_to_position(
                    buffer.validation_error.index)

                if show_position:
                    text = '%s (line=%s column=%s)' % (
                        buffer.validation_error.message, row, column)
                else:
                    text = buffer.validation_error.message

                return [(token, text)]
            else:
                return []

        super(ValidationToolbarControl, self).__init__(get_tokens)


class ValidationToolbar(Window):
    def __init__(self, show_position=False):
        super(ValidationToolbar, self).__init__(
            ValidationToolbarControl(show_position=show_position),
            height=LayoutDimension.exact(1),
            filter=HasValidationError() & ~IsDone())
