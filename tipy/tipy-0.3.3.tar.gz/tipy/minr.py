#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""The classes used for data mining.

Curently there is two data miners:
    - Corpus miner: mine from text files.
    - Facebook miner: mine from a facebook profile. In fact, this miner write
      the profile's posts into a file and then the file is mines the same way as
      a text corpus. That's why the two miners classes subclass the TextMiner
      class.

@todo 0.1.0:
    Implement the twitter miner which should be very similar to the facebook
    miner.
"""

from tipy.tknz import TextTokenizer
from tipy.db import SqliteDatabaseConnector, insert_ngrams
from os import system
from abc import ABCMeta, abstractmethod
try:
    from urllib.request import Request, urlopen
except ImportError:
    from urllib2 import Request, urlopen
from json import loads, dumps
from re import compile
from requests import request, HTTPError, get
from time import mktime
from datetime import datetime
from tipy.lg import lg


FB_CREATION_TIME = 1075852860
"""@var: Facebook creation date in unix time."""


# This class is taken from the facebook python sdk package.
# The facebook python sdk can't be build for python 3 so I modify it to make it
# compatible.
# See: https://facebook-sdk.readthedocs.org/
class GraphAPI(object):
    """A client for the Facebook Graph API.
    See http://developers.facebook.com/docs/api for complete
    documentation for the API.
    The Graph API is made up of the objects in Facebook (e.g., people,
    pages, events, photos) and the connections between them (e.g.,
    friends, photo tags, and event RSVPs). This client provides access
    to those primitive types in a generic way. For example, given an
    OAuth access token, this will fetch the profile of the active user
    and the list of the user's friends:
       graph = facebook.GraphAPI(access_token)
       user = graph.get_object("me")
       friends = graph.get_connections(user["id"], "friends")
    You can see a list of all of the objects and connections supported
    by the API at http://developers.facebook.com/docs/reference/api/.
    You can obtain an access token via OAuth or by using the Facebook
    JavaScript SDK. See
    http://developers.facebook.com/docs/authentication/ for details.
    If you are using the JavaScript SDK, you can use the
    get_user_from_cookie() method below to get the OAuth access token
    for the active user from the cookie saved by the SDK.
    """

    def __init__(self, access_token=None, timeout=None, version=None):
        # The default version is only used if the version kwarg does not exist.
        default_version = "2.0"
        valid_API_versions = ["2.0", "2.1", "2.2", "2.3"]

        self.access_token = access_token
        self.timeout = timeout

        if version:
            version_regex = compile("^\d\.\d$")
            match = version_regex.search(str(version))
            if match is not None:
                if str(version) not in valid_API_versions:
                    raise GraphAPIError("Valid API versions are " +
                                        str(valid_API_versions).strip('[]'))
                else:
                    self.version = "v" + str(version)
            else:
                raise GraphAPIError("Version number should be in the"
                                    " following format: #.# (e.g. 2.0).")
        else:
            self.version = "v" + default_version

    def get_object(self, id, **args):
        """Fetchs the given object from the graph."""
        return self.request(self.version + "/" + id, args)

    def get_objects(self, ids, **args):
        """Fetchs all of the given object from the graph.
        We return a map from ID to object. If any of the IDs are
        invalid, we raise an exception.
        """
        args["ids"] = ",".join(ids)
        return self.request(self.version + "/", args)

    def get_connections(self, id, connection_name, **args):
        """Fetchs the connections for given object."""
        return self.request(
            self.version + "/" + id + "/" + connection_name, args)

    def put_object(self, parent_object, connection_name, **data):
        """Writes the given object to the graph, connected to the given parent.
        For example,
            graph.put_object("me", "feed", message="Hello, world")
        writes "Hello, world" to the active user's wall. Likewise, this
        will comment on a the first post of the active user's feed:
            feed = graph.get_connections("me", "feed")
            post = feed["data"][0]
            graph.put_object(post["id"], "comments", message="First!")
        See http://developers.facebook.com/docs/api#publishing for all
        of the supported writeable objects.
        Certain write operations require extended permissions. For
        example, publishing to a user's feed requires the
        "publish_actions" permission. See
        http://developers.facebook.com/docs/publishing/ for details
        about publishing permissions.
        """
        assert self.access_token, "Write operations require an access token"
        return self.request(
            self.version + "/" + parent_object + "/" + connection_name,
            post_args=data,
            method="POST")

    def put_wall_post(self, message, attachment={}, profile_id="me"):
        """Writes a wall post to the given profile's wall.
        We default to writing to the authenticated user's wall if no
        profile_id is specified.
        attachment adds a structured attachment to the status message
        being posted to the Wall. It should be a dictionary of the form:
            {"name": "Link name"
             "link": "http://www.example.com/",
             "caption": "{*actor*} posted a new review",
             "description": "This is a longer description of the attachment",
             "picture": "http://www.example.com/thumbnail.jpg"}
        """
        return self.put_object(profile_id, "feed", message=message,
                               **attachment)

    def put_comment(self, object_id, message):
        """Writes the given comment on the given post."""
        return self.put_object(object_id, "comments", message=message)

    def put_like(self, object_id):
        """Likes the given post."""
        return self.put_object(object_id, "likes")

    def delete_object(self, id):
        """Deletes the object with the given ID from the graph."""
        self.request(self.version + "/" + id, method="DELETE")

    def delete_request(self, user_id, request_id):
        """Deletes the Request with the given ID for the given user."""
        self.request("%s_%s" % (request_id, user_id), method="DELETE")

    def put_photo(self, image, album_path="me/photos", **kwargs):
        """
        Upload an image using multipart/form-data.
        image - A file object representing the image to be uploaded.
        album_path - A path representing where the image should be uploaded.
        """
        return self.request(
            self.version + "/" + album_path,
            post_args=kwargs,
            files={"source": image},
            method="POST")

    def get_version(self):
        """Fetches the current version number of the Graph API being used."""
        args = {"access_token": self.access_token}
        try:
            response = request("GET",
                               "https://graph.facebook.com/" +
                               self.version + "/me",
                               params=args,
                               timeout=self.timeout)
        except HTTPError as e:
            response = loads(e.read())
            raise GraphAPIError(response)

        try:
            headers = response.headers
            version = headers["facebook-api-version"].replace("v", "")
            return float(version)
        except Exception:
            raise GraphAPIError("API version number not available")

    def request(
            self, path, args=None, post_args=None, files=None, method=None):
        """Fetches the given path in the Graph API.
        We translate args to a valid query string. If post_args is
        given, we send a POST request to the given path with the given
        arguments.
        """
        args = args or {}

        if post_args is not None:
            method = "POST"

        if self.access_token:
            if post_args is not None:
                post_args["access_token"] = self.access_token
            else:
                args["access_token"] = self.access_token

        try:
            response = request(method or "GET",
                               "https://graph.facebook.com/" +
                               path,
                               timeout=self.timeout,
                               params=args,
                               data=post_args,
                               files=files)
        except HTTPError as e:
            response = loads(e.read())
            raise GraphAPIError(response)

        headers = response.headers
        if 'json' in headers['content-type']:
            result = response.json()
        elif 'image/' in headers['content-type']:
            mimetype = headers['content-type']
            result = {"data": response.content,
                      "mime-type": mimetype,
                      "url": response.url}
        elif "access_token" in parse_qs(response.text):
            query_str = parse_qs(response.text)
            if "access_token" in query_str:
                result = {"access_token": query_str["access_token"][0]}
                if "expires" in query_str:
                    result["expires"] = query_str["expires"][0]
            else:
                raise GraphAPIError(response.json())
        else:
            raise GraphAPIError('Maintype was not text, image, or querystring')

        if result and isinstance(result, dict) and result.get("error"):
            raise GraphAPIError(result)
        return result

    def fql(self, query):
        """FQL query.
        Example query: "SELECT affiliations FROM user WHERE uid = me()"
        """
        return self.request(self.version + "/" + "fql", {"q": query})

    def get_app_access_token(self, app_id, app_secret):
        """Get the application's access token as a string."""
        args = {'grant_type': 'client_credentials',
                'client_id': app_id,
                'client_secret': app_secret}

        return self.request("oauth/access_token", args=args)["access_token"]

    def get_access_token_from_code(
            self, code, redirect_uri, app_id, app_secret):
        """Get an access token from the "code" returned from an OAuth dialog.
        Returns a dict containing the user-specific access token and its
        expiration date (if applicable).
        """
        args = {
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": app_id,
            "client_secret": app_secret}

        return self.request("oauth/access_token", args)

    def extend_access_token(self, app_id, app_secret):
        """
        Extends the expiration time of a valid OAuth access token. See
        <https://developers.facebook.com/roadmap/offline-access-removal/
        #extend_token>
        """
        args = {
            "client_id": app_id,
            "client_secret": app_secret,
            "grant_type": "fb_exchange_token",
            "fb_exchange_token": self.access_token,
        }

        return self.request("oauth/access_token", args=args)


