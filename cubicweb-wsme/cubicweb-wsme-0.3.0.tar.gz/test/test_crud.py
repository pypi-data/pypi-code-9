import base64
import json
import urllib

import cubicweb

from cubicweb.devtools import webtest, httptest


class WSMECRUDLegacyTest(httptest.CubicWebServerTC):
    """ Tests that hits cubicweb wsgi bugs so we keep them
    in their legacy form
    """

    @classmethod
    def init_config(cls, config):
        super(WSMECRUDLegacyTest, cls).init_config(config)

    def test_cwgroup_entity_delete(self):
        with self.admin_access.repo_cnx() as cnx:
            cnx.create_entity('CWGroup', name=u'test').eid
            cnx.commit()

        self.web_login()
        url = 'cwgroup/test'
        res = self.web_request(
            url, method='DELETE', headers={"Accept": "application/json"})
        if '<!DOCTYPE html>' in res.body:
            import html2text
            print html2text.html2text(res.body)
            assert False
        self.assertEqual(204, res.status)

    def test_del_relation(self):
        with self.admin_access.repo_cnx() as cnx:
            u = cnx.find('CWUser', login=u'anon').one()
            g = cnx.find('CWGroup', name=u'managers').one()
            u.cw_set(in_group=g)
            g_eid = g.eid
            cnx.commit()

        self.web_login()

        res = self.web_request(
            'cwuser/anon/in_group/%s' % (g_eid),
            method='DELETE',
            headers={"Accept": "application/json"})

        self.assertEqual(204, res.status)

        with self.admin_access.repo_cnx() as cnx:
            u = cnx.find('CWUser', login=u'anon').one()

            self.assertEqual(1, len(u.in_group))

    def test_entity_get_not_exists(self):
        self.web_login()
        url = 'cwuser/nonexistinguser'
        res = self.web_request(
            url, headers={'Accept': 'application/json'})
        self.assertEqual(404, res.status)
        data = json.loads(res.body)
        self.assertIn('faultcode', data)
        self.assertEqual(data['faultcode'], 'Client')
        self.assertEqual(data['faultstring'], 'Not Found')


