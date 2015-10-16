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
        negation_str = ''

        if self.negated:
            negation_str = 'not_'

        return '%s=%s%s(%s)' % (
            self.field, negation_str, self.operator, ', '.join(self.parameter))
