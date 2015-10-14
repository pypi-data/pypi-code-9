# -*- coding: utf-8 -*-
'''
Copyright 2015 
	Centre de données socio-politiques (CDSP)
	Fondation nationale des sciences politiques (FNSP)
	Centre national de la recherche scientifique (CNRS)
License
	This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

import json
from collections import defaultdict
import traceback
import logging
import uuid
from threading import Lock

class RoomHandler(object):
	"""Store data about connections, rooms, which users are in which rooms, etc."""
	class __OnlyOne:
		def __init__(self):
			self.val = None
			self.client_info = {}  # for each client id we'll store  {'wsconn': wsconn, 'room':room, 'user':username}
			self.room_info = {}  # dict  to store a list of  {'cid':cid, 'user':username, 'wsconn': wsconn} for each room
			self.roomates = {}  # store all connection from a room
			self.user_conn_id = {}  # store a list of connection for a unique user id
			self.all_conn = [] # store all connection 
			self._add_roomuser_lock_client_info = Lock()
			self._add_roomuser_lock_room_info = Lock()
			self._add_roomuser_lock_user_conn_id = Lock()
			self._add_roomuser_lock_roomates = Lock()
			self._add_roomuser_lock_all_conn = Lock()
			self._say_lock = Lock()
			
		def __str__(self):
			return 'self ' + self
		
		def add_roomuser(self, message, user):
			"""Add user to room. Return clientID"""
			# meant to be called from the main handler (page where somebody indicates a username and a room to join)
			cid = uuid.uuid4().hex  # generate a connection id.
			decodemessage = json.loads(message)
			room = decodemessage["room"]
			self._add_roomuser_lock_room_info.acquire()
			try:
				if not room in self.room_info:  # it's a new room
					self.room_info[room] = []
			finally:
				self._add_roomuser_lock_room_info.release()	 
			nn = user.username
			self._add_roomuser_lock_user_conn_id.acquire()
			try:
				if user.id in self.user_conn_id:
					self.user_conn_id[user.id].append(cid)
				else:
					self.user_conn_id[user.id] = []
					self.user_conn_id[user.id].append(cid)
			finally:
				self._add_roomuser_lock_user_conn_id.release()
			self._add_roomuser_lock_client_info.acquire()
			try:
				self.client_info[cid] = {'room': room, 'user': nn, 'uid': user.id}  # we still don't know the WS connection for this client
			finally:
				self._add_roomuser_lock_client_info.release()
			self._add_roomuser_lock_room_info.acquire()
			try:
				self.room_info[room].append({'cid': cid, 'user': nn, 'uid': user.id})
			finally:
				self._add_roomuser_lock_room_info.release()
			return cid
			
		def add_client_wsconn(self, client_id, conn):
			"""Store the websocket connection corresponding to an existing client."""
			self._add_roomuser_lock_all_conn.acquire()
			try:
				self.all_conn.append(conn)
			finally:
				self._add_roomuser_lock_all_conn.release()
			self._add_roomuser_lock_client_info.acquire()
			try:
				self.client_info[client_id]['wsconn'] = conn
				cid_room = self.client_info[client_id]['room']
			finally:
				self._add_roomuser_lock_client_info.release()
			self._add_roomuser_lock_roomates.acquire()
			try:
				if cid_room in self.roomates:
					self.roomates[cid_room].add(conn)
				else:
					self.roomates[cid_room] = {conn}
			finally:
				self._add_roomuser_lock_roomates.release()		 
			self._add_roomuser_lock_room_info.acquire()
			try:  
				for user in self.room_info[cid_room]:
					if user['cid'] == client_id:
						user['wsconn'] = conn
						break
			finally:
				self._add_roomuser_lock_room_info.release()
			# send "join" and  "user_list" messages
			self.send_join_msg(client_id)
			user_list = self.users_in_room(cid_room)
			cwsconns = self.roomate_cwsconns(client_id)
			self.send_users_msg(cwsconns, user_list)	
			
		def remove_client(self, cid):
			"""Remove all client information from the room handler."""
		
			self._add_roomuser_lock_client_info.acquire()
			try:
				cid_room = self.client_info[cid]['room']
				user = self.client_info[cid]['user']
				uid = self.client_info[cid]['uid']
				 # first, remove the client connection from the corresponding room in self.roomates
				client_conn = self.client_info[cid]['wsconn']
			finally:
				self._add_roomuser_lock_client_info.release()
			self._add_roomuser_lock_all_conn.acquire()
			try:
				self.all_conn.remove(client_conn)
			finally:
				self._add_roomuser_lock_all_conn.release()	
			self._add_roomuser_lock_roomates.acquire()
			try:	
				if client_conn in self.roomates[cid_room]:
					self.roomates[cid_room].remove(client_conn)
					if len(self.roomates[cid_room]) == 0:
						del(self.roomates[cid_room])
			finally:
				self._add_roomuser_lock_roomates.release()				  
				r_cwsconns = self.roomate_cwsconns(cid)
				# filter out the list of connections r_cwsconns to remove clientID
			self._add_roomuser_lock_client_info.acquire()
			try:	
				r_cwsconns = [conn for conn in r_cwsconns if conn != self.client_info[cid]['wsconn']]
				self.client_info[cid] = None
			finally:
				self._add_roomuser_lock_client_info.release()
			self._add_roomuser_lock_room_info.acquire()
			try:	  
				for userid in self.room_info[cid_room]:
					if userid['cid'] == cid:
						self.room_info[cid_room].remove(userid)
						break
			finally:
				self._add_roomuser_lock_room_info.release()	 
			self._add_roomuser_lock_user_conn_id.acquire()
			try:		
				self.user_conn_id[uid].remove(cid)
				if not self.user_conn_id[uid]:
					del(self.user_conn_id[uid])
			finally:
				self._add_roomuser_lock_user_conn_id.release()	
				
			self.send_leave_msg(user, r_cwsconns)
			user_list = self.users_in_room(cid_room)
			self.send_users_msg(r_cwsconns, user_list)
			
			self._add_roomuser_lock_room_info.acquire()
			try:	  
				if len(self.room_info[cid_room]) == 0:  # if room is empty, remove.
					del(self.room_info[cid_room])
					logging.info("Removed empty room %s" % cid_room) 
			finally:
				self._add_roomuser_lock_room_info.release()	
					
		def users_in_room(self, rn):
			"""Return a list with the usernames of the users currently connected to the specified room."""
			nir = []  # users in room
			for user in self.room_info[rn]:
				nir.append(user['user'])
			return nir
		
		def roomate_cwsconns(self, cid):
			"""Return a list with the connections of the users currently connected to the room where
			the specified client (cid) is connected."""
			cid_room = self.client_info[cid]['room']
			r = {}
			self._add_roomuser_lock_roomates.acquire()
			try:
				if cid_room in self.roomates:
					r = self.roomates[cid_room]
				return r
			finally:
				self._add_roomuser_lock_roomates.release() 
			
		def send_to_room(self, room, pmessage):
			"""Return a list with the connections of the users currently connected to the room where
			the specified client (cid) is connected."""
			response = {}
			response["data"] = pmessage["data"]
			response["task"] = pmessage["task"]
			self._add_roomuser_lock_roomates.acquire()
			try:
				if room in self.roomates:
					con_room = self.roomates[room]
					answer = json.dumps(response)
					for c in con_room:
						try:
							self._say_lock.acquire()
							c.write_message(answer)
						except Exception, e:
							logging.warning('send to room : %s', e)
							logging.warning(answer)
							logging.warning(traceback.format_exc())
						finally:
							self._say_lock.release()
				else:
					logging.info('room %s does not exist', room)
			finally:
				self._add_roomuser_lock_roomates.release() 
				 
		def send_to_users(self, user, pmessage):
			"""Return a list with the connections of the users currently connected to the room where
			the specified client (cid) is connected."""
			response = {}
			response["data"] = pmessage["data"]
			response["task"] = pmessage["task"]
			for u in user:
				if u in self.user_conn_id:
					con_room = self.user_conn_id[u]
					for c in con_room:
						try:
							sock = self.client_info[c]['wsconn']
							self._say_lock.acquire()
							sock.write_message(json.dumps(response))
						except Exception, e:
							logging.warning('send to users : %s', e)
							logging.warning(json.dumps(response))
							logging.warning(traceback.format_exc())
						finally:
							self._say_lock.release()
				else:
					logging.info('user %s not found', u)
		
		def send_to_all(self, pmessage):
			"""Return a list with the connections of the users currently connected to the room where
			the specified client (cid) is connected."""
			response = {}
			response["data"] = pmessage["data"]
			response["task"] = pmessage["task"]
			con_room = self.all_conn
			for c in con_room:
				try:
					self._say_lock.acquire()
					c.write_message(json.dumps(response))
				except Exception, e:
					logging.warning('send to all : %s', e)
					logging.warning(json.dumps(response))
					logging.warning(traceback.format_exc())
				finally:
					self._say_lock.release()
				 
		def send_to_cid(self, cid, pmessage):
			"""Return a list with the connections of the users currently connected to the room where
			the specified client (cid) is connected."""
			response = {}
			response["data"] = pmessage["data"]
			response["task"] = pmessage["task"]
			con_cid = self.client_info[cid]['wsconn']
			try:
				self._say_lock.acquire()
				con_cid.write_message(json.dumps(response))
			except Exception, e:
					logging.warning('send to cid : %s', e)
					logging.warning(json.dumps(response))
					logging.warning(traceback.format_exc())
			finally:
				self._say_lock.release()

		
		def send_join_msg(self, client_id):
			"""Send a message of type 'join' to all users connected to the room where client_id is connected."""
			username = self.client_info[client_id]['user']
			r_cwsconns = self.roomate_cwsconns(client_id)
			msg = {"msgtype": "join", "username": username, "data": " joined the chat room."}
			pmessage = json.dumps(msg)
			for conn in r_cwsconns:
				try:
					self._say_lock.acquire()
					conn.write_message(pmessage)
				except Exception, e:
					logging.warning('send join message : %s', e)
					logging.warning(pmessage)
					logging.warning(traceback.format_exc())
				finally:
					self._say_lock.release()
	
		@staticmethod
		def send_users_msg(conns, user_list):
			"""Send a message of type 'user_list' (contains a list of usernames) to all the specified connections."""
			msg = {"msgtype": "user_list", "data": user_list}
			pmessage = json.dumps(msg)
			for c in conns:
				try:
					c.write_message(pmessage)
				except:
					pass
	
		@staticmethod
		def send_leave_msg(user, rconns):
			"""Send a message of type 'leave', specifying the username that is leaving, to all the specified connections."""
			msg = {"msgtype": "leave", "username": user, "data": " left the chat room."}
			pmessage = json.dumps(msg)
			for conn in rconns:
				try:
					conn.write_message(pmessage)
				except:
					pass

	instance = None
	
	def __new__(cls): # __new__ always a classmethod
		if not RoomHandler.instance:
			RoomHandler.instance = RoomHandler.__OnlyOne()
		return RoomHandler.instance

	def __getattr__(self, name):
		
		return getattr(self.instance, name)
	
	def __setattr__(self, name):
		return setattr(self.instance, name)
	