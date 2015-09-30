from .io_example import ListLike

__all__ = ['IOTemplate']


class IOTemplate(ListLike):
    '''Represent a group of examples.

    It has a similar API to a list, but has some additional methods.
    '''

    def __repr__(self):
        tname = type(self).__name__
        if self.template is not None:
            return '%s(%r)' % (tname, self.template)

        optargs = ''
        if self.value != 1:
            optargs += ', value=' + str(self.value)
        # if self.feedback:
        #    optargs += ', feedback=' + repr(self.feedback)

        return '%s(%r%s)' % (tname, list(self), optargs)

    def _parse(self, template):
        from .io_parser import parse_io_template
        return parse_io_template(template)

    @property
    def grade(self):
        return self.value * min(ex.grade for ex in self)

    def with_grades(self, template):
        '''Return a graded copy of itself'''

        if isinstance(template, str):
            template = IOTemplate(template)

        data = [x.with_grades(y) for (x, y) in zip(self, template)]
        return IOTemplate(data, value=self.value)

    def get_grade(self):
        '''Returns the grade for the given run'''

        return self.grade

    def get_message(self, format='text'):  # @ReservedAssignment
        '''Return a formatted message for the given run'''

        if self.grade != 1:
            mingrade = min(self, key=lambda x: x.grade)
            return mingrade.get_message()
