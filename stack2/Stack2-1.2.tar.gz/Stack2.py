class Stack:
      """
      Python Stack V2 with view and change.
      """
      def __init__(self):
              self.__storage = []

      def isEmpty(self):
              return len(self.__storage) == 0

      def push(self,p):
              self.__storage.append(p)

      def pop(self):
              return self.__storage.pop()
      def view(self):
              return self.__storage[-1]
      def change(self, new):
              self.__storage[-1] = new

