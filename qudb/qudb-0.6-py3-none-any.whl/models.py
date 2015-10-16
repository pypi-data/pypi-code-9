from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import sessionmaker, relationship, backref
#from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()

# TODO: cascade behavior
# TODO: enable foreign key support:
# http://docs.sqlalchemy.org/en/rel_0_9/dialects/sqlite.html#sqlite-foreign-keys


class Term(Base):
    __tablename__ = 'term'

    id = Column(Integer, primary_key=True)
    code = Column(String(3), nullable=False, unique=True)

    assessments = relationship('Assessment', backref='term')

    @staticmethod
    def get(session, term):
        results = session.query(Term).filter_by(code=term)
        try:
            return results.one()
        except NoResultFound:
            raise TermDoesNotExist

    @staticmethod
    def filter(session, atype=None):
        results = session.query(Term)
        if atype is not None:
            results = results.join(Assessment).join(AssessmentType) \
                             .filter_by(name=atype)
        return results.order_by(Term.code)

    def __str__(self):
        return '{}'.format(self.code)


class AssessmentType(Base):
    __tablename__ = 'assessment_type'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    label = Column(String)

    assessments = relationship('Assessment', backref='type')

    @staticmethod
    def filter(session, term=None, question=None):
        results = session.query(AssessmentType)
        if term is not None:
            results = results.join(Assessment).join(Term).filter_by(code=term)
        if question is not None:
            results = results.join(Assessment).join(AssessmentQuestion) \
                             .join(Question).filter_by(file=question)
        return results.order_by(AssessmentType.name)

    @staticmethod
    def get(session, atype):
        results = session.query(AssessmentType).filter_by(name=atype)
        try:
            return results.one()
        except NoResultFound:
            raise AssessmentTypeDoesNotExist

    def __repr__(self):
        return self.label or self.name


