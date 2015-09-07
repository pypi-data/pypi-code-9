from django.contrib import admin

from .models import Topic, Post, Reply, ProfaneWord
# TODO: update

class TopicInline(admin.TabularInline):
    model = Topic
    extra = 0


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 0


class TopicAdmin(admin.ModelAdmin):
    list_display = ["title", "post_count", "creator", "created"]
    list_filter = ["creator", "created"]
    inlines = [PostInline]


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", 'topic', "reply_count", "creator", "created"]
    list_filter = ["creator", "created"]
    inlines = [ReplyInline]


class ReplyAdmin(admin.ModelAdmin):
    search_fields = ["body", "creator"]
    list_display = ["body", "post", "creator", "created"]


class ProfaneWordAdmin(admin.ModelAdmin):
    pass


admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(ProfaneWord, ProfaneWordAdmin)
