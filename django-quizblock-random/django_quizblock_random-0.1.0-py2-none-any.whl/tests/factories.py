import factory
from quizblock_random.models import Question, QuestionUserLock, QuizRandom
from pagetree.tests.factories import UserFactory
from pagetree.tests.factories import HierarchyFactory


class CustomPagetreeModuleFactory(object):
    def __init__(self):
        hierarchy = HierarchyFactory(name='main', base_url='/pages/')
        root = hierarchy.get_root()
        root.add_child_section_from_dict({
            'label': 'Welcome to the Intro Page',
            'slug': 'intro',
            'children': [
                {
                    'label': 'Step 1',
                    'slug': 'step-1',
                    'pageblocks': [{
                        'block_type': 'Text Block'
                    }]
                },
                {
                    'label': 'Step 2',
                    'slug': 'step-2',
                    'pageblocks': [{
                        'block_type': 'My Block Name'
                    }]
                },
            ]
        })

        self.root = root


class Dummy(object):
    id = 1


class QuizRandomFactory(factory.DjangoModelFactory):
    class Meta:
        model = QuizRandom

    quiz_name = "Random Quiz"
    quiz_type = "Random Quiz Type"


class QuestionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Question
    quiz = factory.SubFactory(QuizRandomFactory)


class QuestionUserLockFactory(factory.DjangoModelFactory):
    class Meta:
        model = QuestionUserLock

    quiz = factory.SubFactory(QuizRandomFactory)
    user = factory.SubFactory(UserFactory)
    question_used = True
    question_current = True
    question = factory.SubFactory(QuestionFactory)