class Assessment(Base):
    __tablename__ = 'assessment'

    term_id = Column(Integer, ForeignKey('term.id'), primary_key=True)
    type_id = Column(Integer, ForeignKey('assessment_type.id'),
                     primary_key=True)

    date = Column(Date, default=None)  # TODO: use and test!
    # TODO: material = Column(Text, default=None)

    @hybrid_property
    def name(self):
        return '{} {}'.format(self.term, self.type)

    # TODO: try hybrid_property for {avg/max/min}_score (compute from
    # questions)

    # assessment_questions (aqs)
    aqs = relationship('AssessmentQuestion',
        primaryjoin='and_(Assessment.term_id==AssessmentQuestion.term_id, '
                         'Assessment.type_id==AssessmentQuestion.type_id, '
                         'AssessmentQuestion.question_id==Question.id, '
                         'Question.mcq==False)',
        backref='assessment',
        order_by='AssessmentQuestion.order',
        collection_class=ordering_list('order', count_from=1))
    # assessment_multiple_choice_questions (amcqs)
    amcqs = relationship('AssessmentQuestion',
        primaryjoin='and_(Assessment.term_id==AssessmentQuestion.term_id, '
                         'Assessment.type_id==AssessmentQuestion.type_id, '
                         'AssessmentQuestion.question_id==Question.id, '
                         'Question.mcq==True)',
        backref='mc_assessment',
        order_by='AssessmentQuestion.order',
        collection_class=ordering_list('order', count_from=1))

    # questions (qs) and multiple-choice questions (mcqs)
    qs = association_proxy('aqs', 'question')
    mcqs = association_proxy('amcqs', 'question')

    @staticmethod
    def filter(session, term=None, atype=None, question=None):
        results = session.query(Assessment)
        if term is not None:
            results = results.join(Term).filter_by(code=term)
        if atype is not None:
            results = results.join(AssessmentType).filter_by(name=atype)
        if question is not None:
            results = results.join(AssessmentQuestion).join(Question) \
                             .filter_by(file=question)
        return results.order_by(Assessment.date)

    @staticmethod
    def get(session, term, atype):
        results = Assessment.filter(session, term, atype)
        try:
            return results.one()
        except NoResultFound:
            raise AssessmentDoesNotExist

    @staticmethod
    def add_question(session, term, atype, question, mcq=False, bonus=False,
                     points=None, order=None, date=None, commit=True):
        a, q = _get_or_create_a_q(session, term, atype, question, mcq)

        # Update non-unique attributes
        if date is not None:
            if a.date is not None:
                raise AssessmentDateExists
            else:
                a.date = date

        # TODO: add other assessment_question fields: students, avg, max, min
        if mcq:
            if q in a.mcqs:
                raise AssessmentQuestionExists
            elif order is None:
                a.amcqs.append(AssessmentQuestion(question=q,
                    bonus=bonus, points=points))
            else:
                a.amcqs.insert(order-1, AssessmentQuestion(question=q,
                    bonus=bonus, points=points))
        else:
            if q in a.qs:
                raise AssessmentQuestionExists
            elif order is None:
                a.aqs.append(AssessmentQuestion(question=q,
                    bonus=bonus, points=points))
            else:
                a.aqs.insert(order-1, AssessmentQuestion(question=q,
                    bonus=bonus, points=points))
        session.add(a)
        if commit:
            session.commit()

    @staticmethod
    def update_question(session, term, atype, question, mcq=False, bonus=False,
                        points=None, order=None, date=None):
        a, q, aq = _get_a_q_aq(session, term, atype, question)

        if aq.equals(bonus, points, order):  # TODO: remaining fields
            raise NoChangeRequired
        # update all non-order fields
        if points is not None:
            aq.points = points
        if bonus is not None:
            aq.bonus = bonus
        if date is not None:
            a.date = date
        # TODO: remaining fields
        if order is not None and order != aq.order:
            # update order
            if mcq:
                assert aq in a.amcqs
                a.amcqs.remove(aq)
                a.amcqs.insert(order, aq)
            else:
                assert aq in a.aqs
                a.aqs.remove(aq)
                a.aqs.insert(order-1, aq)

        session.add(a)
        session.commit()

    def update_assessment(session, term, atype, date):
        a = Assessment.get(session, term, atype)
        if date is None or date == a.date:
            raise NoChangeRequired
        a.date = date
        session.add(a)
        session.commit()

    def remove_question(session, term, atype, question):
        a, q, aq = _get_a_q_aq(session, term, atype, question)

        if q.mcq:
            a.amcqs.remove(aq)
        else:
            a.aqs.remove(aq)
        session.delete(aq)
        session.add(a)

        # remove q, a, at, t with no assessment-questions
        if len(q.assessment_questions) == 0:
            session.delete(q)
        if len(a.aqs) == 0 and len(a.amcqs) == 0:
            session.delete(a)
        if len(a.type.assessments) == 0:
            session.delete(a.type)
        if len(a.term.assessments) == 0:
            session.delete(a.term)

        session.commit()

    def __repr__(self):
        return self.name


class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    file = Column(String, nullable=False, unique=True)
    mcq = Column(Boolean, default=False)
    chapter = Column(String)

    # TODO: try hybrid_property for {avg/max/min}_score (compute from
    # assessment_questions)

    @staticmethod
    def filter(session, term=None, atype=None, question=None, mcq=None):
        results = session.query(Question)
        if question is not None:
            results = results.filter_by(file=question)
        if mcq is not None:
            results = results.filter_by(mcq=mcq)
        if term is not None or atype is not None:
            results = results.join(AssessmentQuestion).join(Assessment)
        if term is not None:
            results = results.join(Term).filter_by(code=term)
        if atype is not None:
            results = results.join(AssessmentType).filter_by(name=atype)
        return results.order_by(Question.file)

    @staticmethod
    def get(session, question):
        results = session.query(Question).filter_by(file=question)
        try:
            return results.one()
        except NoResultFound:
            raise QuestionDoesNotExist

    def __repr__(self):
        return '{}{}'.format(self.file, ' (MCQ)' if self.mcq else '')


