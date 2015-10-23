# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
import functools
import six
import string
import re
import collections
import uuid
import copy

from random import SystemRandom

import arrow

from suds.servicedefinition import WebFault
from suds.client import MethodNotFound

try:
    from functools import lru_cache
except ImportError:
    from functools32 import lru_cache

from .portal import Portal, TransportError, TLSError
from .replay import Replay
from .utils import notimplemented
from .exceptions import BaseError

random = SystemRandom()

__all__ = ['User', 'Error', 'DoesNotExist', 'TLSError']

logger = logging.getLogger(__name__)


class Error(BaseError):
    pass


class DoesNotExist(Error):
    def __init__(self, *args, **kwargs):
        super(DoesNotExist, self).__init__(*args, **kwargs)
        self.message = "The user was not found on the VidyoPortal"


PortalVersionInfo = collections.namedtuple(
    'PortalVersionInfo',
    ('maj', 'min', 'micro', 'patch', 'db')
)


def _vidyo_service(method, api_attr, val):
    """
    Method decorator to avoid cryptic errors when functions requiring a
    particular Vidyo WS API call are not available
    """
    @functools.wraps(method)
    def wrapped(obj, *args, **kwargs):
        if getattr(obj, api_attr, None) != val:
            msg = 'ProgrammingError: "%s" `api_type` required for %s' % (val, method)
            logger.exception(msg)
            raise AttributeError(msg)
        return method(obj, *args, **kwargs)
    return wrapped


def _userservice(method):
    """Method decorator requiring Vidyo user API"""
    return _vidyo_service(method, 'api_type', 'user')


def _adminservice(method):
    """method decorator requiring Vidyo admin API"""
    return _vidyo_service(method, 'api_type', 'admin')


