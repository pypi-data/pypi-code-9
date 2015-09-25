# -*- coding: utf-8 -*-
## -----------------------------------------------------------------
## Copyright (C)2013 ITYOU - www.ityou.de - support@ityou.de
## -----------------------------------------------------------------
"""
This module contains the postgres database interface
"""
import os
import logging
from time import time
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Unicode, DateTime
from sqlalchemy.orm import sessionmaker

from ityou.esi.theme import PSQL_URI
from config import TABLE_FOLLOWS, TABLE_LIKES

BASE = declarative_base()

class Follow(BASE):
    """ Follow Database
    uid: User Id of the follower
    fid: User Id of the following
    """
    __tablename__ = TABLE_FOLLOWS
    
    id              = Column(Integer, primary_key=True)
    uid             = Column(Unicode)
    fid             = Column(Unicode)

class Like(BASE):
    """Class for Vorting top/flop
       vote: 1 or -1
    """    
    __tablename__ = TABLE_LIKES
    
    id          = Column(Integer, primary_key=True)
    vote        = Column(Integer)
    uid         = Column(Unicode)
    sid         = Column(Unicode)
    timestamp   = Column(DateTime)


class DBApi(object):
    """ DB Util
    """
    def __init__(self):
        """Initialize Database
        """
        # --- psql ----------------------
        engine  = create_engine(PSQL_URI,  client_encoding='utf8', echo=False)

        self.session = sessionmaker(bind=engine)
        BASE.metadata.create_all(engine)
        
    def getFollowings(self, uid):
        """ Finds fids matching to the uid. This are the followings 
        of the user with uid.
        Return: list of fids
        """
        f = []
        try:
            se = self.session()
            q = se.query(Follow.fid).filter(Follow.uid == uid).all()
            for m in q:
                f.append(m[0])
        except:
            logging.error('Error while executing getFollowing')
        finally:
            se.close()

        return f
            
    def setFollowing(self, uid, fid, remove=False):
        """ Checks if there's an entry in DB with given uid and fid. 
        If there's none, it adds one.
        If remove=True is given, the function does the opportunity.
        Returns: True if action was successful, False if not
        """
        res = False
        try:
            se = self.session()
            q = se.query(Follow).filter(Follow.uid == uid, Follow.fid == fid)
            if not remove and not q.first():
                f = Follow(
                       uid = uid,
                       fid = fid
                       )
                se.add(f)
                se.commit()
                res = True
            elif remove and q.first():
                q.delete()
                se.commit()
                res = True
            else:
                se.close()
        except:
            logging.error('Error while executing setFollowing')
        finally:
            se.close()

        return res

            
    def getFollowers(self, fid):
        """ Given is the fid. Getting uids from DB where the fid matches. 
        This are the followers of the user (fid)
        Returns: list of uids
        """
        f = []

        try:
            se = self.session()
            q = se.query(Follow.uid).filter(Follow.fid == fid).all()
            for m in q:
                f.append(m[0])

        except:
            logging.error('Error while executing getFollowers')
        finally:
            se.close()

        return f        

    
    def isFollowing(self, uid, fid):
        """ Checks if user with uid is following the user with fid.
        Returns: True or False 
        """
        try:
            se = self.session()
            q = se.query(Follow).filter(
                Follow.uid == uid, 
                Follow.fid == fid).first()
        except:
            logging.error('Error while executing isFollowing')
        finally:
            se.close()

        if q:
            return True
        else:
            return False



    # ---- like/dislike ----------------------------------
    
    def vote(self, uid, sid, vote):
        """ Save vote into the DB
            uid: object uid
            sid: browser session id
            vote: 1 or -1
        """
        if vote not in [-1,1]:
            return None,None
        
        timestamp = datetime.now()
        
        vo = Like(
            uid = uid,
            sid = sid,
            vote = vote,
            timestamp = timestamp
            )
        
        try:
            se = self.session()
            q = se.query(Like).filter(Like.uid == uid).filter(Like.sid == sid)

            if q.count() == 0:
                se.add(vo)
                se.commit()
            elif q.count() == 1:                
                q.update({'vote':vote})
                se.commit()
            else:
                pass
        except:
            logging.error("Could not vote %s" % str(vo))
            return None, None
        finally:
            # return all votes
            se.close()
            
        se = self.session()
        qv = se.query(Like).filter(Like.uid == uid)
        qv_top  = qv.filter(Like.vote == 1).count()
        qv_flop = qv.filter(Like.vote == -1).count()
        se.close()
        
        return qv_top, qv_flop

   
    
    def getLikes(self, uid):
        """ returns the vote 
            uid: object uid
        """
        count = 0
        try:
            se = self.session()
            qv = se.query(Like).filter(Like.uid == uid)
            
            ## return all votes
            qv_top  = qv.filter(Like.vote == 1).count()
            qv_flop = qv.filter(Like.vote == -1).count()
        except:
            logging.error("Could not get votes of %s" % uid)
            return None,None
        finally:
            se.close()

        return qv_top, qv_flop


    def getAllLikes(self, sid):
        """ returns the vote on all own documents
            sid: User sid
        """
        count = 0
        try:
            se = self.session()
            qv = se.query(Like).filter(Like.sid == sid)
            
            ## return all votes
            qv_top  = qv.filter(Like.vote == 1).count()
            qv_flop = qv.filter(Like.vote == -1).count()
        except:
            logging.error("Could not get votes of %s" % sid)
            return None,None
        finally:
            se.close()

        return qv_top, qv_flop
                
