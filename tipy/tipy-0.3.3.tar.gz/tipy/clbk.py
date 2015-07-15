#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Callback class holds the buffers and allow the outer world to access them."""


class Callback(object):
    """Allow access to the current buffers from anywhere.

    This class is used as a callback to retrieve and modify the input buffers.
    There is two input buffers the left buffer and the right buffer:
        - Left buffer contains every characters preceding the cursor.
        - Right buffer contains every characters following the cursor.

    It is possible to subclass this class and override its methods in order to
    use the program in other GUIs or command line interfaces.

    G{classtree Callback}
    """

    def __init__(self):
        """Initialize the left and right buffer to empty string."""
        self.left = ''
        self.right = ''

    def update(self, character, offset=0):
        """Update the left and right buffers.

        This method should be called after each character addition or deletion
        or after each cursor move.
        In the default GUI this method is called when a signal indicating that
        the input text have changed or that the cursor position have changed.

        @param character:
            The character which has been inputted. It could be any character
            associated to keyboard keys including backspace, arrow keys...
        @type character: str
        @param offset:
            Indicate the cursor position offset against the previous cursor
            position. 0 means no move, a positive value means move to the right
            and a negative value means move to the left.
        @type offset: int
        """
        if character == '\b' and len(self.left) >= offset:
            self.left = self.left[:-offset]
        elif character == '\x1B[D' and len(self.left) >= offset:
            self.right = self.left[offset:] + self.right
            self.left = self.left[:offset]
        elif character == '\x1B[C' and len(self.right) >= offset:
            self.left += self.right[:offset]
            self.right = self.right[offset:]
        else:
            self.left += character
