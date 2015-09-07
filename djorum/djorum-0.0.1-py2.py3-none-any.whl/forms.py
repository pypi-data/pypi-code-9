from django import forms

from djorum.models import Reply, ProfaneWord

# class PostForm(forms.ModelForm):
#
#     title = forms.CharField(max_length=60, required=True)
#
#     class Meta():
#         model = Post
#         exclude = ('creator','updated', 'created', 'closed', 'topic',)

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        exclude = ('creator', 'updated', 'created', 'topic', 'post', 'user_ip', 'parent')

    def clean_body(self):
        body = self.cleaned_data["body"]

        # TODO: hmm
        # if FORUM_FILTER_PROFANE_WORDS:
        #     profane_words = ProfaneWord.objects.all()
        #     bad_words = [w for w in profane_words if w.word in body.lower()]
        #
        #     if bad_words:
        #         raise forms.ValidationError("Bad words like '%s' are not allowed in posts." %
        #                                     (reduce(lambda x, y: "%s,%s" % (x, y), bad_words)))

        return body
