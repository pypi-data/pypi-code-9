import json
import urllib

from cubicweb.devtools import webtest


class WSMEQueryTest(webtest.CubicWebTestTC):
    @classmethod
    def init_config(cls, config):
        super(WSMEQueryTest, cls).init_config(config)
        config.debugmode = True

    def test_orderby(self):
        self.login()

        res = self.webapp.get(
            '/cwuser?orderby=login',
            headers={"Accept": "application/json"})

        data = res.json
        self.assertNotIn('faultcode', data)
        self.assertEqual(
            ['admin', 'anon'],
            [d['login'] for d in data])

        res = self.webapp.get(
            '/cwuser?orderby=-login',
            headers={"Accept": "application/json"})

        data = res.json
        self.assertNotIn('faultcode', data)
        self.assertEqual(
            ['anon', 'admin'],
            [d['login'] for d in data])

    def test_limit(self):
        self.login()

        res = self.webapp.get(
            '/cwuser?limit=1',
            headers={"Accept": "application/json"})

        data = res.json
        self.assertEqual(1, len(data))

    def test_offset(self):
        self.login()

        # we need a limit because sqlite seems not to like an offset without a
        # limit
        res = self.webapp.get(
            '/cwuser?limit=1&offset=2',
            headers={"Accept": "application/json"})

        data = res.json
        self.assertNotIn('faultcode', data)
        self.assertEqual(0, len(data))

    def test_filter_on_one_attribute(self):
        self.login()

        res = self.webapp.get(
            '/cwuser?' + urllib.urlencode({
                'filter': json.dumps({
                    'login': 'admin'
                })
            }),
            headers={"Accept": "application/json"}
        )

        data = res.json
        self.assertNotIn('faultcode', data)

        self.assertEqual(1, len(data))
        self.assertEqual(u'admin', data[0]['login'])

    def test_filter_on_attribute_and_relation(self):
        self.login()

        res = self.webapp.get(
            '/cwuser?' + urllib.urlencode({
                'filter': json.dumps({
                    'login': {'$ne': 'anon'},
                    'in_group': {
                        'name': 'managers'
                    }
                })
            }),
            headers={"Accept": "application/json"}
        )

        data = res.json
        self.assertNotIn('faultcode', data)

        self.assertEqual(1, len(data))
        self.assertEqual(u'admin', data[0]['login'])

    def test_unset_relation(self):
        with self.admin_access.repo_cnx() as cnx:
            g_eid = cnx.create_entity('CWGroup', name=u'test').eid
            cnx.find('CWUser', login=u'admin').one().cw_set(in_group=g_eid)
            cnx.commit()

        self.login()

        url = '/cwgroup/test'
        res = self.webapp.put_json(
            url,
            {"<in_group": None},
            headers={"Accept": "application/json",
                     "Content-Type": "application/json"})
        if '<!DOCTYPE html>' in res.body:
            import html2text
            print html2text.html2text(res.body)
            assert False
        self.assertEqual(200, res.status_int)
        with self.admin_access.repo_cnx() as cnx:
            self.assertEqual(
                (),
                cnx.entity_from_eid(g_eid).reverse_in_group)

    def test_unset_relation_w_empty_list(self):
        with self.admin_access.repo_cnx() as cnx:
            g_eid = cnx.create_entity('CWGroup', name=u'test').eid
            cnx.find('CWUser', login=u'admin').one().cw_set(in_group=g_eid)
            cnx.commit()

        self.login()

        url = '/cwgroup/test'
        res = self.webapp.put_json(
            url,
            {"<in_group": []},
            headers={"Accept": "application/json",
                     "Content-Type": "application/json"})
        if '<!DOCTYPE html>' in res.body:
            import html2text
            print html2text.html2text(res.body)
            assert False
        self.assertEqual(200, res.status_int)
        with self.admin_access.repo_cnx() as cnx:
            self.assertEqual(
                (),
                cnx.entity_from_eid(g_eid).reverse_in_group)

    def test_call_function(self):
        with self.admin_access.repo_cnx() as cnx:
            u = cnx.create_entity(
                'CWUser', login=u"newuser", upassword=u"xx",
                in_group=cnx.find('CWGroup', name='users').one())
            cnx.commit()
            self.assertEqual(u.cw_adapt_to('IWorkflowable').state, 'activated')
            u.cw_clear_relation_cache()
        self.login()

        res = self.webapp.post_json(
            '/cwuser/newuser/!IWorkflowable.fire_transition',
            {"tr": "deactivate", "comment": "from the tests"},
            headers={"Accept": "application/json",
                     "Content-Type": "application/json"})

        data = res.json
        self.assertNotIn('faultcode', data)

        self.assertIn('eid', data)
        self.assertIn('modification_date', data)

        with self.admin_access.repo_cnx() as cnx:
            u = cnx.entity_from_eid(u.eid)
            self.assertEqual(
                u.cw_adapt_to('IWorkflowable').state, 'deactivated')

    def test_reverse_inlined(self):
        self.login()

        with self.admin_access.repo_cnx() as cnx:
            etype_eid = cnx.find('CWEType', name='CWUser').one().eid

        res = self.webapp.post_json(
            '/workflow/',
            {"name": "test", "workflow_of": [{"eid": etype_eid}],
             "<state_of": [{"name": "draft"}]},
            headers={"Accept": "application/json",
                     "Content-Type": "application/json"})

        data = res.json
        self.assertNotIn('faultcode', data)

    def test_set_inlined_null(self):
        self.login()

        res = self.webapp.post_json(
            '/cwproperty/',
            {"pkey": "system.version.cubicweb", "for_user": None},
            headers={"Accept": "application/json",
                     "Content-Type": "application/json"})

        data = res.json
        self.assertNotIn('faultcode', data)
