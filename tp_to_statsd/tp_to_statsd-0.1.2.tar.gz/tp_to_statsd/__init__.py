import os
from xml.etree import ElementTree as ET

import requests
from slugify import slugify
from statsd.defaults.env import statsd


class TP(object):
    """
    Encapsulated access to some parts of the Target Process REST API.
    """

    def __init__(self, api_base=None, tp_user=None, tp_password=None):
        self.api_base = api_base
        if self.api_base is None:
            self.api_base = os.environ.get('TP_API_BASE')
        if self.api_base is None:
            raise ValueError('Must provide API base URI.')
        self.user = tp_user
        if self.user is None:
            self.user = os.environ.get('TP_USER')
        if self.user is None:
            raise ValueError('Must provide API user.')
        self.password = tp_password
        if self.password is None:
            self.password = os.environ.get('TP_PASSWORD')
        if self.password is None:
            raise ValueError('Must provide API password.')

    @classmethod
    def plural_for_type(kls, typename):
        """Convert (eg) Bug to Bugs, UserStory to Userstories."""

        if not isinstance(typename, str):
            raise TypeError("Requires a (string) typename.")
        if typename == "":
            raise ValueError("Requires a non-empty typename.")

        # FIXME: incomplete
        _overrides = {
            'UserStory': 'Userstories',
        }

        return _overrides.get(
            typename,
            typename[0].upper() + typename[1:].lower() + 's',
        )

    def act_on_collection(self, initial_url):
        """yields every child of a paginated collection"""

        nexturl = initial_url

        while True:
            #print("Fetching " + nexturl)
            resp = requests.get(
                nexturl,
                auth=(
                    self.user,
                    self.password,
                ),
            )
            root = ET.fromstring(resp.text)
            for child in root:
                yield child
            nexturl = root.attrib.get('Next')
            if nexturl is None:
                break

    def get_state_count(
        self,
        state_id,
        tp_type,
    ):
        count = 0
        for entity in self.act_on_collection(
            self.api_base + "%(type)s/?include=[EntityState]&where=EntityState.Id eq '%(state_id)s'&take=250" % {
                'state_id': state_id,
                'type': TP.plural_for_type(tp_type),
            }
        ):
            count += 1
        return count

    def get_states(self, tp_type, tp_process=None):
        states = []

        apiurl = self.api_base + "EntityStates?where=(IsInitial eq 'false') and (IsFinal eq 'false') and (EntityType.Name eq '%(type)s')" % {
            'type': tp_type,
        }
        if tp_process is not None:
            apiurl += " and (Process.Name eq '%(process)s')" % {
                'process': tp_process,
            }

        for state in self.act_on_collection(apiurl):
            state_id = state.attrib.get('Id')
            state_name = state.attrib.get('Name')
            states.append(
                (state_id, state_name)
            )
        return states


# use this as a gauge
key_pattern = 'tp.%(process)s.%(type)s.%(state)s.count'

def update_statsd_gauge(tp_process, tp_type, state_name, count):
    statsd_key = key_pattern % {
        'process': slugify(tp_process),
        'state': slugify(state_name),
        'type': slugify(tp_type),
    }
    print('Calculated %s as %d.' % (statsd_key, count))
    statsd.gauge(
        statsd_key,
        count,
    )