class WSMECRUDTest(webtest.CubicWebTestTC):
    @classmethod
    def init_config(cls, config):
        super(WSMECRUDTest, cls).init_config(config)
        config.debugmode = True

    def test_cwuser_get(self):
        url = '/cwuser?' + urllib.urlencode({'filter': '{"login": "anon"}'})
        res = self.webapp.get(url, headers={"Accept": "application/json"})
        if '<!DOCTYPE html>' in res.body:
            import html2text
            print html2text.html2text(res.body)
        data = res.json
        self.assertNotIn('faultstring', data)
        self.assertEqual(u"anon", data[0]['login'])

    def test_cwuser_get_keyonly(self):
        url = '/cwuser?' + urllib.urlencode({'keyonly': True})
        res = self.webapp.get(url, headers={"Accept": "application/json"})
        if '<!DOCTYPE html>' in res.body:
            import html2text
            print html2text.html2text(res.body)
        data = res.json
        self.assertNotIn('login', data[0])
        self.assertIn('modification_date', data[0])

    def test_cwuser_entity_get(self):
        url = '/cwuser/anon?fetch=in_group'
        res = self.webapp.get(url, headers={"Accept": "application/json"})
        if '<!DOCTYPE html>' in res.body:
            import html2text
            print html2text.html2text(res.body)
        data = res.json
        self.assertEqual(u"anon", data['login'])
        self.assertEqual(1, len(data['in_group']))
        self.assertIn('modification_date', data['in_group'][0])

    def test_cwuser_entity_get_fetch_typed_relation(self):
        with self.admin_access.repo_cnx() as cnx:
            cnx.find('CWGroup', name=u'managers').one().cw_set(
                created_by=cnx.find('CWUser', login=u'admin').one())
            cnx.commit()
        self.login()
        url = '/cwuser/admin?fetch=<created_by[CWGroup]'
        res = self.webapp.get(url, headers={"Accept": "application/json"})
        if '<!DOCTYPE html>' in res.body:
            import html2text
            print html2text.html2text(res.body)
        data = res.json
        self.assertEqual(200, res.status_int, data)
        self.assertEqual(u"admin", data['login'])
        self.assertEqual(1, len(data['<created_by']))
        self.assertIn('modification_date', data['<created_by'][0])

    def test_cwgroup_post(self):
        self.login()
        url = '/cwgroup'
        res = self.webapp.post(
            url, '{"name": "test"}',
            headers={"Accept": "application/json",
                     "Content-Type": "application/json"})
        if '<!DOCTYPE html>' in res.body:
            import html2text
            print html2text.html2text(res.body)
            assert False

        data = res.json
        self.assertEqual(200, res.status_int, data)

        self.assertEqual(u"test", data['name'])
        g_eid = data['eid']

        with self.admin_access.repo_cnx() as cnx:
            self.assertEqual(u"test", cnx.entity_from_eid(g_eid).name)

    def test_cwgroup_entity_put(self):
        with self.admin_access.repo_cnx() as cnx:
            g_eid = cnx.create_entity('CWGroup', name=u'test').eid
            cnx.commit()

        self.login()
        url = '/cwgroup/test'
        res = self.webapp.put(
            url, '{"name": "newname"}',
            headers={"Accept": "application/json",
                     "Content-Type": "application/json"})
        if '<!DOCTYPE html>' in res.body:
            import html2text
            print html2text.html2text(res.body)
            assert False
        self.assertEqual(200, res.status_int)
        with self.admin_access.repo_cnx() as cnx:
            self.assertEqual(u"newname", cnx.entity_from_eid(g_eid).name)

    def test_multi_create(self):
        self.login()

        res = self.webapp.post_json(
            '/cwuser?fetch=in_group',
            {
                'login': "AUser", 'password': "APassword",
                'in_group': [{
                    'name': 'ANewGroup'
                }]
            },
            headers={"Accept": "application/json",
                     "Content-Type": "application/json"},
        )

        data = res.json
        self.assertNotIn('faultcode', data)

        self.assertEqual(200, res.status_int)

        g_eid = data['in_group'][0]['eid']
        with self.admin_access.repo_cnx() as cnx:
            self.assertEqual(u"ANewGroup", cnx.entity_from_eid(g_eid).name)

    def test_multi_update(self):
        with self.admin_access.repo_cnx() as cnx:
            g_eid = cnx.find('CWGroup', name=u'managers').one().eid

        self.login()

        res = self.webapp.put_json(
            '/cwuser/admin?fetch=in_group',
            {
                'surname': 'Admin',
                'in_group': [{
                    'eid': g_eid,
                    'name': 'newname'
                }]
            },
            headers={"Accept": "application/json",
                     "Content-Type": "application/json"},
        )

        data = res.json
        self.assertNotIn('faultcode', data)

        self.assertEqual(200, res.status_int)

        self.assertEqual(u'Admin', data['surname'])
        self.assertEqual(g_eid, data['in_group'][0]['eid'])

        with self.admin_access.repo_cnx() as cnx:
            self.assertEqual(u"newname", cnx.entity_from_eid(g_eid).name)

    def test_update_and_create(self):
        with self.admin_access.repo_cnx() as cnx:
            g_eid = cnx.find('CWGroup', name=u'managers').one().eid

        self.login()

        res = self.webapp.put_json(
            '/cwuser/admin?fetch=in_group',
            {
                'surname': "AdminName",
                'in_group': [{
                    'name': 'ANewGroup'
                }, {
                    'eid': g_eid,
                }]
            },
            headers={"Accept": "application/json",
                     "Content-Type": "application/json"},
        )

        data = res.json
        self.assertNotIn('faultcode', data)

        self.assertEqual(200, res.status_int)

        g_eids = [g['eid'] for g in data['in_group']]
        with self.admin_access.repo_cnx() as cnx:
            names = set(cnx.entity_from_eid(eid).name for eid in g_eids)
            self.assertEqual(names, set([u"managers", u"ANewGroup"]))

    def test_create_and_update(self):
        with self.admin_access.repo_cnx() as cnx:
            g_eid = cnx.find('CWGroup', name=u'managers').one().eid

        self.login()

        res = self.webapp.post_json(
            '/cwuser',
            {
                'login': "AUser", 'password': "APassword",
                'in_group': [{
                    'eid': g_eid,
                    'name': 'NewName'
                }]
            },
            headers={"Accept": "application/json",
                     "Content-Type": "application/json"},
        )

        data = res.json
        self.assertNotIn('faultcode', data)

        self.assertEqual(200, res.status_int)

        with self.admin_access.repo_cnx() as cnx:
            self.assertEqual(u"NewName", cnx.entity_from_eid(g_eid).name)

    def test_get_relation(self):
        self.login()

        res = self.webapp.get(
            '/cwgroup/managers/<in_group?keyonly=1&limit=2',
            headers={"Accept": "application/json",
                     "Content-Type": "application/json"})

        data = res.json
        self.assertNotIn('faultcode', data)

        self.assertEqual(200, res.status_int)
        self.assertEqual(1, len(data))
        self.assertEqual('CWUser', data[0]['cw_etype'])

    def test_add_relation(self):
        with self.admin_access.repo_cnx() as cnx:
            u_eid = cnx.find('CWUser', login=u'anon').one().eid

        self.login()

        res = self.webapp.post_json(
            '/cwgroup/managers/<in_group',
            u_eid,
            headers={"Accept": "application/json",
                     "Content-Type": "application/json"})

        self.assertEqual(200, res.status_int)

        with self.admin_access.repo_cnx() as cnx:
            g = cnx.find('CWGroup', name=u'managers').one()
            u = cnx.find('CWUser', login=u'anon').one()

            self.assertIn(g, u.in_group)

    def test_get_binary(self):
        with self.admin_access.repo_cnx() as cnx:
            f = cnx.create_entity(
                'File', data=cubicweb.Binary('test'),
                data_name=u'filename',
                data_format=u'text/plain')
            cnx.commit()
            eid = f.eid

        self.login()

        res = self.webapp.get(
            '/file/{}'.format(eid),
            headers={"Accept": "application/json"})

        data = res.json
        self.assertNotIn('faultcode', data)
        self.assertEqual(200, res.status_int)

        self.assertEqual(data['data'], base64.encodestring('test'))

    def test_set_binary(self):
        with self.admin_access.repo_cnx() as cnx:
            f = cnx.create_entity(
                'File', data=cubicweb.Binary('test'),
                data_name=u'filename',
                data_format=u'text/plain')
            cnx.commit()
            eid = f.eid

        self.login()

        res = self.webapp.put_json(
            '/file/{}'.format(eid),
            {"data": base64.encodestring('newcontent')},
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json"})

        data = res.json
        self.assertNotIn('faultcode', data)
        self.assertEqual(200, res.status_int)

        self.assertEqual(data['data'], base64.encodestring('newcontent'))

        with self.admin_access.repo_cnx() as cnx:
            f = cnx.entity_from_eid(eid)
            self.assertEqual(f.data.getvalue(), 'newcontent')