class MinerRegistry(list):
    """List every "miner" classes to be used.

    MinerRegistry gather every miners to be used according to the configuration
    file. It provide methods to mine corpuses from different sources, using
    different processing strategies and store the results in different outputs.

    G{classtree MinerRegistry}
    """

    def __init__(self, config):
        """ Constructor of the MinerRegistry class.

        @param config:
            The configuration file. It is used to retrieve the miners classes
            names that will be added to the MinerRegistry.
        @type config: L{drvr.Configuration}
        """
        self.config = config
        self.set_miners()   # TODO: remove (never evaluated)

    def set_miners(self):
        """Add miner class(es) to the list according to the configuration.

        Retrieve the miners classes names from the configuration and try to
        add them to the list.
        """
        self[:] = []
        for miner in self.config.getas('MinerRegistry', 'miners', 'list'):
            self.add_miner(miner)

    def add_miner(self, minerName):
        """Try to add a miner class to the list using its name.

        Get the miner class name from the configuration and create an instance
        of this class if it exists, then, add the instance to the list.

        @param minerName:
            The name of the miner. It must correspond to a section of the
            configuration so that its miner class can be retrieved.
        @type minerName: str
        """
        try:
            minerClass = self.config[minerName]['class']
        except KeyError:
            print("Config file is incorrect. Check the miner key of the"
                  " %s section if exists or create it." % (minerName))
        if minerClass == 'CorpusMiner':
            miner = CorpusMiner(self.config, minerName)
        elif minerClass == 'FacebookMiner':
            miner = CorpusMiner(self.config, minerName)
        else:
            print('WARNING: miner class "%s" is unknown. miner won\'t be'
                  'added to the registry.' % minerName)
            miner = None
        if miner:
            self.append(miner)

    def mine(self):
        """Use the miner instances list to mine the sources.

        Loop through every miner instances of the list and call their mine()
        method to perform their mining operation.
        """
        for miner in self:
            miner.mine()

    def close_databases(self):
        """Close database of every miner instances using a database."""
        for miner in self:
            if callable(getattr(miner, "close_database", None)):
                miner.close_database()


