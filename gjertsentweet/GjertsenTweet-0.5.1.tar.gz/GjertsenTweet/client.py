import sys

from npyscreen import NPSAppManaged

from authentication import authenicate
from forms import TweetForm


class TwitterClient(NPSAppManaged):
    """This is the client. It only loads the
       form where you can post tweets, search, 
       and see your feed."""
    
    def onStart(self):
        self.addForm('MAIN', TweetForm, name='GjertsenTweet')


def main():
    authenicate()
    TwitterClient().run()
    return 0


if __name__ == '__main__':
    sys.exit(main())