class AssessmentQuestion(Base):
    __tablename__ = 'assessment_question'

    question_id = Column(Integer, ForeignKey('question.id'), primary_key=True)
    term_id = Column(Integer, primary_key=True)
    type_id = Column(Integer) # not a primary key to use a question
                              # only once per term
    bonus = Column(Boolean, default=False)
    points = Column(Integer)
    order = Column(Integer)
    student_count = Column(Integer)  # should be an Assessment, or Term, attribute
    avg_score = Column(Integer)
    max_score = Column(Integer)
    min_score = Column(Integer)

    question = relationship('Question', backref='assessment_questions')

    @hybrid_property
    def file(self):
        return self.question.file

    __table_args__ = (
        ForeignKeyConstraint(['term_id', 'type_id'],
                             ['assessment.term_id', 'assessment.type_id']),
        # UniqueConstraint('term_id', 'type_id', 'order')
        #  unique constraint commented out for two reasons:
        #  1. causes issues with SQLAlchemy's OrderingList extension
        #  2. prevents MCQs and normal questions from being listed in
        #     the same table (they can have the same order)
    )

    # TODO: compare remaining fields
    def equals(self, bonus, points, order):
        return (bonus is None or self.bonus == bonus) \
           and (points is None or self.points == points) \
           and (order is None or self.order == order)

    @staticmethod
    def filter(session, term=None, atype=None, question=None, mcq=None):
        results = session.query(AssessmentQuestion)
        if question is not None or mcq is not None:
            results = results.join(Question)
        if question is not None:
            results = results.filter_by(file=question)
        if mcq is not None:
            results = results.filter_by(mcq=mcq)
        if term is not None or atype is not None:
            results = results.join(Assessment)
        if term is not None:
            results = results.join(Term).filter_by(code=term)
        if atype is not None:
            results = results.join(AssessmentType).filter_by(name=atype)
        # order
        if atype is None:
            results = results.order_by(Question.file)
        else:
            results = results.order_by(AssessmentQuestion.order)
        return results

    @staticmethod
    def get(session, term, atype, question):
        results = AssessmentQuestion.filter(session, term, atype, question)
        try:
            return results.one()
        except NoResultFound:
            raise AssessmentQuestionDoesNotExist

    # @staticmethod
    # def by_assessment(session, mcq, term, atype):
    #     assessment = Assessment.get(session, term, atype)
    #     if mcq:
    #         return assessment.amcqs
    #     else:
    #         return assessment.aqs

    def __str__(self):
        return '{}. {} {}{}'.format(self.order, self.question,
            '+' if self.bonus else '',
            self.points if self.points is not None else '')

    def __repr__(self):
        return '{}(question={}, order={})'.format(
            type(self).__name__, self.question, self.order)


def get_one_or_create(session, model, **kwargs):
    try:
        # lookup by unique fields only
        instance = session.query(model).filter_by(**kwargs).one()
    except NoResultFound:
        # insert all fields
        instance = model(**kwargs)
        session.add(instance)
        session.flush()
    return instance


def _get_or_create_a_q(session, term, atype, question, mcq):
    t = get_one_or_create(session, Term, code=term)
    at = get_one_or_create(session, AssessmentType, name=atype)
    a = get_one_or_create(session, Assessment, term=t, type=at)
    q = get_one_or_create(session, Question, file=question, mcq=mcq)
    return a, q


def _get_a_q_aq(session, term, atype, question):
    a = Assessment.get(session, term, atype)
    q = Question.get(session, question)
    aq = AssessmentQuestion.get(session, term, atype, question)
    return a, q, aq


def init(db):
    db = db or ':memory:'
    engine = create_engine('sqlite:///{}'.format(db))
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


class AssessmentQuestionExists(Exception):
    '''The specified question already belongs to the specified assessment'''
    pass


class AssessmentQuestionDoesNotExist(Exception):
    '''The specified question does not belong to the specified assessment'''
    pass


class QuestionDoesNotExist(Exception):
    '''The specified question does not exist in any assessment'''
    pass


class AssessmentDoesNotExist(Exception):
    '''The specified assessment does not exist'''
    pass


class AssessmentTypeDoesNotExist(Exception):
    '''The specified assessment-type does not exist'''
    pass


class TermDoesNotExist(Exception):
    '''The specified assessment does not exist'''
    pass


class NoChangeRequired(Exception):
    pass


class AssessmentDateExists(Exception):
    pass
