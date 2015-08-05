from django.test import TestCase
from quizblock_random.models import QuizRandom, Submission, QuestionUserLock
from django.contrib.auth.models import User
from .factories import (
    Dummy, QuestionUserLockFactory, CustomPagetreeModuleFactory,
    QuestionFactory, UserFactory, QuizRandomFactory)


class FakeReq(object):
    def __init__(self):
        self.POST = dict()


class TestBasics(TestCase):
    def test_create(self):
        q = QuizRandom()
        self.assertNotEqual(q, None)

    def test_add_form(self):
        f = QuizRandom.add_form()
        self.assertTrue('allow_redo' in f.fields)
        self.assertTrue('show_submit_state' in f.fields)

    def test_create_method(self):
        r = FakeReq()
        q = QuizRandom.create(r)
        self.assertEquals(q.description, '')
        self.assertEquals(q.display_name, 'Quiz Random')
        self.assertFalse(q.show_submit_state)
        self.assertFalse(q.allow_redo)

    def test_create_method_two(self):
        r = FakeReq()
        r.POST['show_submit_state'] = 'on'
        r.POST['allow_redo'] = 'on'
        q = QuizRandom.create(r)
        self.assertEquals(q.description, '')
        self.assertEquals(q.display_name, 'Quiz Random')
        self.assertTrue(q.show_submit_state)
        self.assertTrue(q.allow_redo)

    def test_dict_roundtrip(self):
        q1 = QuizRandom(description="first", show_submit_state=False)
        d = q1.as_dict()
        q2 = QuizRandom(description="second")
        q2.import_from_dict(d)
        self.assertEquals(q2.description, "first")
        self.assertEquals(q1.allow_redo, q2.allow_redo)
        self.assertEquals(q1.show_submit_state, q2.show_submit_state)

    def test_create_from_dict(self):
        q = QuizRandom(description="first")
        d = q.as_dict()
        q2 = QuizRandom.create_from_dict(d)
        self.assertEquals(q2.description, "first")
        self.assertEquals(q.allow_redo, q2.allow_redo)
        self.assertEquals(q.show_submit_state, q2.show_submit_state)

    def test_create_from_dict_defaults(self):
        d = {
            'description': 'Test QuizRandom',
            'rhetorical': True,
            'questions': [],
        }
        q = QuizRandom.create_from_dict(d)
        self.assertEquals(q.description, 'Test QuizRandom')
        self.assertEquals(q.allow_redo, True)
        self.assertEquals(q.show_submit_state, True)

    def test_import_from_dict_defaults(self):
        d = {
            'description': 'Test QuizRandom',
            'rhetorical': True,
            'questions': [],
        }
        q = QuizRandom()
        q.import_from_dict(d)
        self.assertEqual(q.description, 'Test QuizRandom')
        self.assertEqual(q.allow_redo, True)
        self.assertEqual(q.show_submit_state, True)
        self.assertEqual(q.submission_set.count(), 0)
        self.assertEqual(q.question_set.count(), 0)

    def test_import_from_dict_defaults_2(self):
        d = {
            'description': 'Test QuizRandom',
            'allow_redo': False,
            'rhetorical': True,
            'show_submit_state': True,
            'questions': [{
                'text': 'Test Question',
                'question_type': 'single choice',
                'explanation': '',
                'intro_text': '',
                'answers': [],
            }],
        }
        q = QuizRandom()
        q.import_from_dict(d)
        self.assertEqual(q.description, 'Test QuizRandom')
        self.assertEqual(q.allow_redo, False)
        self.assertEqual(q.show_submit_state, True)
        self.assertEqual(q.submission_set.count(), 0)
        self.assertEqual(q.question_set.count(), 1)

    def test_edit(self):
        q = QuizRandom()
        q.edit(dict(description='foo',
                    allow_redo='0', show_submit_state='on'), None)
        self.assertEqual(q.description, 'foo')
        self.assertEqual(q.allow_redo, '0')
        self.assertTrue(q.show_submit_state)

    def test_edit_two(self):
        q = QuizRandom()
        q.edit(dict(description='foo'), None)
        self.assertEqual(q.description, 'foo')
        self.assertFalse(q.allow_redo)
        self.assertFalse(q.show_submit_state)


class UserTests(TestCase):
    def setUp(self):
        self.u = User.objects.create(username="testuser")

    def test_submit(self):
        q = QuizRandom.objects.create()
        self.assertFalse(q.unlocked(self.u))
        q.submit(self.u, dict(foo='bar'))
        self.assertTrue(q.unlocked(self.u))
        q.clear_user_submissions(self.u)
        self.assertFalse(q.unlocked(self.u))


class TestIsUserCorrect(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.quiz = QuizRandom.objects.create()

    def test_no_questions(self):
        self.assertEquals(self.quiz.score(self.user), None)


class SubmissionTest(TestCase):
    def test_unicode(self):
        quiz = QuizRandom.objects.create()
        user = User.objects.create(username="testuser")
        s = Submission.objects.create(quiz=quiz, user=user)
        self.assertTrue(
            str(s).startswith("quiz %d submission by testuser" % quiz.id))


class TestQuestionUserLock(TestCase):
    def test_create(self):
        s = Dummy()
        q = Dummy()
        q.quiz = Dummy()
        u = Dummy()
        qul = QuestionUserLock.create(s, q, u)
        self.assertIsNotNone(qul)

    def test_set_question_user_lock(self):
        s = CustomPagetreeModuleFactory()
        qul = QuestionUserLockFactory(section=s.root)
        self.assertIsNone(
            qul.set_question_user_lock(qul.question, None))
        qul.quiz = qul.question.quiz
        qul.save()
        self.assertIsNotNone(
            qul.set_question_user_lock(qul.question, None))

    def test_quiz_set_question_userlock(self):
        s = CustomPagetreeModuleFactory().root
        question = QuestionFactory()
        q = question.quiz
        u = UserFactory()
        q.set_question_userlock(s, question, u)

        r = q.get_random_question_set(s, None, None, None)
        self.assertTrue(len(r) > 0)

        q.unset_question_userlock(u)
        r = q.get_random_question_set(s, None, None, None)
        self.assertEqual(len(r), 0)

    def test_get_random_question_empty(self):
        q = QuizRandomFactory()
        self.assertIsNone(q.get_random_question(None, None, None))

    def test_get_random_question_no_userlock(self):
        s = CustomPagetreeModuleFactory().root
        question = QuestionFactory()
        q = question.quiz
        u = UserFactory()
        r = q.get_random_question(s, q, u)
        self.assertEqual(r, question)

    def test_get_random_question_with_userlock(self):
        s = CustomPagetreeModuleFactory().root
        question = QuestionFactory()
        q = question.quiz
        u = UserFactory()
        q.set_question_userlock(s, question, u)
        r = q.get_random_question(s, q, u)
        self.assertEqual(r, question)
