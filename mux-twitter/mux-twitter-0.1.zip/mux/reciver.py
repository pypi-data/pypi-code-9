#!/usr/bin/env python

from twython import TwythonError, TwythonRateLimitError, TwythonAuthError
from twython import TwythonStreamer
from delorean import parse as parse_date
from asyncio import coroutine
import logging
import struct

log = logging.getLogger('epic-tweet.reciver')

class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        # https://dev.twitter.com/streaming/overview/messages-types
        # https://dev.twitter.com/overview/api/tweets
        log.debug(data)
        
        
        if 'friends' in data:
            #sent on inital connect
            return
            
        elif 'direct_message' in data:
            data = data['direct_message']
            msg_id = data['id']
            frm_id = data['sender_id']
            frm_name = data['sender_screen_name']
            to_id = data['recipent_id']
            to_name = data['recipent_screen_name']
            msg = data['text']
            created_at = parse_date(data['created_at']).epoch()

            log.info("Direct message:{} from {} ({}) to {} ({}): {}".format(msg_id, frm_name, frm_id, to_name, to_id, msg))
            

        # deletion messages
        # {'delete': {'status':{'id':432432, 'user_id':43234232}}}
        # also has id_str and user_id_str
        
        # location deletion messages
        # {'scrub_geo':{'user_id':4324323, 'up_to_status_id':342532432}}
        # _str keys as well
        elif 'scrub_geo' in data:
            uid = data['scrub_geo']['user_id']
            log.info("Got a geo scrub request for UID:{} however we do not use geo location data".format(uid))
        
        # limit notices - matched more than can be delivered
        # {'limit':{'track':3223}}
        # track is number of undelivered items
        # not implementing

        # status withheld messages
        # {'status_withheld': {'id':432432, 'user_id':43234232, 'withheld_in_countries':['US', 'AU']}}
        # not implementing

        # user withheld messages
        # {'user_withheld': {'id':43243243243, 'withheld_in_countries':['US', 'AU']}}
        # not implementing

        # disconnect
        # {'disconnect':{'code':3, 'stream_name':'', 'reason':''}}
        elif 'disconnect' in data:
            code = data['disconnect']['code']
            reason = data['disconnect']['reason']
            msg = {1: "Remote end shut down for internal administrative reasons",
                   2: "Too many connections from endpoint",
                   3: "control streams used to close stream",
                   4: "Client is reading too slowly, disconnecting",
                   5: "close stream sent by twitter client",
                   6: "Authentication token has been revoked",
                   7: "Connection limit hit, killing oldest connection (us)",
                   8: "twitter issue, shoudl never see this client side",
                   9: "Requested number of back fill messages exceeds buffer size",
                   10: "stream exception at remote end (twitter issue)",
                   11: "remote broker has stalled (twitter issue)",
                   12: "remote end is load shedding, OK for reconnect",
                   None: "Unknown error",
                   }.get(code)
            log.error("Recived disconect: {} - ({}) {}".format(msg, code, reason))
            # server closed connection, shut down our end as well and exit normmaly
            # client logic shoudl then reconnect
            self.disconnect()

        # stall warning
        # {"warning": {"code":"FALLING_BEHIND",
        #              "message":"msg here"
        #              "percent_full": 60 }
        # }
        elif 'warning' in data and data['warning']['code'] == 'FALLING_BEHIND':
            capacity = data['warning']['percent_full']
            msg = data['warning']['message']
            log.warn("Falling behind twitter, about to stall: serverside buffers at {}% - {}".format(capacity, msg))
        
        # event
        # {'target': USER, 'source': USER, 'event':'EVENT_NAME', 'target_object':TARGET_OBJECT, 'created_at':'Sat sep 3 00:00:00 +0000 2010'}
        # Description                         Event Name              Source             Target          Target Object
        # User deauthorizes stream            access_revoked          Deauthorizing user App owner       client_application
        # User blocks someone                 block                   Current user       Blocked user    Null
        # User removes a block                unblock                 Current user       Unblocked user  Null
        # User favorites a Tweet              favorite                Current user       Tweet author    Tweet
        # User’s Tweet is favorited           favorite                Favoriting user    Current user    Tweet
        # User unfavorites a Tweet            unfavorite              Current user       Tweet author    Tweet
        # User’s Tweet is unfavorited         unfavorite              Unfavoriting user  Current user    Tweet
        # User follows someone                follow                  Current user       Followed user   Null
        # User is followed                    follow                  Following user     Current user    Null
        # User unfollows someone              unfollow                Current user       Followed user   Null
        # User creates a list                 list_created            Current user       Current user    List
        # User deletes a list                 list_destroyed          Current user       Current user    List
        # User edits a list                   list_updated            Current user       Current user    List
        # User adds someone to a list         list_member_added       Current user       Added user      List
        # User is added to a list             list_member_added       Adding user        Current user    List
        # User removes someone from a list    list_member_removed     Current user       Removed user    List
        # User is removed from a list         list_member_removed     Removing user      Current user    List
        # User subscribes to a list           list_user_subscribed    Current user       List owner      List
        # User’s list is subscribed to        list_user_subscribed    Subscribing user   Current user    List
        # User unsubscribes from a list       list_user_unsubscribed  Current user       List owner      List
        # User’s list is unsubscribed from    list_user_unsubscribed  Unsubscribing user Current user    List
        # User updates their profile          user_update             Current user       Current user    Null
        # User updates their protected status user_update             Current user       Current user    Null
        # not implementing

        # normal status update
        elif 'id' in data:
            # this is a status update
            msg_id = data['id']
            user_id = data['user']['id']
            user_name = data['user']['screen_name']
            msg = data['text']
            created_at = parse_date(data['created_at']).epoch()
            reply_to = data['in_reply_to_status_id']
            mentions = data['entities']['user_mentions']
            formated_mentions = ['@{} ({})'.format(item['screen_name'], item['id']) for item in mentions]
            
            log.info("Msg:{} from {} ({}) to {}: {}".format(msg_id, user_name, user_id, formated_mentions, msg))

            self.pipe.append(data)
            self.eventfd.increment()

    def on_error(self, status_code, data):
        if status_code == 420:
            log.warn("Server has connected too many times for this user")

            raise TwythonRateLimitError(status_code, RATE_LIMIT_WARN_DELAY)
            
        elif status_code == 429:
            # Expected response:
            # { "errors": [ {"code": 88, "message": "Rate limit exceeded"} ] }
            log.warn("Recived rate limit warning")

            raise TwythonRateLimitError(status_code, RATE_LIMIT_WARN_DELAY)
            
        else:
            data = data.strip() # has a \r\n at the end of the output
            log.critical("Invalid request: (response_code: {}) {}".format(status_code, data))
            log.error("Disconnecting due to unknown response")
            self.disconnect()
            
            raise TwythonError("Received unknown response")
    
    def on_timeout(self):
        log.error("Could not connect, connection timed out")
        self.disconnect() # lib is not smart enough to bail out

        raise TwythonError()



def reciver(twitter, stream, out_pipe, eventfd):
    """ 
    out_pipe: the pipe to send indvidual tweets to for processing
    """
    log.info("Connecting to twitter")

    stream.pipe = out_pipe
    stream.eventfd = eventfd

    # grab posts we may have missed
    # normmaly this would be a background job 
    # but i dont want to introdcue the complexity atm
    # and i dont care if i miss an action or two from users
    # between the 'get messages' and 'connect to stream'
    log.info("Getting timeline")
    posts = twitter.get_mentions_timeline( # can return up to 800 items
                count=20,
                #since_id= ,  # grab everything newer than this post id
                trim_user=True, # we only want numerical ids, not full user info
                )

    log.info("Getting direct messages")
    direct_msgs = twitter.get_direct_messages( # can return up to 800 items
                    count=20,
                    #since_id= ,  # grab everything newer than this post id
                    trim_user=True, # we only want numerical ids, not full user info
                    )

    log.info("Streaming in status updates")
    stream.user(replies='all', # we want to see all replies, not just people we follow
                stall_warnings="true", # handy to know if the server is not catching up to the server
                retry_count=3,
                retry_in=60,
                )
    log.info("Connection was closed")
