class Stack:
    """
    Python Stack V2 with view and change.
    """
    def __init__(self):
        self.__storage = []

    def isEmpty(self):
        """
        Returns if the Stack is empty.
        """
        return len(self.__storage) == 0

    def push(self,p):
        """
        Add to the Stack.
        """
        self.__storage.append(p)

    def pop(self):
        """
        Delete the top element.
        """
        return self.__storage.pop()

    def view(self):
        """
        Return the Topmost item in the Stack.
        """
        return self.__storage[-1]

    def change(self, new):
        """
        Make edits to the Topmost item in the Stack.
        """
        self.__storage[-1] = new

