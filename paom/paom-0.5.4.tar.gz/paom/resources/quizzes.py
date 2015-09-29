from paom.base import BaseResource


class Quizzes(BaseResource):

    ABSOLUTE_URL = "/quizzes/"
    REQUEST_TYPES = ["GET", "POST", "ALL"]


class Questions(BaseResource):

    ABSOLUTE_URL = "/questions/"
    REQUEST_TYPES = ["POST", "ALL"]


class Answers(BaseResource):

    ABSOLUTE_URL = "/answers/"
    REQUEST_TYPES = ["POST", "ALL"]


class QuizResults(BaseResource):

    ABSOLUTE_URL = "/quiz-results/"
    REQUEST_TYPES = ["POST", "ALL"]


class UserAnswers(BaseResource):

    ABSOLUTE_URL = "/user-answers/"
    REQUEST_TYPES = ["POST", "ALL"]


class UserResults(BaseResource):

    ABSOLUTE_URL = "/user-results/"
    REQUEST_TYPES = ["POST", "ALL"]
