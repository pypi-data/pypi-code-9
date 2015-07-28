import weakref
from threading import Thread

from npyscreen import (ActionForm, SplitForm, TitleText, Pager, notify_confirm, 
                       notify_yes_no, ButtonPress)
from twitter import Twitter, TwitterStream

from authentication import authenicate
from response import parse_tweet


class TweetForm(ActionForm, SplitForm):
    """This is the form that contains the feed, 
       including the fields to write a tweet
       and search and post."""

    QUIT_BUTTON_BR_OFFSET = (2, 21)
    QUIT_BUTTON_TEXT = 'Quit'

    SEARCH_BUTTON_BR_OFFSET = (2,13)
    SEARCH_BUTTON_TEXT = 'Search'
    
    TWEET_BUTTON_BR_OFFSET = (2,6)
    TWEET_BUTTON_TEXT = 'Tweet'

    BUTTONS_TEXT = [QUIT_BUTTON_TEXT, SEARCH_BUTTON_TEXT, TWEET_BUTTON_TEXT]
    BUTTONS_OFFSET = [QUIT_BUTTON_BR_OFFSET, SEARCH_BUTTON_BR_OFFSET, TWEET_BUTTON_BR_OFFSET]
    BUTTONS_DATA = zip(BUTTONS_TEXT, BUTTONS_OFFSET)

    def create(self):
        """initiliazes the form, adds the widgets and fires up the feed."""
        self.tweet = self.add(TitleText, name="What's happening?", 
                              use_two_lines=False, begin_entry_at=18)
        self.search = self.add(TitleText, name="Search", begin_entry_at=18)
        self.draw_line_at = 5
        self.nextrely += 4
        self.feed = self.add(Pager, ascii=False)
        
        # Since we don't have any ok botton we just do this, we want to
        # move all buttons at once
        ActionForm.move_ok_button = self.move_buttons
        
        # Populates the feed with the latest tweets
        self.populate()
        
        # Fires up the twitter stream so we can collect new tweets
        thread = Thread(target=self.stream)
        thread.daemon = True
        thread.start()
    
    
    # Had to override edit from ActionForm in order to add more buttons.
    # Basically just copied the code from ActionForm, cleaned up the code
    # a bit, added one more button and changed the name and positioning of 
    # the other buttons
    def edit(self):
        self._add_buttons()
        tmp_rely, tmp_relx = self.nextrely, self.nextrelx
       
        self.editing=True
        if self.editw < 0: self.editw=0
        if self.editw > len(self._widgets__)-1:
            self.editw = len(self._widgets__)-1
        if not self.preserve_selected_widget:
            self.editw = 0
    
        if not self._widgets__[self.editw].editable: 
            self.find_next_editable()
        
        self.display()

        while not self._widgets__[self.editw].editable:
            self.editw += 1
            if self.editw > len(self._widgets__)-2: 
                self.editing = False
                return False
        
        edit_return_value = None
        while self.editing:
            if not self.ALL_SHOWN: self.on_screen()
            try:
                self.while_editing(weakref.proxy(self._widgets__[self.editw]))
            except TypeError:
                self.while_editing()
            self._widgets__[self.editw].edit()
            self._widgets__[self.editw].display()
            
            self.handle_exiting_widgets(self._widgets__[self.editw].how_exited)
            
            if self.editw > len(self._widgets__)-1: 
                self.editw = len(self._widgets__)-1
            
            if self.tweet_button.value or self.search_button.value or self.quit_button.value:
                self.editing = False
        
            if self.search_button.value:
                self.search_button.value = False
                edit_return_value = self.on_search()
            elif self.tweet_button.value:
                self.tweet_button.value = False
                edit_return_value = self.on_tweet()
            elif self.quit_button.value:
                self.quit_button.value = False
                edit_return_value = self.on_quit()
         
        self.nextrely, self.nextrelx = tmp_rely, tmp_relx
        self.display()
        self.editing = False
        self._delete_buttons()
        return edit_return_value
     
    def _add_buttons(self):
        quit_button_text = self.QUIT_BUTTON_TEXT
        cmy, cmx = self.curses_pad.getmaxyx()
        cmy -= self.QUIT_BUTTON_BR_OFFSET[0]
        cmx -= len(quit_button_text)+self.QUIT_BUTTON_BR_OFFSET[1]
        self.quit_button = self.add_widget(self.OKBUTTON_TYPE, name=quit_button_text, 
                                           rely=cmy, relx=cmx, use_max_space=True)
        self.quit_button_pos = len(self._widgets__)-1
        self.quit_button.update()

        search_button_text = self.SEARCH_BUTTON_TEXT
        cmy, cmx = self.curses_pad.getmaxyx()
        cmy -= self.SEARCH_BUTTON_BR_OFFSET[0]
        cmx -= len(search_button_text)+self.SEARCH_BUTTON_BR_OFFSET[1]
        self.search_button = self.add_widget(self.OKBUTTON_TYPE, name=search_button_text, 
                                             rely=cmy, relx=cmx, use_max_space=True)
        self.search_button_pos = len(self._widgets__)-1
        self.search_button.update()        
        
        tweet_button_text = self.TWEET_BUTTON_TEXT
        my, mx = self.curses_pad.getmaxyx()
        my -= self.TWEET_BUTTON_BR_OFFSET[0]
        mx -= len(tweet_button_text)+self.TWEET_BUTTON_BR_OFFSET[1]
        self.tweet_button = self.add_widget(self.OKBUTTON_TYPE, name=tweet_button_text, 
                                            rely=my, relx=mx, use_max_space=True)
        self.tweet_button_pos = len(self._widgets__)-1
        self.tweet_button.update()

        self._added_buttons = [self.quit_button, self.search_button, self.tweet_button]
      
    def _delete_buttons(self):
        self.quit_button.destroy()
        self.search_button.destroy()
        self.tweet_button.destroy()
        del self._widgets__[self.tweet_button_pos]
        del self.tweet_button
        del self._widgets__[self.search_button_pos]
        del self.search_button
        del self._widgets__[self.quit_button_pos]
        del self.quit_button

    def on_tweet(self):
        post = self.tweet.value
        if len(post) == 0:
            notify_confirm('You can\'t post an empty tweet')
        elif len(post) > 140:
            notify_confirm('Your tweet is too long!', title='Error')
        elif notify_yes_no('Are you sure you want to post:\n' + post, title='Post'):
            self.post_tweet(post)
            self.tweet.value = ''

    def on_search(self):
        query = self.search.value
        if len(query) > 0:
            self.search_tweets(query)
        self.search.value = ''

    def on_quit(self):
        if notify_yes_no('Are you sure you wanna quit?', title='Quit'):
            exit()

    def post_tweet(self, post):
        twittr = Twitter(auth=authenicate())
        twittr.statuses.update(status=post)


    def update_feed(self, data):
        """Updates the feed, new tweets go first, the rest
           gets pushed down. The will at most contain the
           100 newest tweets.
           Returns the updated feed."""
        twit =  parse_tweet(data, self.max_x)
        feed = self.feed.values
        if twit: 
            for i, text in enumerate(twit):
                feed.insert(i,text)

        if len(self.feed.values) >= 1000:
            feed = feed[0:1000]
        return feed

    def populate(self):
        """Populates the the feed with the last 50 tweets from
           your feed when the client starts."""
        twittr = Twitter(auth=authenicate())
        tweets = reversed(twittr.statuses.home_timeline(count=50))

        for data in tweets:
            self.feed.values = self.update_feed(data)

    def stream(self):
        """Listens to your feed, and updates it whenever
           someone posts a new tweet."""
        twittr_stream = TwitterStream(auth=authenicate(), 
                                      domain='userstream.twitter.com')       
        #tweets = twittr_stream.user()

        for data in twittr_stream.user():
            self.feed.values = self.update_feed(data)

    def search_tweets(self, query):
        """Searches for tweets and adds them to the feed
           :param query: what you are searching for."""
        twittr = Twitter(auth=authenicate())
        tweets = twittr.search.tweets(q=query)
        tweets = reversed(tweets['statuses'])
        for data in tweets:
            self.feed.vaules = self.update_feed(data)   
    
    # Like edit, this function is supposed to override move_ok_button
    # from ActionForm. The code is more or less stolen from ActionForm, but
    # made some changes so it moves all 3 buttons
    def move_buttons(self):
        if hasattr(self, 'quit_button'):
            for button, data in zip(self._added_buttons, self.BUTTONS_DATA):
                text = data[0]
                offset = data[1]
                cmy, cmx = self.curses_pad.getmaxyx()
                cmy -= offset[0]
                cmx -= len(text) + offset[1]
                button.rely = cmy
                button.relx = cmx

