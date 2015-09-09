# copyright 2014 Christophe de Vienne, all rights reserved.
# contact http://www.unlish.com/ -- mailto:christophe@unlish.com
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-wsme tests
"""

import wsme

from cubicweb.devtools import testlib

from cubes.wsme.loader import load_entities, get_columns
from cubes.wsme.loader import to_fetchtree, get_entities
import cubes.wsme


class DummyTest(testlib.CubicWebTC):
    def test_dumb(self):
        pass


class WSMELoaderTest(testlib.CubicWebTC):
    @classmethod
    def init_config(cls, config):
        super(WSMELoaderTest, cls).init_config(config)
        config.debugmode = True

    def setUp(self):
        super(WSMELoaderTest, self).setUp()

    def test_to_fetchtree(self):
        self.assertEqual(
            to_fetchtree(None, keyonly=False),
            {'': {}})
        self.assertEqual(
            to_fetchtree(None, keyonly=True),
            {})
        self.assertEqual(
            to_fetchtree([]),
            {})
        self.assertEqual(
            to_fetchtree(['in_group.']),
            {'in_group': {'': {}}})

        self.assertEqual(
            to_fetchtree(['in_group']),
            {'in_group': {}})

        self.assertEqual(
            to_fetchtree(['in_group.name']),
            {'in_group': {'name': {}}})

        self.assertEqual(
            to_fetchtree(['in_group.name', 'in_group.owned_by']),
            {'in_group': {'name': {}, 'owned_by': {}}})

        self.assertEqual(
            to_fetchtree(['in_group.', 'in_group.owned_by']),
            {'in_group': {'': {}, 'owned_by': {}}})

    def test_get_columns_keyonly(self):
        CWGroup = self.vreg.wsme_registry.lookup('CWGroup')

        with self.admin_access.repo_cnx() as cnx:
            m = get_columns(cnx, CWGroup, None)

            self.assertEqual(m, {'eid': None, 'modification_date': None})

    def test_get_columns_defaults(self):
        CWGroup = self.vreg.wsme_registry.lookup('CWGroup')

        with self.admin_access.repo_cnx() as cnx:
            m = get_columns(cnx, CWGroup, {'': {}})

            self.assertEqual(m, {
                'eid': None,
                'name': None,
                'modification_date': None,
                'creation_date': None,
                'cwuri': None,
                'created_by': {'eid': None, 'modification_date': None},
            })

    def test_get_columns_ignore_multiple_relations(self):
        print self.vreg.wsme_registry.cwtypes
        print self.vreg.wsme_registry._complex_types
        CWUser = self.vreg.wsme_registry.lookup('CWUser')
        print CWUser

        with self.admin_access.repo_cnx() as cnx:
            m = get_columns(cnx, CWUser, {'in_group': None})

            self.assertEqual(m, {
                'eid': None,
                'login': None,
                'modification_date': None,
                'creation_date': None,
                'cwuri': None,
                'firstname': None,
                'surname': None,
                'last_login_time': None,
                'custom_workflow': {'eid': None, 'modification_date': None},
                'created_by': {'eid': None, 'modification_date': None},
                'primary_email': {'eid': None, 'modification_date': None},
            })

    def test_get_entities(self):
        CWUser = self.vreg.wsme_registry.guess_datatype('CWUser')
        Event = self.vreg.wsme_registry.guess_datatype('Event')

        events = [Event(), Event(), Event()]
        users = [CWUser(), CWUser()]

        self.assertEqual(get_entities(events, ('owned_by',)), [])
        events[0].owned_by = users

        self.assertEqual(set(get_entities(events, ('owned_by',))),
                         set(users))

        events[1].owned_by = [users[0]]

        self.assertEqual(set(get_entities(events, ('owned_by',))),
                         set(users))

        self.assertEqual(get_entities(events, ('created_by', 'created_by')),
                         [])

        events[0].created_by = users[0]
        events[1].created_by = users[0]
        events[2].created_by = users[1]

        self.assertEqual(set(get_entities(events, ('created_by',))),
                         set(users))

    def test_load_entities_keyonly(self):
        CWGroup = self.vreg.wsme_registry.lookup('CWGroup')

        with self.admin_access.repo_cnx() as cnx:
            expected = cnx.execute(
                'Any G, MD ORDERBY N '
                'WHERE G is CWGroup, G name N, G modification_date MD').rows
            res = load_entities(cnx, CWGroup, orderby=['name'], fetchtree={})

        self.assertIs(res[0].name, wsme.types.Unset)
        self.assertEqual(
            [[e.eid, e.modification_date] for e in res],
            expected)

    def test_load_entities_attributes(self):
        CWGroup = self.vreg.wsme_registry.lookup('CWGroup')

        with self.admin_access.repo_cnx() as cnx:
            expected = cnx.execute(
                'Any G, N, MD ORDERBY N '
                'WHERE G is CWGroup, G name N, G modification_date MD').rows
            res = load_entities(
                cnx, CWGroup, orderby=['name'], fetchtree={'': {}})

        self.assertIsNot(res[0].name, wsme.types.Unset)
        self.assertEqual(
            [[e.eid, e.name, e.modification_date] for e in res],
            expected)

    def test_load_entities_unary_relations(self):
        CWGroup = self.vreg.wsme_registry.lookup('CWGroup')

        with self.admin_access.repo_cnx() as cnx:
            cnx.execute(
                'SET X created_by U WHERE X is CWGroup, U login "admin"')
            expected = cnx.execute(
                'Any G, N, MD, U, UMD ORDERBY N '
                'WHERE G is CWGroup, G name N, G modification_date MD, '
                'G created_by U?, U modification_date UMD').rows
            res = load_entities(
                cnx, CWGroup, orderby=['name'], fetchtree={'': {}})

        self.assertIsNot(res[0].created_by, wsme.types.Unset)
        self.assertEqual(
            [[e.eid, e.name, e.modification_date,
              e.created_by.eid, e.created_by.modification_date] for e in res],
            expected)

    def test_load_entities_null_relations(self):
        CWUser = self.vreg.wsme_registry.lookup('CWUser')

        with self.admin_access.repo_cnx() as cnx:
            cnx.execute('DELETE X created_by U WHERE X is CWUser')
            expected = cnx.execute(
                'Any U, L, MD, NULL ORDERBY L '
                'WHERE U is CWUser, U login L, U modification_date MD').rows
            res = load_entities(
                cnx, CWUser, orderby=['login'], fetchtree={'': {}})

        self.assertIsNot(res[0].created_by, wsme.types.Unset)
        self.assertEqual(
            [[e.eid, e.login, e.modification_date,
              e.created_by] for e in res],
            expected)

    def test_load_entities_nested_unary_relations(self):
        CWGroup = self.vreg.wsme_registry.lookup('CWGroup')

        with self.admin_access.repo_cnx() as cnx:
            cnx.execute(
                'SET X created_by U WHERE X is CWGroup, U login "admin"')
            expected = cnx.execute(
                'Any G, N, MD, U, UMD ORDERBY N '
                'WHERE G is CWGroup, G name N, G modification_date MD, '
                'G created_by U?, U modification_date UMD').rows
            res = load_entities(
                cnx, CWGroup, orderby=['name'],
                fetchtree={'created_by': {'': {}}})

        self.assertIsNot(res[0].created_by, wsme.types.Unset)
        self.assertIsNot(res[0].created_by.created_by, wsme.types.Unset)
        self.assertEqual(
            [[e.eid, e.name, e.modification_date,
              e.created_by.eid, e.created_by.modification_date] for e in res],
            expected)

    def test_load_entities_multi_relation_keyonly(self):
        CWUser = self.vreg.wsme_registry.lookup('CWUser')

        with self.admin_access.repo_cnx() as cnx:
            res = load_entities(
                cnx, CWUser, orderby=['login'], fetchtree={'in_group': {}})

        self.assertIsNot(res[0].in_group, wsme.types.Unset)
        self.assertIs(res[0].in_group[0].name, wsme.types.Unset)

    def test_load_entities_multi_relation_attributes(self):
        CWUser = self.vreg.wsme_registry.lookup('CWUser')

        with self.admin_access.repo_cnx() as cnx:
            res = load_entities(
                cnx, CWUser, orderby=['login'],
                fetchtree={'in_group': {'': {}}})

        self.assertIsNot(res[0].in_group, wsme.types.Unset)
        self.assertIsNot(res[0].in_group[0].name, wsme.types.Unset)

    def test_load_entities_multi_relation_nested(self):
        CWUser = self.vreg.wsme_registry.lookup('CWUser')

        with self.admin_access.repo_cnx() as cnx:
            cnx.execute(
                'SET X created_by U WHERE X is CWGroup, U login "admin"')
            res = load_entities(cnx, CWUser, orderby=['login'],
                                fetchtree={
                                    'in_group': {
                                        'created_by': {
                                            'in_group': {'': {}}}}})

        self.assertIsNot(res[0].in_group, wsme.types.Unset)
        self.assertIsNot(res[0].in_group[0].name, wsme.types.Unset)
        self.assertIsNot(res[0].in_group[0].created_by, wsme.types.Unset)
        self.assertIsNot(
            res[0].in_group[0].created_by.in_group,
            wsme.types.Unset)
        self.assertIsNot(
            res[0].in_group[0].created_by.in_group[0].name,
            wsme.types.Unset)

    def test_load_entities_multi_relation_nested_w_empty_targets(self):
        CWUser = self.vreg.wsme_registry.lookup('CWUser')

        with self.admin_access.repo_cnx() as cnx:
            res = load_entities(cnx, CWUser, orderby=['login'],
                                fetchtree={
                                    'in_group': {
                                        'created_by': {
                                            'in_group': {'': {}}}}})

        self.assertIsNot(res[0].in_group, wsme.types.Unset)
        self.assertIsNot(res[0].in_group[0].name, wsme.types.Unset)
        self.assertIsNone(res[0].in_group[0].created_by)

    def test_load_entities_reverse_relation(self):
        CWUser = self.vreg.wsme_registry.lookup('CWUser')

        with self.admin_access.repo_cnx() as cnx:
            res = load_entities(
                cnx, CWUser,
                fetchtree={'<created_by': {}})
        self.assertIsNot(res[0].created_by_object, wsme.types.Unset)
        self.assertIsNot(res[0].created_by_object[0].cw_etype, 'CWGroup')

    def test_load_entities_typed_relation(self):
        CWUser = self.vreg.wsme_registry.lookup('CWUser')

        with self.admin_access.repo_cnx() as cnx:
            cnx.execute(
                'SET X created_by U WHERE X is CWGroup, U login "admin"')
            res = load_entities(
                cnx, CWUser,
                fetchtree={'<created_by[CWGroup]': {}})
        self.assertIsNot(res[0].created_by_object, wsme.types.Unset)
        self.assertEquals(res[0].created_by_object[0].cw_etype, 'CWGroup')

        with self.admin_access.repo_cnx() as cnx:
            cnx.execute(
                'SET X created_by U WHERE X is CWGroup, U login "admin"')
            res = load_entities(
                cnx, CWUser,
                query_filter={'login': 'admin'},
                fetchtree={'<created_by[CWGroup,CWUser]': {}})
        self.assertIsNot(res[0].created_by_object, wsme.types.Unset)
        for entity in res[0].created_by_object:
            self.assertIn(entity.cw_etype, ('CWGroup', 'CWUser'))

    def test_limit(self):
        Event = self.vreg.wsme_registry.lookup('Event')

        with self.admin_access.repo_cnx() as cnx:
            cnx.create_entity('Event', name=u'event 1')
            cnx.create_entity('Event', name=u'event 2')
            cnx.create_entity('Event', name=u'event 3')

            res = load_entities(
                cnx, Event, orderby=('name',), limit=1, fetchtree={'': {}})

            self.assertEqual(len(res), 1)
            self.assertEqual(res[0].name, 'event 1')

            res = load_entities(
                cnx, Event, orderby=('name',), limit=2, fetchtree={'': {}})

            self.assertEqual(len(res), 2)
            self.assertEqual(res[0].name, 'event 1')
            self.assertEqual(res[1].name, 'event 2')

    def test_offset(self):
        Event = self.vreg.wsme_registry.lookup('Event')

        with self.admin_access.repo_cnx() as cnx:
            cnx.create_entity('Event', name=u'event 1')
            cnx.create_entity('Event', name=u'event 2')
            cnx.create_entity('Event', name=u'event 3')

            res = load_entities(
                cnx, Event, orderby=('name',), limit=2, offset=1,
                fetchtree={'': {}})

            self.assertEqual(len(res), 2)
            self.assertEqual(res[0].name, 'event 2')
            self.assertEqual(res[1].name, 'event 3')

            res = load_entities(
                cnx, Event, orderby=('name',), limit=1, offset=2,
                fetchtree={'': {}})

            self.assertEqual(len(res), 1)
            self.assertEqual(res[0].name, 'event 3')

    def test_load_unauthorized_attribute(self):
        Event = self.vreg.wsme_registry.lookup('Event')

        with self.admin_access.repo_cnx() as cnx:
            cnx.create_entity('Event', restricted_permissions_attr=u'test')
            cnx.commit()

        with self.new_access('anon').repo_cnx() as cnx:
            res = load_entities(cnx, Event, fetchtree={'': {}})

        self.assertIs(res[0].restricted_permissions_attr, wsme.types.Unset)

    def test_fetch_any_relation(self):
        Event = self.vreg.wsme_registry.lookup('Event')

        with self.admin_access.repo_cnx() as cnx:
            e = cnx.create_entity('Event', restricted_permissions_attr=u'test')
            e.cw_set(organized_by=cnx.user)
            cnx.commit()

        with self.new_access('anon').repo_cnx() as cnx:
            res = load_entities(
                cnx, Event, fetchtree={'organized_by': {'': {}}})

        self.assertIs(res[0].restricted_permissions_attr, wsme.types.Unset)

    def test_fetch_invalid_relation(self):
        Event = self.vreg.wsme_registry.lookup('Event')

        with self.admin_access.repo_cnx() as cnx:
            e = cnx.create_entity('Event', restricted_permissions_attr=u'test')
            e.cw_set(organized_by=cnx.user)
            cnx.commit()

            with self.assertRaises(KeyError) as cm:
                load_entities(
                    cnx, Event, fetchtree={'unknown': {'': {}}})

        exc = cm.exception
        self.assertEqual(exc.message, 'No attr named unknown')

    def test_fetch_ignore_extra_attr(self):
        Event = self.vreg.wsme_registry.lookup('Event')

        with self.admin_access.repo_cnx() as cnx:
            e = cnx.create_entity('Event', restricted_permissions_attr=u'test')
            e.cw_set(organized_by=cnx.user)
            cnx.commit()

            load_entities(
                cnx, Event, fetchtree={'extra_attr': {'': {}}})

    def test_fetch_ignore_attributes(self):
        Event = self.vreg.wsme_registry.lookup('Event')

        with self.admin_access.repo_cnx() as cnx:
            e = cnx.create_entity('Event', restricted_permissions_attr=u'test')
            e.cw_set(organized_by=cnx.user)
            cnx.commit()

            load_entities(
                cnx, Event, fetchtree={'name': {'': {}}})
