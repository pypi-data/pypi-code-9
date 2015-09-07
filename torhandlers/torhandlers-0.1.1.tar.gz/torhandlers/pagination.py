# -*- coding: utf-8 -*-
__author__ = 'Alex Bo'
__email__ = 'bosha@the-bosha.ru'

class Page:

    def __init__(self, pages_number, current_page, items_number):
        self.pages_number = pages_number
        self.current_page = current_page
        self.items_number = items_number

    def __len__(self):
        return self.items_number

    def __repr__(self):
        return '<Page %s of %s>' % (self.current_page, self.pages_number)

    def __iter__(self):
        self.itercounter = 0
        return self

    def __next__(self):
        if self.itercounter < self.pages_number:
            self.itercounter += 1
            return self.itercounter
        else:
            raise StopIteration

    @property
    def has_next(self):
        return True if self.current_page < self.pages_number else False

    @property
    def has_previous(self):
        return True if self.current_page != 1 else False

    @property
    def number(self):
        return self.current_page

    @property
    def current(self):
        return self.number

    @property
    def next_page_number(self):
        if self.has_next:
            return self.current_page + 1
        return None

    @property
    def previous_page_number(self):
        if self.has_previous:
            return self.pages_number - 1
        return None

    @property
    def as_dict(self):
        return {
            'has_next': self.has_next,
            'has_previous': self.has_previous,
            'next_page_number': self.next_page_number,
            'previous_page_number': self.previous_page_number,
            'items_number': self.items_number,
            'current_page': self.current_page,
            'pages_number': self.pages_number
        }