@six.python_2_unicode_compatible
class User(object):
    """
    The Vidyo user class implements user and conference related RPC functionality.
    """

    # endpoint statuses
    USER_OFFLINE = 0
    USER_BUSY = 1
    USER_IDLE = 2

    def __init__(self, host, user=None, password=None, member=None,
                 api_type='user', ssl=True):
        """
        ``host``: string of the portal hostname.
        ``member`` a `member.PortalMember`` object associated with the user.
            This is required for admin operations.

        Valid kwargs are:
            ``user``: RPC username
            ``password``: RPC password
            ``api_type``: RPC type. The Vidyo API is separated into user and
                admin functionality, and they each have very different functionality.
                valid values are ``('user', 'admin')``; defaults to `'admin'` if not
                given.
            ``ssl``: Boolean - whether to use an HTTPS connection in RPC (default `True`).
                This also enforces that audio and video streams are encrypted in
                conference.
        """
        self._admin_service = None
        self._user_service = None
        self._password = password
        self.member = member
        self.portal = Portal(host, user=user, password=password, api_type=api_type, ssl=ssl)

        # make sure that we separate admin/user interfaces so we use the right RPC
        if self.portal.api_type == 'admin':
            self._admin_service = self.portal.service
            self.api_type = 'admin'
        elif self.portal.api_type == 'user':
            self._user_service = self.portal.service
            self.api_type = 'user'
        else:
            raise Error("Given neither user or admin role")

    @lru_cache()
    def entity_id(self):
        """
        Get the account ID from the Portal. A non-negative integer.
        """
        # History lesson:
        # Vidyo's createMember() admin API function returns the string 'OK'
        # on success. On failure an exception is raised. Pretty much every other
        # function call in both admin and user RPC APIs
        # requires the entityID value that *should* have been returned from
        # createMember. It's a totally stupid situation and means we have to use
        # the following ugliness to determine the ``entity_id`` used everywhere.
        try:
            try:
                if self.member:
                    if self.member.memberID:
                        return int(self.member.memberID)
            except AttributeError:
                pass

            if self.portal.api_type == 'user':
                return int(self._my_account().entityID)

            if self.portal.api_type == 'admin':
                filt = self.portal.client.factory.create('Filter')
                filt.query = self.username()
                resp = self._admin_service.getMembers(filt)
                logger.debug('VidyoPortal getMembers()%s', resp)

                try:
                    for memb in resp.member:
                        if memb.name == filt.query:
                            self.member.memberID = int(memb.memberID)
                            return self.member.memberID
                except AttributeError as e:
                    logger.exception(e)
                    raise DoesNotExist()

            return int(self.member.memberID)
        except WebFault as e:
            logger.exception(e)
            raise TransportError(e)
        except AttributeError as e:
            raise DoesNotExist()

    @_adminservice
    def delete(self):
        """delete the user from the VidyoPortal"""
        logger.info('deleting user %r', self.entity_id())
        try:
            self._admin_service.deleteMember(self.entity_id())
            self.entity_id.cache_clear()
            self._login_info.cache_clear()
            self._my_account.cache_clear()
            try:
                self.member.memberID = None
            except AttributeError:
                pass
        except WebFault:
            # WebFault is as specific as we can be here because the Vidyo
            # 'Exception' type is only valid for the User API so we rely on suds
            # unmarshalling an HTTP 500 into WebFault instead.
            # It's like catching BaseException.
            raise Error('deletion failed')

    @_adminservice
    def create(self):
        """
        Register the new user on the VidyoPortal.
        Can fail for multiple reasons including duplicate id on the portal.
        Returns entity_id on success, a unique non-negative integer used by the
        portal as a user id.
        """
        logger.info('creating member %r', self.member)
        try:
            self._admin_service.addMember(dict(self.member))
        except WebFault as e:
            raise Error('user creation failed:%s' % e)
        return self.entity_id()

    @_adminservice
    def update(self, **kwargs):
        """synchronize the user information on the VidyoPortal to self.member"""
        member = copy.copy(self.member)
        member.update(**kwargs)
        self._admin_service.updateMember(memberID=self.entity_id(), member=dict(member))
        # update internal parameters only on success
        self.member = member

    @_userservice
    def activate_endpoint(self, endpoint_id, poll_status=False):
        """
        Request that the endpoint identified by `endpoint_id` is activated so that
        it may subsequently join a call. This initiates communication between the
        client and the router.

        `endpoint_id` is a string of the serial number of the installed viydo client.

        It can be retrieved from vidyodesktop over HTTP and in JavaScript and C, by
        sending a REQUEST_EID message to the client.
        """
        endpoint_id = endpoint_id.lstrip('eid=')
        logger.debug("activate endpoint %s:%r", self, endpoint_id)
        status = self.status()
        # TODO loop until status change if `poll_status` is True
        try:
            self._user_service.linkEndpoint(endpoint_id)
        except WebFault as e:
            logger.exception("couldn't link endpoint with status=%s:%s", status, e)
            raise Error(str(e))

    @_userservice
    def join_room(self, room_owner, endpoint_id=None, pin=None, room_id=None, guest=True):
        """
        join another user's conference room. If ``room_id is None``, joins the
        user's default room, otherwise joins the room with the given ``room_id``.
        If ``endpoint_id`` is given, activate the endpoint and wait for the status
        change before joining the room. This is required when using the default
        desktop client, as there are no status-change notification API.
        """
        logger.debug(
            "join room(%r, %r, %r, %r)", self, room_owner, endpoint_id,
            {'pin': pin, 'room_id': room_id, 'guest': guest}
        )
        # TODO check whether that room belongs to that user
        room_owner = room_id or room_owner.entity_id()
        if endpoint_id:
            self.activate_endpoint(endpoint_id,)

        try:
            if pin:
                self._user_service.joinConference(conferenceID=room_owner, PIN=str(pin))
            else:
                self._user_service.joinConference(conferenceID=room_owner)
        except WebFault as e:
            # clients can be left logged in. We probably don't want that.
            logger.exception(
                "couldn't start conference:%s,%s,%s,%s,%s - %s",
                room_owner, endpoint_id, pin, room_id, guest, e
            )
            if not guest:
                self.log_out()
            raise Error("could not start conference - endpoint is not connected")

    @_userservice
    def join_room_and_lock(self, room_owner, endpoint_id, **kwargs):
        """
        Join a conference and lock it to prevent others from joining.
        There is obviously a pretty easy timing attack here, but Vidyo's API
        provides no way to do the joining and locking as an atomic operation.
        """
        room_owner._user_service.unlockRoom(
            kwargs.get('room_id') or room_owner.entity_id(),
            kwargs['pin']
        )
        self.join_room(room_owner, endpoint_id, **kwargs)
        room_owner._user_service.lockRoom(room_owner.entity_id())

    def secure_all_rooms(self, room_ids=None, pin=None):
        """
        Make a reasonable attempt to prevent others from joining a room casually.
        A pin is added for all rooms.
        """
        if self.api_type == 'admin':
            service = self._admin_service
        else:
            service = self._user_service
        if room_ids is not None:
            if not hasattr(room_ids, '__iter__'):
                rooms = (room_ids,)
        else:
            rooms = self.all_room_ids()
        for room_id in rooms:
            service.removeRoomURL(room_id)
            # VidyoPortal only accepts digital pins
            # `PIN` should be a 3-10 digit number':Exception from portal
            if pin and str(pin).isdigit():
                service.createRoomPIN(room_id, str(pin))
                service.createModeratorPIN(room_id, str(pin))

    @_userservice
    def create_private_room(self, extension_prefix):
        """
        Create a new room with a randomly generated PIN for the current user.
        """
        room_name = ''.join(random.choice(string.ascii_letters) for x in range(16))
        pin = random.randint(100, 9999999999)

        # It's unlikely that we'll see a collision (for fair values of unlikely)
        # but the extension is the weak point at maximum 53 bits of entropy, the
        # probability of a collision is about 1e-9 at 10000 existing users.
        # Apart from unreliably parsing the exception message, there's
        # no real way of telling what went wrong, so we just have to raise a base `Error`.
        try:
            extension = "%s%s" % (extension_prefix, random.randint(0, 9999999999999))
            room = self._user_service.createRoom(room_name, extension)
        except WebFault as e:
            logger.exception("failed to createRoom: '%s'", e)
            raise Error(e)

        try:
            self._user_service.createRoomPIN(room.entityID, pin)
        except WebFault as e:
            logger.exception("Couldn't create PIN for new room. Trying to delete")
            self._user_service.deleteRoom(room.entityID)
            raise Error(e)

        url = six.moves.urllib_parse.urlparse(room.RoomMode.roomURL)
        return {
            'room_name': room_name,
            'room_url': room.RoomMode.roomURL,
            'extension': extension,
            'pin': pin,
            'room_id': room.entityID,
            'key': six.moves.urllib_parse.parse_qs(url.query)['key'][0]
        }

    @_userservice
    def _room_ids_user(self):
        """The VidyoPortalUserService has no `getRooms` call, and the admin API
        returns an entirely different kind of object. It's best just to factor the
        two out.
        """
        f = self.portal.client.factory.create('Filter')
        f.EntityType = 'Room'
        entity_id = self.entity_id()
        # VidyoPortalUserService provides no getRooms call.
        rooms = self._user_service.searchByEntityID(self.entity_id())

        if not rooms.total:
            return []
        entity_id = self.entity_id()
        # The filtered search is pretty general so we need to check the ownerID for every element.
        # Don't ask me why an array membername is uppercase singular here,
        # but lowercase in the admin `getRooms` function
        return [
            room.entityID for room in getattr(rooms, 'Entity', [])
            if int(room.ownerID) == entity_id
        ]

    @_adminservice
    def _room_ids_admin(self):
        """get a list of entity ids for rooms owned by this user, or (empty)"""
        filt = self.portal.client.factory.create('Filter')
        filt.query = self.username()
        rooms = self._admin_service.getRooms(filt)

        return [int(r.roomID) for r in getattr(rooms, 'room', [])]

    @lru_cache()
    def all_room_ids(self):
        if self.api_type == 'admin':
            return self._room_ids_admin()
        return self._room_ids_user()

    def delete_all_rooms(self):
        if self.api_type == 'admin':
            service = self._admin_service
        else:
            service = self._user_service

        for room in self.all_room_ids():
            # Trying to delete the base room causes the portal to freak out.
            try:
                if int(room) != self.entity_id():
                    logger.info("deleting room %s", room)
                    service.deleteRoom(room)
            finally:
                self.all_room_ids.cache_clear()

    def delete_room(self, room_id=None):
        """
        Purges an extra virtual VidyoRoom from the VidyoPortal. Cannot delete
        the room with the ``id == entityID``
        """
        logger.info("deleting room %s", room_id)
        service = self._admin_service or self._user_service
        # Can't remove the last room
        if room_id:
            if int(room_id) == self.entity_id():
                logger.exception('VidyoRoom deletion cannot act on base room')
                raise Error("can't delete user's base room")
            else:
                service.deleteRoom(room_id)
                self.all_room_ids.cache_clear()
        else:
            raise NotImplementedError("Can't delete room; not implemented")

    def owns_room(self, room_id):
        """determine if self owns the given roomID"""
        return room_id in self.all_room_ids()

    @_userservice
    def leave_room(self, room_id=None, kick_users=True, pin=None):
        """
        Attempts to elbow a user out of a given conference.
        If ``logout==True``, the Vidyo Endpoint is deauthenticated after leaving
        the conference.
        If it is the user's own room, all will be removed from the conference.
        Thanks to Vidyo's 'unique' handling of their API development,
        you have to search through all members in a conference to get the unique
        participantID value required to leave a conference.
        More ugly code follows.
        """
        if room_id is None:
            # portal > v3 call only
            try:
                room_id = self._user_service.getConferenceID()
            except MethodNotFound:
                # portal < v3 has no way to determine this
                room_id = self.entity_id()
            except WebFault:
                # Assume unable to get conferenceID which means there is no conference
                logger.warn("Tried to end nonexistent conference")
                return

        if kick_users and self.owns_room(room_id):
            # only the owner can kick other users.
            try:
                try:
                    if pin:
                        self._user_service.disconnectConferenceAll(room_id, pin)
                        logger.debug("disconnectConferenceAll(%s) with pin %s", room_id, pin)
                    else:
                        self._user_service.disconnectConferenceAll(room_id)
                        logger.debug("disconnectConferenceAll(%s) without pin", room_id)
                except WebFault:
                    pass
            except MethodNotFound:
                # portal >= v3 call only
                parties = self._user_service.getParticipants(room_id, '').Entity
                if parties.total:
                    users = parties.Entity
                    for user in users:
                        self._user_service.leaveConference(user.ownerID, user.participantID)
            return
        else:
            try:
                parties = self._user_service.getParticipants(room_id, '').Entity
            except AttributeError:
                # When there are no parties in the conference, the returned obj
                # doesn't have the entity member. This is very irritating.
                return
            for user in parties:
                if int(user.entityID) == self.entity_id():
                    self._user_service.leaveConference(room_id, user.participantID)

    @_userservice
    def log_out(self):
        """
        Invalidate endpoint sessions, and exits conferences.
        """
        # Somewehere between 3.0 and 3.1 Vidyo changed the behaviour of
        # logOut() to do the following:
        # [...]
        # That's right;  If a user is in a conference at the time logOut() is
        # called, it will be ignored.
        # To end a conference we must call User.leave_room()
        self.leave_room()
        self._user_service.logOut()
        try:
            self._user_service.logoutAllOtherSessions()
        except MethodNotFound:
            pass
        self._login_info.cache_clear()

    @lru_cache()
    @_userservice
    def _my_account(self):
        my_acc = self._user_service.myAccount()
        logger.debug('VidyoPortal myAccount()%s', my_acc)
        return my_acc

    @lru_cache()
    def portal_version_string(self):
        """raw version string as returned by the portal"""
        try:
            ver = self._user_service.getPortalVersion()
        except AttributeError:
            ver = self._admin_service.getPortalVersion()
            logger.debug('VidyoPortal getPortalVersion():%s', ver)
        return ver

    def portal_version_info(self):
        """
        get a tuple of `(maj, min, micro, patch, db)` of the remote server API version.
        Version number parsing is done in base 10, ignoring leading zeroes.
        """
        return PortalVersionInfo(
            *map(int, re.match(
                '^VidyoConferencing-(?P<maj>\d).(?P<min>\d).(?P<micro>\d)\((?P<patch>\d+)\).DBv(?P<db>\d+)', # NOQA longline
                self.portal_version_string(),
                re.IGNORECASE
            ).groups())
        )

    @lru_cache()
    @_userservice
    def _login_info(self):
        """
        Get authentication credentials for the user endpoint so that call
        handling can start.
        This must *NOT* be called after registering previous authentication
        credentials with the Vidyo endpoint, or the previous session will be
        invalidated.
        """
        login = self._user_service.logIn()
        logger.debug('VidyoPortal login()%s', login)
        return login

    @_userservice
    def _proxies(self):
        """
        There is no runtime way for a user to select an available proxy
        as they are set only once at the time of user creation.
        Additionally, there is no runtime way for an admin to determine the
        available proxies at time of user creation (only super can do that)
        so this call usually results in failure. We check for that in
        endpoint_login_dict() and return dummy values in that case
        (the VidyoWeb application will hard crash if VidyoProxyAddress is not
        set even if numberProxies == 0)
        """
        try:
            proxy = self._login_info().proxyaddress
        except AttributeError:
            logger.info("no proxy assigned to user:%s", self)
            return None
        return proxy

    @_userservice
    def _endpoint_login_dict(self, guest=True, **kwargs):
        """
        Combine various information from multiple API calls to get necessary
        endpoint authentication information. There's alot. Irritating again.
        ``guest`` (bool) disables whether an endpoint will remain logged in and able
        to access their account post-conference if True.
        If your users don't manage their Vidyo credentials, it's best to set this
        to True.

        returns a dictionary of login information used by the endpoint to authnticate
        with the vidyo manager.
        """
        login_info = self._login_info()
        vmaddress = login_info.vmaddress
        vm_identity = vmaddress.split('@')[0]
        server_port = int(vmaddress.split(':')[1].split(';')[0])
        server_address = vmaddress.split('@')[1].split(':')[0]
        is_tls = vmaddress.split('transport=')[1] == 'TLS'
        if not kwargs.get('insecure_transport'):
            # use binary and to avoid the short ciruit.
            # The RPC transport AND the media transport is authenticated, or
            # nothing is.
            if not (is_tls & self.portal.ssl):
                raise TLSError()

        proxy = self._proxies()
        proxyaddress = None
        proxyport = None
        if proxy:
            assert ':' in proxy
            proxyaddress, proxyport = proxy.split(':', 1)

        return {
            'emcpSecured': is_tls,
            'guestLogin': bool(guest),
            'locationTag': login_info.loctag,
            'name': self._my_account().displayName,
            'portalAccessKey': login_info.pak,
            'portalAddress': self.portal.url.services_url,
            'portalVersion': self.portal_version_string(),
            'serverAddress': server_address,
            'serverPort': server_port,
            'showDialpad': False,
            'showStartmeeting': False,
            'userName': self.username(),
            'numberProxies': proxy and 1 or 0,
            'vidyoProxyAddress': proxyaddress and proxyaddress or "0.0.0.0",
            'vidyoProxyPort': proxyport and proxyport or "0",
            'vmIdentity': vm_identity
        }

    def endpoint_login_data(self, guest=True, **kwargs):
        """
        Get a dictionary of login credentials used to access the VidyoManager service.
        This is passed directly to the Vidyo endpoint which then initiates communication
        with the VM and router.
        """
        return self._endpoint_login_dict(guest, **kwargs)

    def vidyodesktop_login_string(self, guest=True, **kwargs):
        """The endpoint login string needed by VidyoDesktop to login
        This is the string requested as a URL from http://localhost:63457
        Not all parameters are encoded here because query parameters othe than
        those included are not documented.
        """
        login = self._endpoint_login_dict(guest=guest, **kwargs)
        login_info = self._login_info()
        login['guestLogin'] = guest and 'yes' or 'no'
        return 'http://127.0.0.1:63457/dummy?%s' % (
            six.moves.urllib_parse.urlencode({
               'url': self.portal.url.ajax_url,
               'vm': login_info.vmaddress,
               'proxy': self._proxies(),
               'un': login['userName'],
               'pak': login['portalAccessKey'],
               'guest': login['guestLogin'],
               'portal': login['portalAddress'],
               'loctag': login['locationTag'],
               'portalVersion': login['portalVersion']
            })
        )

    @lru_cache()
    def username(self):
        """
        Get the portal username for the current member. This is `api_type` agnostic.
        """
        try:
            return self._user_service.getUserName()
        except MethodNotFound:  # Sometime after portal3.1,
            pass
        except AttributeError:
            # Admin service
            pass
        try:
            if self.member.name:
                return self.member.name
        except AttributeError:
            pass
        if self.portal.user and self.api_type == 'user':
            return self.portal.user
        else:
            logger.exception("couldn't resolve username of Vidyo User")
            raise Error("couldn't resolve username of Vidyo User")

    @_userservice
    @notimplemented
    def set_audibility(self, audible):
        pass

    @_userservice
    @notimplemented
    def set_visibility(self, is_visible):
        pass

    @_userservice
    def start_recording(self, quality=-1):
        """
        Try and start a recording of the user's current conference.
        If the conference is already being recorded this is a no-op.
        If no conference is in progress for the user, LookupError is raised.
        `quality` is an integer value indicating the recording quality. The portal
        does not have a method to query resolution and framerate of different
        recording profiles, only dealing with human-assigned names so this is
        an index into the array of recording profiles available on the portal.
        By default `-1` will refer to the last profile in the list returned
        from the portal, which in an off-the-shelf configuration will be the
        high-quality setting.

        On success returns a UUID of the recording in the user's library of recordings.
        """
        profiles = self._user_service.getRecordingProfiles()
        if not profiles.total:
            raise LookupError("no available recorder")
        profile = profiles.recorder[quality].recorderPrefix

        conf = self._user_service.getConferenceID()
        participants = self._user_service.getParticipants(conf)
        if getattr(participants, 'recorderID'):
            logger.warn("call already in progress")

        self._user_service.startRecording(
            conferenceID=conf,
            recorderPrefix=profile,
        )
        try:
            return int(self._user_service.getParticipants(conf).recorderID)
        except AttributeError:
            raise RuntimeError("couldn't start recording")

    @_userservice
    def stop_recording(self):
        # FIXME https://tracker.ajenta.net/issues/147
        # Viyo API has no facility to determine the id of the
        # recording in progress.

        # The following is a hack to workaround the bug above.
        # We first get a list of all extant recordings for the user.
        # We then stop the recording.
        # After that compute the difference between the two sets of
        # recordings and apply a few heuristics to make fairly sure
        # that the recording is likely to be the correct one.
        # Also require that the difference in length between the number of
        # recordings is 1.

        # Admin users can access all users' recordings. We mustn't allow
        # returning a recording for another user.
        assert self.username() not in ('admin', 'super')
        assert self._my_account().EntityType == 'Normal'

        try:
            current_conf = self._user_service.getConferenceID()
            participants = self._user_service.getParticipants(current_conf)
            recorder_id = participants.recorderID
            if recorder_id is None:
                raise RuntimeError("No recording in progress")
        except (WebFault, AttributeError) as e:
            raise RuntimeError("no conference in progress:%s", e)

        start_time = arrow.now()

        replay = Replay(self.portal.url.host, self.username(), self._password)
        recordings_before = replay.filter(start__lte=start_time, room=current_conf)
        self._user_service.stopRecording(current_conf, recorder_id)

        stop_time = arrow.now()

        recordings_after = replay.filter(False, end__gt=start_time, room=current_conf)
        assert len(
            set(map(lambda x: x.guid, recordings_after)) - set(lambda x: x.guid, recordings_before)
        ) == 1
        candidate = recordings_after[0]
        if candidate.endTime < start_time:
            raise LookupError()
        if candidate.endTime > stop_time:
            # clock skew
            raise EnvironmentError("Possible clock skew between localhost and the remote system")

        return uuid.UUID(candidate.guid)

    @_userservice
    def status(self):
        """
        Get the activity state of the client.
        possible statuses are USER_OFFLINE (not authenticated), USER_IDLE (authenticated),
        and USER_BUSY (involved in the call process, and therefore currently unreachable)
        """
        try:
            stat = self._user_service.myEndpointStatus()
            logger.debug('myEndpointStatus():%s', stat)
        except WebFault as e:
            logger.exception('VidyoPortal myEndpointStatus() exception:%s', e)
            raise Error("RPC failed")

        possible_stats = {
            'Offline': self.USER_OFFLINE, 'Online': self.USER_IDLE,
            'Busy': self.USER_BUSY, 'BusyInOwnRoom': self.USER_BUSY,
            'Ringing': self.USER_BUSY, 'RingAccepted': self.USER_BUSY,
            'RingRejected': self.USER_BUSY, 'RingNoAnswer': self.USER_BUSY,
            'Alerting': self.USER_BUSY, 'AlertCancelled': self.USER_BUSY,
        }
        # We don't use possible_stats.get() because we want to know of KeyError
        try:
            return possible_stats[stat]
        except KeyError:
            raise Error("Unknown status from portal:%s", stat)

    def __str__(self):
        return "%s(%r@%r)" % (
            self.__class__.__name__,
            self.username(),
            self.portal.url.geturl(),
        )