class Miner(object):
    """Abstract class for all miners.

    G{classtree Miner}
    """

    __metaclass__ = ABCMeta

    def __init__(self, config=None, minerName='None', callback=None):
        self.config = config
        self.name = minerName
        self.callback = callback
        self.dbFile = self.config.getas(self.name, 'database')

    def rm_db(self):
        """Remove the database file (call os.system)."""
        system("rm %s" % (self.dbFile))

    @abstractmethod
    def mine(self):
        raise NotImplementedError("Method must be implemented")


class TextMiner(Miner):
    """The miner for text files.

    This miner mines text files by extracting valid n-grams from them and
    inserting them in databases. Mining a text require:
        - Tokenizing the text.
        - Extracting n-grams.
        - Inserting n-grams in a database in a special way.

    @see: L{TextTokenizer}, L{db.insert_ngrams}

    G{classtree TextMiner}
    """

    def __init__(self, config, minerName, callback=None):
        """Constructor of the FacebookMiner class.

        @param config:
            The configuration file. It is used to retrieve the miner parameters.
        @type config: L{drvr.Configuration}
        @param minerName:
            The name of the miner.
        @type minerName: str
        @param callback:
            The callback is used to show the progress percentage. In the gui a
            callback method is implemented to update a progress bar showing the
            n-grams insertion progress (cf. py).
        @type callback: fun(float, ...)
        """
        super().__init__(config, minerName, callback)
        self.lowercase = self.config.getas(self.name, 'lowercase')
        self.n = self.config.getas(self.name, 'n', 'int')

    def update_db(self, textPath):
        """Mine a text file, updating the database.

        @param textPath:
            The path to the text file to mine.
        @type textPath: str
        """
        for i in range(1, self.n + 1):
            self.add_to_db(self.crt_ngram_map(textPath, i), i, True)

    def crt_new_db(self, textPath):
        """Mine a text file.

        This method dosen't try to update the n-grams counts so it will fail if
        it tries to add an n-gram which is already in the database but this
        method is a little faster than update_db().

        @note: If you're intending to create a new database but it already
               exists please consider calling rm_db() first.

        @param textPath:
            The path to the text file to mine.
        @type textPath: str
        """
        for i in range(1, self.n + 1):
            self.add_to_db(self.crt_ngram_map(textPath, i), i, False)

    def crt_ngram_map(self, textPath, n):
        """Create a n-gram dictionary from a file.

        @param textPath:
            The path to the text file to mine.
        @type textPath: str
        @param n:
            The n in n-gram. Specify the maximum size of the n-grams to
            generate.
        @type n: int

        @return:
            The n-gram dictionary.
        @rtype: dict
        """
        lg.info("Parsing " + str(n) + "-grams from " + textPath)
        self.callback(0, 'parsing ' + str(n) + '-grams from ' + textPath)
        self.tokenizer = TextTokenizer(
            textPath, n, self.lowercase, 0, self.callback)
        ngramMap = self.tokenizer.tknize_text()
        lg.info(
            str(len(ngramMap)) + ' ngrams have been extracted from ' + textPath)
        return ngramMap

    def add_to_db(self, ngramMap, n, append=False):
        """Add n-grams of an n-gram dictionary to the database.

        @param ngramMap:
            The n-gram dictionnary returned by TextTokenizer.tknize_text().
            See the above-mentioned method docstring for more information.
        @type ngramMap: dict
        @param n:
            The n in n-gram. Specify the maximum size of the n-grams to
            generate.
        @type n: int
        @param append:
            Indicate weither the n-grams should be appened to the database.
        @type append: bool
        """
        lg.info("Writing result to " + self.dbFile)
        self.callback(0, 'writing ' + str(n) + '-grams to ' + self.dbFile)
        insert_ngrams(ngramMap, n, self.dbFile, append, True, self.callback)
        lg.info('n-grams successfully added to the database')


