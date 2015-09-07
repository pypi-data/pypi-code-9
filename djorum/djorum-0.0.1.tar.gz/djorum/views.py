from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth import get_user_model
# TODO: Remove user passes test mixin
from braces.views import UserPassesTestMixin

from djorum.models import Topic, Post, Reply
from djorum.forms import ReplyForm
User = get_user_model()


class TopicList(generic.ListView):
    context_object_name = 'topics'
    model = Topic
    template_name = 'djorum/index.html'


class TopicCreate(generic.CreateView):
    model = Topic
    fields = ['title', 'description', 'closed']
    template_name = 'djorum/new_topic.html'

    def form_valid(self, form):
        form = form.save(commit=False)
        form.creator = User.objects.get(id=self.request.user.id)
        form.save()
        topic = Topic.objects.get(slug=form.slug)
        messages.success(self.request, 'The topic %s was created!' % (topic,))
        return HttpResponseRedirect(reverse('djorum:topic_posts', args=(topic.slug,)))


class TopicUpdate(UserPassesTestMixin, generic.UpdateView):
    model = Topic
    fields = ['title', 'description', 'closed']
    template_name = 'djorum/topic_update_form.html'

    def form_valid(self, form):
        topic = Topic.objects.get(slug=self.kwargs['slug'])
        form = form.save(commit=False)
        if form.closed:
            messages.error(self.request, 'You have closed the topic %s!' % (topic,))
        if topic.closed and not form.closed:
            messages.success(self.request, 'You have reopened %s!' % (topic,))
        messages.success(self.request, 'The topic %s was updated!' % (topic,))
        form.save()
        return HttpResponseRedirect(reverse('djorum:topic_posts', args=(topic.slug,)))

    # TODO: test these 403s like with tribes
    def test_func(self, user):
        if Topic.objects.get(slug=self.kwargs['slug']).creator == user:
            return True
        else:
            raise PermissionDenied


class TopicDelete(UserPassesTestMixin, generic.DeleteView):
    model = Topic
    template_name = 'djorum/topic_confirm_delete.html'

    success_url = reverse_lazy('djorum:topics')

    def test_func(self, user):
        if Topic.objects.get(slug=self.kwargs['slug']).creator == user:
            return True
        else:
            raise PermissionDenied


class PostList(generic.ListView):
    context_object_name = 'posts'
    model = Post
    template_name = 'djorum/post_list.html'

    # TODO: investigate if this does anything
    def get_queryset(self):
        topic = Topic.objects.get(slug=self.kwargs['topic_slug'])
        return Post.objects.filter(topic=topic)

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        topic = Topic.objects.get(slug=self.kwargs['topic_slug'])
        context['topic'] = topic
        return context


class PostCreate(generic.CreateView):
    model = Post
    fields = ['title', 'body', ]
    template_name = 'djorum/new_post.html'

    def form_valid(self, form):
        form = form.save(commit=False)
        form.creator = User.objects.get(id=self.request.user.id)
        form.topic = Topic.objects.get(slug=self.kwargs['topic_slug'])
        form.save()
        post = Post.objects.get(slug=form.slug)
        messages.success(self.request, 'Post successful!')
        return HttpResponseRedirect(reverse('djorum:post', args=(post.topic.slug, post.slug,)))

    def get_context_data(self, **kwargs):
        context = super(PostCreate, self).get_context_data(**kwargs)
        topic = Topic.objects.get(slug=self.kwargs['topic_slug'])
        context['topic'] = topic
        return context


class PostDelete(UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = 'djorum/post_confirm_delete.html'

    def get_success_url(self, *args, **kwargs):
        return reverse('djorum:topic_posts', args=(self.kwargs['topic_slug'],))

    def test_func(self, user):
        if Post.objects.get(slug=self.kwargs['slug']).creator == user:
            return True
        else:
            raise PermissionDenied


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'djorum/post.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        post = Post.objects.get(slug=self.kwargs['slug'])
        context['post'] = post
        replies = Reply.objects.filter(post=post)
        context['replies'] = replies
        context['reply_form'] = ReplyForm()
        return context


def post_comment(request, topic_slug, post_slug):
    target_post = Post.objects.get(slug=post_slug)

    if request.method == 'POST':
        form = ReplyForm(request.POST)

        if form.is_valid():
            comment = Reply()
            comment.post = target_post
            comment.topic = target_post.topic
            comment.body = form.cleaned_data['body']
            comment.creator = request.user
            comment.user_ip = request.META['REMOTE_ADDR']

            comment.save()
            messages.success(request, 'Reply successful!')

            return HttpResponseRedirect(reverse('djorum:post', args=(topic_slug, post_slug)))


def comment_reply(request, topic_slug, post_slug, reply_to_slug):
    target_post = Post.objects.get(slug=post_slug)
    reply_to = Reply.objects.get(slug=reply_to_slug)

    if request.method == 'POST':
        form = ReplyForm(request.POST)

        if form.is_valid():
            reply = Reply()
            reply.post = target_post
            reply.topic = target_post.topic
            reply.body = form.cleaned_data['body']
            reply.creator = request.user
            reply.user_ip = request.META['REMOTE_ADDR']
            reply.parent = reply_to

            reply.save()
            messages.success(request, 'Reply successful!')

            return HttpResponseRedirect(reverse('djorum:post', args=(topic_slug, post_slug)))


def delete_reply(request, topic_slug, post_slug, reply_id):
    reply = Reply.objects.get(id=reply_id)

    if request.method == "POST":

        if request.user == reply.creator or request.user == reply.topic.creator:
            reply.delete()
            messages.success(request, 'Reply %s deleted!' % reply)
        return HttpResponseRedirect(request.GET.get('next'))
    else:
        messages.error(request, 'error')
        return HttpResponseRedirect(reverse('djorum:post', args=(topic_slug, post_slug)))
