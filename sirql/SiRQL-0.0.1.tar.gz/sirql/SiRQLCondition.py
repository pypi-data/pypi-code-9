
class SiRQLCondition(object):
    def __init__(self, field, operator, *parameter):
        self.field = field
        self.operator = operator
        self.parameter = parameter
        self.negated = False

    @staticmethod
    def init(field, operator, negated, *parameter):
        sirql_condition = SiRQLCondition(field, operator, *parameter)
        sirql_condition.negated = negated
        return sirql_condition

    def __str__(self):
        return '%s %s (%s)' % (self.field, self.operator, ', '.join(self.parameter))

