"""entity classes for vcsfile content types

:organization: Logilab
:copyright: 2007-2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
__docformat__ = "restructuredtext en"
import os.path as osp
from itertools import chain

from cubicweb import Unauthorized, ValidationError
from cubicweb.entities import AnyEntity, fetch_config

from cubes.vcsfile.hooks import repo_cache_dir

_MARKER = object()

def remove_authinfo(url):
    try:
        base, remaining = url.split('@')
    except ValueError:
        return url
    try:
        scheme, authinfo = base.split('://')
    except ValueError:
        return url
    return u'%s://***@%s' % (scheme, remaining)

class Repository(AnyEntity):
    """customized class for Repository entities"""
    __regid__ ='Repository'

    __permissions__ = ('write',)
    fetch_attrs, cw_fetch_order = fetch_config(['source_url', 'title', 'type'])
    rest_attr = 'eid' # see #XXX, using path cause pb w/ apache redirection

    @property
    def localcachepath(self):
        """return a path to the local repository cache (`.local_cache`)

        Does make sense only for mercurial repositories.
        The path itself should be enforced unless some late
        permissions problem arises (in which case this will fail).
        There is no warranty of an actual repository here.
        """
        if self.type != 'mercurial':
            raise TypeError('.localcachepath only makes sense on a mercurial repository')
        if self.local_cache is None:
            raise Exception('%s.local_cache does not exist yet' % self.eid)
        return osp.join(repo_cache_dir(self._cw.vreg.config), self.local_cache)

    def dc_title(self):
        if self.title:
            return self.title
        if self.source_url:
            return remove_authinfo(self.source_url)
        title = self._cw._('%(type)s repository #%(eid)s') % {
            'type': self.type, 'eid': self.eid}
        return title

    def printable_value(self, attr, *args, **kwargs):
        if attr == 'source_url':
            if args:
                value = args[0]
            elif 'value' in kwargs:
                value = kwargs['value']
            else:
                value = self.source_url
            if value:
                return remove_authinfo(value)
            return u''
        return super(Repository, self).printable_value(attr, *args, **kwargs)

    # navigation in versioned content #########################################

    def latest_known_revision(self):
        """return the changeset id of the latest known revision"""
        latestrev = self._cw.execute(
            'Any CS ORDERBY E DESC LIMIT 1 WHERE R eid %(r)s, REV from_repository R, '
            'REV changeset CS, REV eid E', {'r' : self.eid})[0][0]
        if latestrev is None:
            return -1
        return latestrev

    def heads_rset(self):
        """return a result set containing head revision (eg revisions without
        children)
        """
        return self._cw.execute(
            'Any REV WHERE R eid %(r)s, REV from_repository R, '
            'NOT CREV parent_revision REV, REV hidden FALSE', {'r' : self.eid})

    def branches(self):
        """return existing branches"""
        rql = 'DISTINCT Any B WHERE R eid %(r)s, REV from_repository R, REV branch B'
        branches = [b for b, in self._cw.execute(rql, {'r' : self.eid})]
        if not branches:
            branches = [self.default_branch()]
        return branches

    def branch_head(self, branch=_MARKER, public_only=False):
        """return latest revision of the given branch"""
        if branch is _MARKER:
            branch = self.default_branch()
        rql = (
            'Any MAX(REV) WHERE '
            '  REV from_repository R, R eid %%(r)s, REV branch %%(branch)s%s'
            % (', REV phase "public"' if public_only else ''))
        eid = self._cw.execute(rql, {'r': self.eid, 'branch': branch})[0][0]
        if eid is None:
            return None
        return self._cw.entity_from_eid(eid)

    # vcs write support ########################################################

    def default_branch(self):
        return u'default'

    def make_revision(self, msg, author=None, branch=None,
                      parentrev=None, added=(), deleted=()):
        """parameters:
        :msg: the check-in message (string, mandatory)
        :author: the check-in author (string)
        :branch: the branch in which the revision should be done (string)
        :parentrev: the parent of the revision
        :added: list of (filename, file-like) tuples
        :deleted: list of filenames to remove

        Filenames are relative to the repo root.

        Return the new revision entity.
        """
        if not self._cw.user.has_permission(u'write', self.eid):
            raise Unauthorized('You are not allowed to create new revisions')
        if author is None:
            author = self._cw.user.login
        assert parentrev, 'you must specify a parent revision'
        #assert parent
        for fpath in chain((fpath for fpath, _ in added), deleted):
            assert not (osp.isabs(fpath) or '../' in fpath), \
                'you must specify a path relative to the root of the repository, not %s' % fpath
        args = {'description' : msg, 'author': author, 'branch': branch,
                'parent': parentrev, 'added': added,
                'deleted': deleted}
        vcsrepo = self.cw_adapt_to('VCSRepo')
        csetid = vcsrepo.add_revision(**args)
        try:
            self.refresh(raise_on_error=True)
        except (Unauthorized, ValidationError):
            vcsrepo.strip_cset(csetid)
            raise
        return vcsrepo.entity_for_cset(csetid)

    def refresh(self, raise_on_error=False):
        self._cw.call_service('refresh_repository', eids=[self.eid], raise_on_error=raise_on_error)


class Revision(AnyEntity):
    """customized class for Revision entities"""
    __regid__ ='Revision'
    fetch_attrs, cw_fetch_order = fetch_config(['changeset', 'branch',
                                                'author', 'description', 'creation_date'],
                                               mainattr='eid',
                                               order='DESC')

    @property
    def shortdesc(self):
        return self.description.split('\n', 1)[0].strip()

    def dc_title(self):
        return u'#%(changeset)s %(desc)s' % {
            'changeset': self.changeset,
            'desc': self.shortdesc}

    def dc_long_title(self):
        try:
            return self._cw._('%(rev)s of repository %(repo)s: %(desc)s') % {
                'rev': self.dc_title(), 'repo': self.repository.dc_title(),
                'desc': self.shortdesc}
        except Unauthorized:
            return self._cw._('%(rev)s of a private repository') % {
                'rev': self.dc_title()}

    def sortvalue(self, rtype=None):
        if rtype is None:
            return self.eid
        return super(Revision, self).sortvalue(rtype)

    # navigation in versioned content #########################################

    @property
    def repository(self):
        return self.from_repository[0]

    @property
    def children_revisions(self):
        return self.reverse_parent_revision

    def export(self):
        '''return text/diff version of the revision'''
        if self.changeset is None:
            return None
        return self._cw.call_service('vcs.export-rev',
                                     repo=self.repository.eid,
                                     nodeid=self.changeset)

