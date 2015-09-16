import logging
from ghost import Ghost

g = Ghost(
    defaults=dict(
        wait_timeout=20,
    )
)


def snap():
    with g.start() as session:
        session.set_viewport_size(1024, 600)
        session.show()
        session.open('http://www.clubic.com')
        session.scroll_to_bottom()
        self.sleep(2)
        session.capture_to('test.png')

def scroll_to_bottom(self):
    x = self.main_frame.scrollPosition().x()
    y = 0
    height = self.page.viewportSize().height()

    while y + height < self.main_frame.contentsSize().height():
        y = y + height
        self.main_frame.scroll(x, y)
        self.sleep()
