"""mercurial_server user interface

:organization: Logilab
:copyright: 2013 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
__docformat__ = "restructuredtext en"
_ = unicode

from cubicweb.predicates import is_instance, match_user_groups, match_form_params, has_related_entities
from cubicweb.view import EntityView
from cubicweb.web import Redirect, RequestError
from cubicweb.web.action import Action
from cubicweb.web.controller import Controller
from cubicweb.web.formwidgets import HiddenInput
from cubicweb.web.views import uicfg
from cubicweb.web.views import ibreadcrumbs

from cubes.vcsfile.views import primary as vcsfile

def setup_ui(vreg):

    def hide(attr, **kwargs):
        kwargs['widget'] = HiddenInput
        uicfg.autoform_field_kwargs.tag_attribute(attr, kwargs)

    afs = uicfg.autoform_section
    pvs = uicfg.primaryview_section
    rct = uicfg.reledit_ctrl
    afs.tag_subject_of(('MercurialServerConfig', 'hgadmin_repository', '*'), 'main', 'hidden')

    # Repository
    afs.tag_subject_of(('Repository', 'hosted_by', '*'), 'main', 'attributes')
    pvs.tag_object_of(('*', 'granted_on', 'Repository'), 'hidden')
    uicfg.autoform_field_kwargs.set_fields_order(
        'Repository', ('title', 'hosted_by', 'source_url'))

    # SshPubKey
    rct.tag_subject_of(('CWUser', 'public_key', '*'), {'reload': True})
    afs.tag_object_of(('CWUser', 'public_key', 'SshPubKey'), 'main', 'hidden')
    afs.tag_attribute(('SshPubKey', 'name'), 'inlined', 'attributes')
    afs.tag_subject_of(('SshPubKey', 'public_key', 'CWUser'), 'main', 'hidden')
    pvs.tag_object_of(('SshPubKey', 'public_key', 'CWUser'), 'attributes')


class MSPIBreadCrumbsAdapter(ibreadcrumbs.IBreadCrumbsAdapter):
    __select__ = is_instance('MercurialServerPermission')
    def parent_entity(self):
        return self.entity.granted_on[0]


class MSCRegenerateAction(Action):
    __regid__ = 'regenerate'
    __select__ = is_instance('MercurialServerConfig') & match_user_groups('managers')

    title = _('regenerate')

    def url(self):
        entity = self.cw_rset.get_entity(0, 0)
        repoeid = entity.eid
        return self._cw.build_url('regenerate_hgadmin_repo', eid=repoeid)


class RegenerateMSC(Controller):
    """Controller used to call the regenerate service"""
    __regid__ = 'regenerate_hgadmin_repo'
    __select__ = Controller.__select__ & match_user_groups('managers') & match_form_params('eid')

    def publish(self, rset=None):
        eid = int(self._cw.form['eid'])
        msc = self._cw.entity_from_eid(eid)
        if msc.e_schema.type != 'MercurialServerConfig':
            raise RequestError('a mercurial server configuration is expected')
        self._cw.cnx.call_service('regenerate_hgadmin_repo', async=False,
                                  eid=msc.eid)
        raise Redirect(msc.absolute_url())


class RepositoryMSPermissionsTab(EntityView):
    __regid__ = _('mercurialserver.repositorypermissions_tab')
    __select__ = is_instance('Repository') & has_related_entities('hosted_by')

    def entity_call(self, entity):
        rset = entity.related('granted_on', role='object')
        self.wview('table', rset, 'null')

vcsfile.RepositoryPrimaryView.tabs.append(RepositoryMSPermissionsTab.__regid__)


def registration_callback(vreg):
    vreg.register_all(globals().values(), __name__)
    setup_ui(vreg)
