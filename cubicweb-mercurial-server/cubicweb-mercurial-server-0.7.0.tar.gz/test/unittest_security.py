# -*- coding: utf-8 -*-
import os.path as osp

from cubicweb import Unauthorized, ValidationError, Binary
from cubicweb.devtools.testlib import CubicWebTC

from cubes.mercurial_server.testutils import MercurialServerTCMixin


class SchemaPermTC(MercurialServerTCMixin, CubicWebTC):

    def test_ordinary_user_AUD(self):
        with self.admin_access.client_cnx() as cnx:
            toto = self.create_user(cnx, u'toto').eid
            titi = self.create_user(cnx, u'titi').eid
            cnx.commit()

        with self.new_access('toto').client_cnx() as cnx:
            # toto cannot create a mercurial server config
            with self.assertRaises(Unauthorized):
                self.create_mercurial_server(cnx, 'for_toto')
                cnx.commit()

        with self.new_access('toto').client_cnx() as cnx:
            # without a public key, toto cannot create a hosted repository
            toto_repo = self.create_mercurial_repo(cnx, 'toto_repo')
            with self.assertRaises(ValidationError) as wraperr:
                toto_repo.cw_set(hosted_by=self.server_config)
            self.assertEqual({'hosted_by': 'To create a hosted repository, toto must have a public key'},
                             wraperr.exception.args[1])

        with self.new_access('titi').client_cnx() as cnx:
            # user titi owns a Repository, but not hosted_by
            pubkey = cnx.create_entity('SshPubKey', data=Binary('titi public key'),
                                       reverse_public_key=titi)
            cnx.commit()
            titi_repo = self.create_mercurial_repo(cnx, 'titi_repo')
            cnx.commit()

        with self.new_access('toto').client_cnx() as cnx:
            pubkey = cnx.create_entity('SshPubKey',
                                       data=Binary('toto public key'),
                                       reverse_public_key=toto)
            self.create_mercurial_repo(cnx, 'toto_repo',
                                       hosted_by=self.server_config)
            cnx.commit()
        with self.admin_access.client_cnx() as cnx:
            toto_user = cnx.entity_from_eid(toto)
            toto_key = toto_user.public_key[0].eid
            toto_login = toto_user.login

            conf_filename = cnx.entity_from_eid(self.server_config).conf_filename
        content = self._hgadmin_file_content(conf_filename)
        self.assertListEqual(
            ['write user=cw/admin/%d repo=admin_repo' % self.admin_pubkey,
             'write user=cw/toto/%d repo=toto_repo' % toto_key],
            content.splitlines())
        with self.admin_access.client_cnx() as cnx:
            keys_subdir = cnx.entity_from_eid(self.server_config).keys_subdir
        pk = self._hgadmin_file_content('keys', keys_subdir,
                                        toto_login, str(toto_key))
        self.assertEqual('toto public key', pk)
        with self.admin_access.client_cnx() as cnx:
            cnx.execute('DELETE CWUser U WHERE U login "toto"')
            cnx.commit()
            conf_filename = cnx.entity_from_eid(self.server_config).conf_filename
        content = self._hgadmin_file_content(conf_filename)

        # all info about toto is gone
        self.assertEqual(['write user=cw/admin/%d repo=admin_repo' %
                          self.admin_pubkey],
                         content.splitlines())
        with self.admin_access.client_cnx() as cnx:
            keys_subdir = cnx.entity_from_eid(self.server_config).keys_subdir
        with self.assertRaises(IOError):
            self._hgadmin_file_content('keys', keys_subdir,
                                       toto_login, str(toto_key))

    def test_delete_hosted_by_non_owner(self):
        # just make sure non-owners of a Repository cannot change its
        # hosted_by relation (as per schema permissions)

        with self.admin_access.client_cnx() as cnx:
            toto = self.create_user(cnx, u'toto').eid
            cnx.commit()
        with self.new_access('toto').client_cnx() as cnx:
            repo = cnx.entity_from_eid(self.admin_user_repo)
            self.assertNotIn(toto, set(o.eid for o in repo.owned_by))
            config = repo.hosted_by[0]
            with self.assertRaises(Unauthorized):
                cnx.execute('DELETE R hosted_by C WHERE R eid %d,'
                            '   C eid %d' %
                            (self.admin_user_repo, config.eid))
                cnx.commit()
        with self.admin_access.client_cnx() as cnx:
            repo = cnx.entity_from_eid(self.admin_user_repo)
            repopath = repo.source_url[7:]
            self.assertTrue(osp.exists(repopath))

    def test_repo_deletion_non_owner(self):
        # make sure non-owners cannot delete a repository (as per schema
        # permissions)
        with self.admin_access.client_cnx() as cnx:
            toto = self.create_user(cnx, u'toto')
            cnx.commit()
        with self.new_access('toto').client_cnx() as cnx:
            repo = cnx.entity_from_eid(self.admin_user_repo)
            with self.assertRaises(Unauthorized):
                cnx.execute('DELETE Repository R WHERE R eid %d' %
                            self.admin_user_repo)
                cnx.commit()
        with self.new_access('toto').client_cnx() as cnx:
            repo = cnx.entity_from_eid(self.admin_user_repo)
            repopath = repo.source_url[7:]
            self.assertTrue(osp.exists(repopath))

    def test_msperm_owner(self):
        with self.admin_access.client_cnx() as cnx:
            owner = self.create_user(cnx, u'owner')
            owner.cw_set(reverse_owned_by=self.admin_user_repo)
            cnx.commit()
        with self.new_access(u'owner').client_cnx() as cnx:
            rset = cnx.execute('INSERT SshPubKey K: K data %(d)s, U public_key K WHERE U eid %(u)s',
                               {'u': cnx.user.eid, 'd': Binary(b'toto')})
            cnx.execute('INSERT MercurialServerPermission P: '
                        'P granted_on R, P permission_level "write", '
                        'P access_key K WHERE R eid %(r)s, K eid %(k)s',
                        {'r': self.admin_user_repo, 'k': rset[0][0]})

    def test_msperm_non_owner(self):
        with self.admin_access.client_cnx() as cnx:
            toto = self.create_user(cnx, u'toto')
            cnx.commit()
        with self.new_access('toto').client_cnx() as cnx:
            rset = cnx.execute('INSERT SshPubKey K: K data %(d)s, U public_key K WHERE U eid %(u)s',
                               {'u': cnx.user.eid, 'd': Binary(b'toto')})
            with self.assertRaises(Unauthorized):
                cnx.execute('INSERT MercurialServerPermission P: '
                            'P granted_on R, P permission_level "write", '
                            'P access_key K WHERE R eid %(r)s, K eid %(k)s',
                            {'r': self.admin_user_repo, 'k': rset[0][0]})


if __name__ == '__main__':
    import unittest
    unittest.main()