class CorpusMiner(TextMiner):
    """The miner for text corpus.

    This miner is basically a L{minr.TextMiner} wrapper that implement the
    mine() method which merely loops on every files of the corpus and call the
    L{minr.TextMiner.update_db} method to effectively do the mining operation.

    G{classtree CorpusMiner}
    """

    def __init__(self, config, minerName, callback=None):
        """Constructor of the CorpusMiner class.

        @param config:
            The configuration file. It is used to retrieve the miner parameters.
        @type config: L{drvr.Configuration}
        @param minerName:
            The name of the miner.
        @type minerName: str
        @param callback:
            The callback is used to show the progress percentage. In the gui a
            callback method is implemented to update a progress bar showing the
            n-grams insertion progress (cf. py).
        @type callback: fun(float, ...)
        """
        super().__init__(config, minerName, callback)
        self.callback = callback
        self.corpusFiles = self.config.getas(self.name, 'texts', 'list')

    def mine(self):
        """Perform the mining operation."""
        for text in self.corpusFiles:
            self.update_db(text)
        self.callback(100, 'Done')


class DictMiner(Miner):
    """A miner to mine dictionary-like files.

    This miner isn't a real miner as it only extract words from a
    dictionary-like file and insert them into a database.
    A dictionnary-like file is a file listing words, one word per line::
        about
        army
        bath
        boat
        ...

    G{classtree DictMiner}
    """

    def __init__(self, config, minerName, callback=None):
        """Constructor of the DictMiner class.

        @param config:
            The configuration file. It is used to retrieve the miner parameters.
        @type config: L{drvr.Configuration}
        @param minerName:
            The name of the miner.
        @type minerName: str
        @param callback:
            The callback is used to show the progress percentage. In the gui a
            callback method is implemented to update a progress bar showing the
            n-grams insertion progress (cf. py).
        @type callback: fun(float, ...)
        """
        super().__init__(config, minerName, callback)
        self.dictFile = self.config.getas(self.name, 'dictionary')
        self.database = self.config.getas(self.name, 'database')

    def mine(self):
        """Perform the mining operation.

        @note: This method could have used the update_db() method like the C
            orpusMiner and FbMiner do but this method avoid useless operations
            and is, therefore, faster.

        @todo 0.0.9:
            Make sure every lines of the file contain one single word (or none).
        """
        progress = 0
        sql = SqliteDatabaseConnector(self.database)
        sql.crt_ngram_table()
        with open(self.dictFile) as dictFile:
            for i, l in enumerate(dictFile):
                pass
        noLines = i + 1
        with open(self.dictFile) as dictFile:
            for word in dictFile:
                ngram = [word.strip('\n').lower()]
                oldCount = sql.ngram_count(ngram)
                if oldCount > 0:
                    sql.update_ngram(ngram, oldCount + 1)
                else:
                    sql.insert_ngram(ngram, 1)
                progress += 100 / noLines
                if self.callback:
                    self.callback(progress)
        sql.commit()
        sql.crt_index(1)
        sql.close_database()

    def insert_words(self):
        progress = 0
        sql = SqliteDatabaseConnector(self.database)
        sql.crt_ngram_table()
        with open(self.dictFile) as dictFile:
            for i, l in enumerate(dictFile):
                pass
        noLines = i + 1
        with open(self.dictFile) as dictFile:
            for word in dictFile:
                ngram = [word.strip('\n').lower()]
                oldCount = sql.ngram_count(ngram)
                if oldCount > 0:
                    sql.update_ngram(ngram, oldCount + 1)
                else:
                    sql.insert_ngram(ngram, 1)
                progress += 100 / noLines
                if self.callback:
                    self.callback(progress)
        sql.commit()
        sql.crt_index(1)
        sql.close_database()


