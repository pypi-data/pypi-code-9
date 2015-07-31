#!/usr/bin/python
# -*- coding:utf-8 -*-

__author__ = 'Waner <wanernet@qq.com>'
__all__ = ["Paginator", "PageItem"]


class Paginator(object):
    def __init__(self, current, total_records=0, page_size=10, display_certain_size=5):
        """ 分页
        :param total_records: 总记录数
        :param page_size: 每页数量
        :param display_certain_size: 分页显示数
        :return:
        """
        self.total_records = total_records  # 总条数
        self.page_size = page_size
        self.display_certain_size = display_certain_size if display_certain_size % 2 > 0 else display_certain_size - 1
        # 总页数
        self.total_pages = self.total_records // self.page_size + (1 if self.total_records % self.page_size > 0 else 0)
        self.current = current if self.total_pages > current else self.total_pages
        self.data = []  # 分页数据
        self.__judge__()

    def __judge__(self):
        if self.total_records > self.page_size:
            self.offsetSize = (self.display_certain_size - 1) / 2  # 边界尺寸
            self.offsetRight = self.total_pages - self.current
            self.offsetLeft = (self.offsetSize - self.current) * -1
            self.startWith = max(self.offsetLeft, 1) if self.offsetRight >= self.offsetSize else max(
                (self.offsetLeft - self.offsetSize + self.offsetRight), 1)
            _count = self.display_certain_size if self.total_pages >= self.display_certain_size else self.total_pages

            for i in range(0, _count):
                self.data.append(PageItem(i + self.startWith, self.total_pages))

        else:
            self.total_pages = 1
            self.data.append(PageItem(1, 1))


class PageItem(object):
    def __init__(self, current=1, total_pages=0):
        """ 分页信息
        :param current: 当前页码
        :param total_pages: 总页数
        :return:
        """
        self.current = current
        self.has_next = self.current < total_pages
        self.has_prev = self.current > 1


if __name__ == "__main__":
    p = Paginator(2, 10, 15, 10)
    print p.current
    print p.total_pages
    print p.display_certain_size
    for l in p.data:
        print "current:%s,prev:%s,next:%s" % (l.current, l.has_prev, l.has_next )

    pass