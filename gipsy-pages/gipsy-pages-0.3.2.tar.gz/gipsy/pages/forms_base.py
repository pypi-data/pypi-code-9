#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


from gipsy.sections.forms_base import SectionAdminFormBase


class PageAdminFormBase(SectionAdminFormBase):
    def __init__(self, *args, **kwargs):
        super(PageAdminFormBase, self).__init__(*args, **kwargs)
        if 'title' in self.fields:
            self.fields['title'].help_text = "Title of a object - used in " \
                "templates as a <strong>headline</strong> and in meta title."
        if 'description' in self.fields:
            self.fields['description'].help_text = "Used in some templates as " \
                "<strong>lead copy</strong> and in meta description."
        if 'parent' in self.fields:
            self.fields['parent'].help_text = "Defines this pages place in page " \
                "tree structure. Parents are also used in composing URL of current page."
        if 'slug' in self.fields:
            self.fields['slug'].help_text = "Used as part of page URL. Contains " \
                "only letters, numbers, underscores or hyphens. Page URL is " \
                "composed of this and parent pages slugs. For example in URL: " \
                "/blog/new-technology/<strong>amazing-piece-of-tech</strong>/"