class FacebookMiner(TextMiner):
    """The Facebook user profile miner.

    This miner use an access token to access a user facebook wall and retrieve
    its text message. While the messages's text is retrieve, the miner write
    them into a txt file. Once every messages have been write to the file the
    miner generate n-grams from the file and insert them in the database, using
    the L{minr.TextMiner} methods.

    G{classtree FacebookMiner}

    @note: The miner do not retrieve every facebook wall messages each time.
        When mining a facebook wall he saves the published date of the latest
        message and on next mining it will only retrieved the messages that have
        been published AFTER the saved date.
        See: L{minr.FacebookMiner.update_fb}

    @todo 0.2.0:
        Create web app in order to log the user to facebook and twitter,
        authenticate them and ask for permissions (if needed) and finaly get
        access token.
    """

    def __init__(self, config, minerName, callback=None):
        """Constructor of the FacebookMiner class.

        @param config:
            The configuration file. It is used to retrieve the miner parameters.
        @type config: L{drvr.Configuration}
        @param minerName:
            The name of the miner.
        @type minerName: str
        @param callback:
            The callback is used to show the progress percentage. In the gui a
            callback method is implemented to update a progress bar showing the
            n-grams insertion progress (cf. py).
        @type callback: fun(float, ...)
        """
        super().__init__(config, minerName, callback)
        self.fbFile = 'fb.txt'
        self.callback = callback
        self.accessToken = self.config.getas(self.name, 'accesstoken')
        self.previousLast = self.config.getas(self.name, 'last_update', 'int')

    def mine(self):
        """Perform the mining operation."""
        if not self.accessToken is None:
            try:
                jsonText = self.get_user_details()
                jsonText = loads(jsonText)
                userInfo = loads(jsonText)
            except TypeError:
                self.callback(0, 'error: Faebook access token is invalid')
                lg.error('Facebook access token is invalid')
                return
        else:
            self.callback(0, 'error: Faebook access token is missing')
            lg.error('Facebook access token is missing')
            return
        self.callback(0, 'Mining facebook user posts')
        PAGE_ID = userInfo['id']
        graph = GraphAPI(self.accessToken)
        profile = graph.get_object(PAGE_ID)
        posts = graph.get_connections(profile['id'], 'posts')
        self.update_fb(posts)
        self.update_db(self.fbFile)
        self.callback(100, 'Done')

    def write_to_file(self, post, fo):
        """Write a facebook post message to a file.

        @param post:
            A facebook post is a dictionary. If the post contains a textual
            message then it is associated to the 'message' key.
        @type post: dict
        @param fo:
            The file to write in.
        @type fo: TextIOWrapper
        """
        if "message" in post:
            fo.write(post['message'].encode('utf-8') + "\n".encode('ascii'))

    def scrap_fb(self, posts):
        """Fully mine every posts of a facebook profile.

        Mine the posts contained in the "posts" parameter (which should contains
        the latest posts) and keep requesting older posts until we reach the
        last post. If a post contains a textual message it is automatically
        written in the file at self.fbFile.
        The latest post unix time is computed and written in the config.

        @note: It is not possible to get every posts of a facebook profile in a
            single request (except if the profile contains very few posts).So
            The method must scan the "posts" dictionary and request the older
            posts until the request return a posts dictionary.

        @param posts:
            "posts" is returned by GraphAPI.get_connections(), it contains
            posts of a facebook profile.
        @type posts: dict
        """
        fo = open(self.fbFile, "wb")
        lastPostTime = ''
        while True:
            try:
                if lastPostTime == '':
                    lastPostTime = mktime(datetime.strptime(
                        posts['data'][0]['created_time'],
                        "%Y-%m-%dT%H:%M:%S+0000").timetuple())
                for post in posts['data']:
                    self.write_to_file(post, fo)
                posts = get(posts['paging']['next']).json()
            except KeyError:
                break
        fo.close()
        if lastPostTime:
            self.config[self.name]['LAST_UPDATE'] = \
                str(int(float(lastPostTime)))

    def update_fb(self, posts):
        """Mine posts of a facebook profile since the last mining operation.

        Mine the posts contained in the "posts" parameter (which should contains
        the latest posts) and keep requesting older posts until:
            - We reach a post that has already be mined (comparison is carried
              out using unix time and the 'last_update' config option)
            - We reach the last post of the facebook profile.
        If a post contains a textual message it is automatically written in
        the file at self.fbFile.
        The latest post unix time is computed and written in the config so that
        we know which posts have been published after this one the next time
        the method is called.

        @note: It is not possible to get every posts of a facebook profile in a
               single request (except if the profile contains very few posts).
               So The method must scan the "posts" dictionary and request the
               older posts until the request return a posts dictionary.

        @param posts:
            "posts" is returned by GraphAPI.get_connections(), it contains posts
            of a facebook profile.
        @type posts: dict
        """
        fo = open(self.fbFile, "wb")
        lastPostTime = ''
        stop = False
        if self.previousLast:
            previousLast = self.previousLast
        else:
            previousLast = FB_CREATION_TIME
        while True:
            try:
                if lastPostTime == '':
                    lastPostTime = mktime(datetime.strptime(
                        posts['data'][0]['created_time'],
                        "%Y-%m-%dT%H:%M:%S+0000").timetuple())
                    diff = lastPostTime - previousLast
                else:
                    try:
                        # not very regular, particularly on first mining
                        self.callback(float(100 * previousLast / mktime(
                            datetime.strptime(
                                posts['data'][0]['created_time'],
                                "%Y-%m-%dT%H:%M:%S+0000").timetuple())))
                    except IndexError:
                        pass
                for post in posts['data']:
                    postTime = mktime(datetime.strptime(
                        post['created_time'],
                        "%Y-%m-%dT%H:%M:%S+0000").timetuple())
                    if postTime > previousLast:
                        self.write_to_file(post, fo)
                    else:
                        stop = True
                        break
                if stop:
                    break
                posts = get(posts['paging']['next']).json()
            except KeyError:
                break
        fo.close()
        if lastPostTime:
            self.config[self.name]['last_update'] = \
                str(int(float(lastPostTime)))

    def get_user_details(self):
        """Use the facebook access token to get details about the user.

        @return:
            The user details or an empty dictionary if the request fail wich
            probably means that the access token is invalid or outdated.
        @rtype: dict
        """
        jDict = {}
        url = "https://graph.facebook.com/me?access_token=" + self.accessToken
        try:
            response = urlopen(Request(url))
            jDict = dumps(response.read().decode('utf-8'))
        except Exception:
            pass
        return jDict

    def rm_db(self):
        """Override the parent method.

        This method delete the database file and also set the last_update option
        of the facebook miner to the oldest value possible so that the facebook
        account will be fully scraped on next mining operation.
        """
        system("rm %s" % (self.dbFile))
        self.config['FbMiner']['last_update'] = str(FB_CREATION_TIME)
