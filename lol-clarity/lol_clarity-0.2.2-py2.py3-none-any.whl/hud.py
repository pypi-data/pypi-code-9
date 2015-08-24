class Vec2(object):
    def __init__(self, x, y):
        self.x = x or 0.0
        self.y = y or 0.0

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.x == other.x
            and self.y == other.y)

class Rect(object):
    def __init__(self, start, end):
        assert isinstance(start, Vec2)
        assert isinstance(end, Vec2)
        self.start = start
        self.end = end

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.start == other.start
            and self.end == other.end)


class LolRect(Rect):
    def __init__(self, start, end, res_w, res_h):
        super(LolRect, self).__init__(start, end)
        assert isinstance(res_w, Vec2)
        assert isinstance(res_h, Vec2)
        self.res_w = res_w
        self.res_h = res_h

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.start == other.start
            and self.end == other.end
            and self.res_w == other.res_h
            and self.res_h == other.res_h)

def get_abs_scaled_rect(rect):
    assert isinstance(rect, LolRect)
    return Rect(
        Vec2(
            rect.start.x / rect.res_w,
            rect.start.y / rect.res_h
        ),
        Vec2(
            rect.end.x / rect.res_w,
            rect.end.y / rect.res_h
        )
    )

def get_lol_scaled_rect(rect, res_w, res_h):
    assert isinstance(rect, Rect)
    return LolRect(
        Vec2(
            rect.start.x * res_w,
            rect.start.y * res_h
        ),
        Vec2(
            rect.end.x * res_w,
            rect.end.y * res_h
        ),
        res_w, res_h
    )
