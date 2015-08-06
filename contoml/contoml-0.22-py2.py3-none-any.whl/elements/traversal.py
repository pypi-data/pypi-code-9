from contoml import tokens
from contoml.elements import common
from contoml.elements.metadata import PunctuationElement, NewlineElement, CommentElement


class TraversalMixin:
    """
    A mix-in that provides convenient sub-element traversal to any class with
    an `elements` member that is a sequence of Element instances
    """

    def __find_following_element(self, index, predicate):
        """
        Finds and returns the index of element in self.elements that evaluates the given predicate to True
        and whose index is higher than the given index, or returns -Infinity on failure.
        """
        for i, element in tuple(enumerate(self.elements))[index+1:]:
            if predicate(element):
                return i
        return float('-inf')

    def __find_preceding_element(self, index, predicate):
        """
        Finds and returns the index of the element in self.elements that evaluates the given predicate to True
        and whose index is lower than the given index.
        """

        for i, element in reversed(tuple(enumerate(self.elements))[:index]):
            if predicate(element):
                return i
        return float('-inf')

    def __must_find_following_element(self, predicate):
        """
        Finds and returns the index to the element in self.elements that evaluatest the predicate to True, or raises
        an error.
        """
        i = self.__find_following_element(-1, predicate)
        if i < 0:
            raise RuntimeError('Could not find non-optional element')
        return i

    def _enumerate_non_metadata_sub_elements(self):
        """
        Returns a sequence of of (index, sub_element) of the non-metadata sub-elements.
        """
        return ((i, element) for i, element in enumerate(self.elements) if element.type != common.TYPE_METADATA)

    def _find_preceding_comma(self, index):
        """
        Returns the index of the preceding comma element to the given index, or -Infinity.
        """
        def predicate(element):
            return isinstance(element, PunctuationElement) and element.token.type == tokens.TYPE_OP_COMMA
        return self.__find_preceding_element(index, predicate)

    def _find_following_comma(self, index):
        """
        Returns the index of the following comma element after the given index, or -Infinity.
        """
        def predicate(element):
            return isinstance(element, PunctuationElement) and element.token.type == tokens.TYPE_OP_COMMA
        return self.__find_following_element(index, predicate)

    def _find_following_newline(self, index):
        """
        Returns the index of the following newline element after the given index, or -Infinity.
        """
        return self.__find_following_element(index, lambda e: isinstance(e, NewlineElement))

    def _find_following_comment(self, index):
        """
        Returns the index of the following comment element after the given index, or -Infinity.
        """
        return self.__find_following_element(index, lambda e: isinstance(e, CommentElement))

    def _find_following_line_terminator(self, index):
        """
        Returns the index of the following comment or newline element after the given index, or -Infinity.
        """
        following_comment = self._find_following_comment(index)
        following_newline = self._find_following_newline(index)

        if following_comment == float('-inf'):
            return following_newline
        if following_newline == float('inf'):
            return following_comment

        if following_newline < following_comment:
            return following_newline
        else:
            return following_comment

    def _find_preceding_newline(self, index):
        """
        Returns the index of the preceding newline element to the given index, or -Infinity.
        """
        return self.__find_preceding_element(index, lambda e: isinstance(e, NewlineElement))

    def _find_following_non_metadata(self, index):
        """
        Returns the index to the following non-metadata element after the given index, or -Infinity.
        """
        return self.__find_following_element(index, lambda e: e.type != common.TYPE_METADATA)

    def _find_closing_square_bracket(self):
        """
        Returns the index to the closing square bracket, or raises an Error.
        """
        def predicate(element):
            return isinstance(element, PunctuationElement) and element.token.type == tokens.TYPE_OP_SQUARE_RIGHT_BRACKET
        return self.__must_find_following_element(predicate)

    def _find_following_opening_square_bracket(self, index):
        """
        Returns the index to the opening square bracket, or -Infinity.
        """
        def predicate(element):
            return isinstance(element, PunctuationElement) and element.token.type == tokens.TYPE_OP_SQUARE_LEFT_BRACKET
        return self.__find_following_element(index, predicate)

    def _find_following_table(self, index):
        """
        Returns the index to the next TableElement after the specified index, or -Infinity.
        """
        from contoml.elements.table import TableElement
        return self.__find_following_element(index, lambda e: isinstance(e, TableElement))

    def _find_preceding_table(self, index):
        """
        Returns the index to the preceding TableElement to the specified index, or -Infinity.
        """
        from contoml.elements.table import TableElement
        return self.__find_preceding_element(index, lambda e: isinstance(e, TableElement))

    def _find_closing_curly_bracket(self):
        """
        Returns the index to the closing curly bracket, or raises an Error.
        """
        def predicate(element):
            return isinstance(element, PunctuationElement) and element.token.type == tokens.TYPE_OP_CURLY_RIGHT_BRACKET
        return self.__must_find_following_element(predicate)

    def _find_following_table_header(self, index):
        """
        Returns the index to the table header after the given element index, or -Infinity.
        """
        from contoml.elements.tableheader import TableHeaderElement
        return self.__find_following_element(index, lambda e: isinstance(e, TableHeaderElement))
