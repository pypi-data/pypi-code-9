from django import forms
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from pagetree.models import Section
from quizblock.models import Quiz, Question, Submission
from random import randint


class QuizRandom(Quiz):
    display_name = "Quiz Random"
    template_file = "quizblock_random/quizblock_random.html"
    quiz_name = models.CharField(max_length=50)
    quiz_type = models.TextField(blank=True)

    def get_random_question(self, section, quiz, user):
        question_set = self.question_set.all()
        set_len = len(question_set)
        if set_len > 0:
            rand_int = randint(0, set_len-1)
            for question in question_set:
                try:
                    current_question = QuestionUserLock.objects.filter(
                        quiz_id=question.quiz.id
                    ).get(
                        question_current=True,
                        user_id=user.id)
                    qid = current_question.question_id
                    question = Question.objects.get(id=qid)
                    return question

                except QuestionUserLock.DoesNotExist:
                    question = question_set[rand_int]
                    self.set_question_userlock(section, question, user)
                    return question
        else:
            return

    def set_question_userlock(self, section, question, user):
        qul = QuestionUserLock.create(section, question, user)
        qul.question_current = True
        qul.question_used = False
        qul.save()

    def get_random_question_set(self, section, block, question, user):
        question_set = QuestionUserLock.objects.filter(section_id=section.id)
        return question_set

    def pageblock(self):
        return self.pageblocks.all().first()

    def quiz(self):
        return self.quiz.all()[0]

    def clear_user_submissions(self, user):
        self.unset_question_userlock(user)
        Submission.objects.filter(user=user, quiz=self).delete()

    def unset_question_userlock(self, user):
        QuestionUserLock.objects.filter(user=user, quiz=self).delete()

    def edit(self, vals, files):
        self.quiz_type = vals.get('quiz_type', '')
        self.description = vals.get('description', '')
        self.rhetorical = vals.get('rhetorical', '')
        self.allow_redo = vals.get('allow_redo', '')
        self.show_submit_state = vals.get('show_submit_state', False)
        self.save()

    def edit_form(self):
        class EditForm(forms.Form):
            quiz_type = forms.CharField(widget=forms.widgets.Textarea(),
                                        initial=self.quiz_type)
            description = forms.CharField(widget=forms.widgets.Textarea(),
                                          initial=self.description)
            rhetorical = forms.BooleanField(initial=self.rhetorical)
            allow_redo = forms.BooleanField(initial=self.allow_redo)
            show_submit_state = forms.BooleanField(
                initial=self.show_submit_state)
            alt_text = (
                "<a href=\"" + reverse("edit-quiz-random", args=[self.id])
                + "\">manage questions/answers</a>")
        return EditForm()

    def get_question(self):
        return

    @classmethod
    def add_form(self):
        class AddForm(forms.Form):
            quiz_type = forms.CharField(widget=forms.widgets.Textarea())
            description = forms.CharField(widget=forms.widgets.Textarea())
            rhetorical = forms.BooleanField()
            allow_redo = forms.BooleanField()
            show_submit_state = forms.BooleanField(initial=True)
        return AddForm()

    @classmethod
    def create(self, request):
        return QuizRandom.objects.create(
            quiz_type=request.POST.get('quiz_type', ''),
            description=request.POST.get('description', ''),
            rhetorical=request.POST.get('rhetorical', ''),
            allow_redo=request.POST.get('allow_redo', ''),
            show_submit_state=request.POST.get('show_submit_state', False))


class QuestionUserLock(models.Model):
    section = models.ForeignKey(Section,)
    quiz = models.ForeignKey(QuizRandom)
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    question_used = models.NullBooleanField(null=True)
    question_current = models.NullBooleanField(null=True)

    def set_question_user_lock(self, question, user):
        try:
            current_question = QuestionUserLock.objects.filter(
                quiz_id=question.quiz.id).get(question_current=True)
            qid = current_question.question_id
            question = Question.objects.get(id=qid)
            return question
        except QuestionUserLock.DoesNotExist:
            return None

    @classmethod
    def create(self, section, question, user):
        return QuestionUserLock.objects.create(
            section_id=section.id,
            quiz_id=question.quiz.id,
            question_id=question.id,
            user_id=user.id
            )
