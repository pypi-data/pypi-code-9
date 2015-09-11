# -*- coding: utf-8 -*-
import os.path as osp

import hglib

from cubicweb import ValidationError, Binary
from cubicweb.devtools.testlib import CubicWebTC

from cubes.mercurial_server.testutils import MercurialServerTCMixin

class HooksBasicTC(MercurialServerTCMixin, CubicWebTC):
    # msc = MercurialServerConfig

    def test_nonascii_login(self):
        with self.admin_access.client_cnx() as cnx:
            user = self.create_user(cnx, u'françois')
            cnx.commit()
            with self.assertRaises(ValidationError):
                cnx.create_entity('SshPubKey',
                                  data=Binary('42'),
                                  reverse_public_key=user)
                cnx.commit()

    def _test_permission_prologue(self, cnx):
        access_key = cnx.user.public_key[0]
        repo = cnx.entity_from_eid(self.admin_user_repo)
        perm = repo.reverse_granted_on[0]
        self._assert_end_of_prologue(cnx, access_key.eid, perm)
        return cnx.entity_from_eid(access_key.eid), cnx.entity_from_eid(perm.eid)

    def _assert_end_of_prologue(self, cnx, access_key, perm):
        server_config = cnx.entity_from_eid(self.server_config)
        # Testing addition
        pubkey = self._hgadmin_file_content('keys', server_config.keys_subdir,
                                            cnx.user().login, str(access_key))
        self.assertEqual(pubkey, 'admin public key')

        # Check access.conf content
        content = self._hgadmin_file_content(server_config.conf_filename)
        self.assertEqual(content,
                         'write user=cw/%(login)s/%(key_eid)d repo=admin_repo\n'
                         % {'login': cnx.user().login,
                            'key_eid': access_key})

    def test_msc_regeneration_service(self):
        with self.admin_access.client_cnx() as cnx:
            access_key, perm = self._test_permission_prologue(cnx)
            access_key = access_key.eid
            perm = perm.eid
            userdesc = cnx.user.format_name_for_mercurial()
            msc = cnx.entity_from_eid(self.server_config)

            with msc.exec_in_hgadmin_clone("pouette", user=userdesc) as hgrepo:
                hgrepo.remove(osp.join(hgrepo.root(), 'keys', msc.keys_subdir))
                filename = osp.join(hgrepo.root(), msc.conf_filename_str)
                with open(filename, 'wb') as access:
                    access.write('')
            cnx.commit()

        with self.admin_access.client_cnx() as cnx:
            cnx.call_service('regenerate_hgadmin_repo', eid=self.server_config)
            self._assert_end_of_prologue(cnx, access_key, perm)

    def test_msc_deletion_ok(self):
        with self.admin_access.client_cnx() as cnx:
            server_config = cnx.entity_from_eid(self.server_config)
            conf_filename = server_config.conf_filename
            keys_dir = server_config.keys_subdir
            access_key, _perm = self._test_permission_prologue(cnx)

            cnx.execute('DELETE MercurialServerConfig X WHERE X eid %s' %
                        self.server_config)
            cnx.commit()

            # Check access.conf content
            content = self._hgadmin_file_content(conf_filename)
            self.assertEqual(content, '\n')

            with self.assertRaises(IOError):
                self._hgadmin_file_content('keys', keys_dir,
                                           cnx.user.login, str(access_key))

    def test_msc_deletion_with_rollback_inside(self):
        """ on deletion failure (i.e.: deletion order is issued
        but the trasnaction fails), the hgadmin repo files should
        be untouched -- though we may observe a pair of deletion commit/backout
        at the mercurial repository level
        """
        with self.admin_access.client_cnx() as cnx:
            access_key, perm = self._test_permission_prologue(cnx)
            access_key = access_key.eid
            perm = perm.eid
            repo = cnx.entity_from_eid(self.server_config).hgadmin_repo
            cnx.execute('DELETE MercurialServerConfig X WHERE X eid %s' %
                        self.server_config)
            cnx.rollback()
            repo.refresh() # need to refresh so local_cache is up to date

        with self.admin_access.client_cnx() as cnx:
            self._assert_end_of_prologue(cnx, access_key, perm)

            # check that a 'backout' commit did happen
            server_config = cnx.entity_from_eid(self.server_config)
            hgrepo = hglib.open(server_config.hgadmin_repopath)
            alllogs = '\n'.join([entry[5] for entry in hgrepo.log()])
            self.assertIn('backout', alllogs)

    def test_permission_AUD(self):
        """ Test Adding, Updating and Deleting """
        with self.admin_access.client_cnx() as cnx:
            access_key, perm = self._test_permission_prologue(cnx)
            # Updating
            perm.cw_set(permission_level=u"write")
            cnx.commit() # Triggers hooks
            # Testing update
            # Check access.conf content
            server_config = cnx.entity_from_eid(self.server_config)
            content = self._hgadmin_file_content(server_config.conf_filename)
            self.assertEqual(content,
                             'write user=cw/%(login)s/%(key_eid)d repo=admin_repo\n'
                             % {'login': cnx.user.login,
                                'key_eid': access_key.eid,
                                })


            # Deleting the permission, thus the access_key relation
            perm.cw_delete()
            cnx.commit() # Triggers hooks
            #Check access.conf content
            content = self._hgadmin_file_content(server_config.conf_filename)
            self.assertEqual(content, '\n')


    def test_accesskey_AUD(self):
        """ Test Adding, Updating and Deleting"""
        with self.admin_access.client_cnx() as cnx:
            access_key, perm = self._test_permission_prologue(cnx)
            # Updating
            access_key.cw_set(data=Binary('24'))
            cnx.commit() # Triggers hooks
            # Testing update
            pubkey = self._hgadmin_file_content('keys', 'cw',
                                                cnx.user.login, str(access_key.eid))
            self.assertEqual(pubkey, '24')

            # Deleting the key, thus the access_key relation
            access_key.cw_delete()
            cnx.commit() # Triggers hooks
            # Testing deletion
            with self.assertRaises(IOError) as exc :
                pubkey = self._hgadmin_file_content('keys', 'cw',
                                                    cnx.user.login, str(access_key.eid))

            # Check access.conf content
            server_config = cnx.entity_from_eid(self.server_config)
            content = self._hgadmin_file_content(server_config.conf_filename)
            self.assertEqual(content, '\n')


    def test_consistent_permissions(self):
        """ Test at most one permissions for any (key, repo) pair"""
        with self.admin_access.client_cnx() as cnx:
            # Adding
            access_key = cnx.create_entity('SshPubKey',
                                           data=Binary('42'),
                                           reverse_public_key=cnx.user)
            perm = cnx.create_entity('MercurialServerPermission',
                                     permission_level=u'read',
                                     access_key=access_key,
                                     granted_on=self.admin_user_repo)
            cnx.commit() # Triggers hooks
            with self.assertRaises(ValidationError) as exc :
                # The relations access_key and repo are inlined ...
                perm = cnx.create_entity('MercurialServerPermission',
                                         permission_level=u'deny',
                                         access_key=access_key,
                                         granted_on=self.admin_user_repo)
                cnx.commit() # ... so are checked immediatly even without commit


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
