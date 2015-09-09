import wsme.types

from cubicweb.devtools import testlib
from cubes.wsme.types import (
    Base, wsattr, PassThroughType, JsonDataType, JsonData)


class WSMETypesTest(testlib.CubicWebTC):
    def test_passthroughtype_validate(self):
        o = object()
        self.assertIs(PassThroughType.validate(o), o)

    def test_jsondatatype_validate(self):
        o = object()
        self.assertIs(JsonDataType.validate(o), o)

    def test_jsondatatype_none(self):
        self.assertIsNone(JsonData.frombasetype(None))

    def test_jsondatatype_tobasetype(self):
        self.assertEqual(JsonData.tobasetype([{'1': 1}]), '[{"1": 1}]')

    def test_fromjson(self):
        o = object()
        from wsme.rest.json import fromjson
        self.assertIs(fromjson(JsonData, o), o)

    def test_wsattr_invalid_rel(self):
        class ACWUser(Base):
            __etype__ = 'CWUser'
            unknown_attr = wsattr('unknown_attr')

        ACWUser.reginit(self.vreg)

        self.assertIsNone(ACWUser.unknown_attr.etype)

        ACWUser.finalize_init()

    def test_wsattr_polymorph_target_is_Any(self):
        class AEvent(Base):
            __etype__ = 'Event'
            __autoattr__ = True

        AEvent.reginit(self.vreg)

        self.assertEqual(AEvent.organized_by.etype, 'Any')

    def test_detect_polymorph_array(self):
        class AEvent(Base):
            __etype__ = 'Event'
            __autoattr__ = True

        AEvent.reginit(self.vreg)
        AEvent.finalize_init()

        self.assertTrue(wsme.types.isarray(AEvent.attended_by.datatype))

    def test_wsattr_forbid_Any_on_non_polymorphic(self):
        class ACWUser(Base):
            __etype__ = 'CWUser'
            in_group = wsattr('in_group', etype='Any')

        with self.assertRaises(ValueError) as cm:
            ACWUser.reginit(self.vreg)

        exc = cm.exception
        self.assertEqual(
            exc.message, 'Any should not be used on non-polymorphic relations')

    def test_wsattr_detects_wrong_etype(self):
        class ACWUser(Base):
            __etype__ = 'CWUser'
            in_group = wsattr('in_group', etype='Event')

        with self.assertRaises(ValueError) as cm:
            ACWUser.reginit(self.vreg)

        exc = cm.exception
        self.assertEqual(
            exc.message,
            'Wrong etype Event for relation in_group subject')

    def test_attr_by_name(self):
        class ACWUser(Base):
            __etype__ = 'CWUser'
            __autoattr__ = True

            reverse_organized_by = wsattr(
                'organized_by', role='object', name='organize')

        ACWUser.reginit(self.vreg)
        ACWUser.finalize_init()

        self.assertIs(ACWUser.attr_by_name('login'), ACWUser.login)
        self.assertIs(ACWUser.attr_by_name('organize'),
                      ACWUser.reverse_organized_by)

        with self.assertRaises(KeyError):
            ACWUser.attr_by_name('password')

    def test_unknown_etype(self):
        class AType(Base):
            __etype__ = 'AType'
            __autoattr__ = True

        AType.reginit(self.vreg)
        AType.finalize_init()

    def test_specific_autoattr(self):
        class ACWUser(Base):
            __etype__ = 'CWUser'
            __autoattr__ = ('login', 'in_group')

        ACWUser.reginit(self.vreg)
        ACWUser.finalize_init()

        self.assertTrue(hasattr(ACWUser, 'in_group'))
        self.assertTrue(hasattr(ACWUser, 'login'))
        self.assertFalse(hasattr(ACWUser, 'surname'))

    def test_from_entity_write_only(self):
        class ACWUser(Base):
            __etype__ = 'CWUser'

            login = wsattr('login', writeonly=True)

        ACWUser.reginit(self.vreg)
        ACWUser.finalize_init()

        with self.admin_access.repo_cnx() as cnx:
            data = ACWUser()
            data.from_entity(cnx.user)

        self.assertIs(data.login, wsme.types.Unset)

    def test_from_entity_typed_fetch(self):
        class AEvent(Base):
            __etype__ = 'Event'
            __autoattr__ = True

        AEvent.reginit(self.vreg)
        AEvent.finalize_init()

        with self.admin_access.repo_cnx() as cnx:
            event = cnx.create_entity(
                'Event', organized_by=cnx.user)
            event.cw_set(attended_by=[
                cnx.user, cnx.find('CWGroup', name='managers').one()])

            data = AEvent()
            data.from_entity(event, fetch=['attended_by[CWGroup]'])

        self.assertEqual(len(data.attended_by), 1)
        self.assertEqual(data.attended_by[0].cw_etype, 'CWGroup')

    def test_types_final_rel(self):
        class ACWUser(Base):
            __etype__ = 'CWUser'
            login = wsattr('login', datatype=wsme.types.text)
            # XXX in real-life, the upassword would never be copied from an
            # entity to a ws type, only from a ws type to an entity (with
            # encryption at the same time)
            password = wsattr('upassword', datatype=wsme.types.text)

        ACWUser.reginit(self.vreg)

        with self.admin_access.repo_cnx() as cnx:
            u = cnx.find("CWUser", login=u"admin").one()
            u_eid = u.eid
            ws_u = ACWUser(u)

        self.assertEqual(u_eid, ws_u.eid)
        self.assertEqual(u"admin", ws_u.login)

        ws_u.login = u"anotherone"
        ws_u.password = 'somepassword'
        with self.admin_access.repo_cnx() as cnx:
            cls = self.vreg['etypes'].etype_class('CWUser')
            u = cls.cw_instantiate(cnx.execute, **ws_u.final_values())

            self.assertNotEqual(u_eid, u.eid)
            self.assertEqual(u"anotherone", ws_u.login)

    def test_types_final_rel_autoattr(self):
        class ACWUser(Base):
            __etype__ = 'CWUser'

            login = wsattr()
            password = wsattr('upassword')

        ACWUser.reginit(self.vreg)
        self.vreg.wsme_registry.finalize_init()

        with self.admin_access.repo_cnx() as cnx:
            u = cnx.find("CWUser", login=u"admin").one()
            u_eid = u.eid
            ws_u = ACWUser(u)

        self.assertEqual(u_eid, ws_u.eid)
        self.assertEqual(u"admin", ws_u.login)

    def test_types_relations(self):
        class ACWUser(Base):
            __etype__ = 'CWUser'

            login = wsattr('login', datatype=wsme.types.text)
            # XXX in real-life, the upassword would never be copied from an
            # entity to a ws type, only from a ws type to an entity (with
            # encryption at the same time)
            password = wsattr('upassword', datatype=wsme.types.text)

            in_group = wsattr('in_group', datatype=['ACWGroup'])

        class ACWGroup(Base):
            __etype__ = 'CWGroup'

            name = wsattr('name', datatype=wsme.types.text)
            users = wsattr('in_group', role='object', datatype=[ACWUser])

        ACWUser.reginit(self.vreg)
        ACWGroup.reginit(self.vreg)

        with self.admin_access.repo_cnx() as cnx:
            u = cnx.find("CWUser", login=u"admin").one()
            u_eid = u.eid
            g_eid = u.in_group[0].eid
            ws_u = ACWUser(u, fetch=['in_group'])
            ws_u2 = ACWUser(u, fetch=['in_group.name'])

        self.assertEqual(u_eid, ws_u.eid)
        self.assertEqual(u"admin", ws_u.login)

        self.assertEqual(g_eid, ws_u.in_group[0].eid)
        self.assertEqual(u"managers", ws_u2.in_group[0].name)

    def test_polymorphic_relations(self):
        State = self.vreg.wsme_registry.lookup('State')

        with self.admin_access.repo_cnx() as cnx:
            state = cnx.find('State', name='activated').one()
            tr_eid = state.allowed_transition[0].eid
            tr_created_by_eid = state.allowed_transition[0].created_by[0].eid
            ws_state = State(state, fetch=['allowed_transition.created_by'])

        self.assertEqual(tr_eid, ws_state.allowed_transition[0].eid)
        self.assertEqual('Transition', ws_state.allowed_transition[0].cw_etype)
        self.assertEqual(
            tr_created_by_eid,
            ws_state.allowed_transition[0].created_by.eid)

    def test_object_relations(self):
        CWGroup = self.vreg.wsme_registry.lookup('CWGroup')
        self.assertTrue(hasattr(CWGroup, 'in_group_object'))
        self.assertEqual('<in_group', CWGroup.in_group_object.name)

