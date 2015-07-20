# -*- coding: utf-8 -*-
"""entity classes for vcsfile content types

:organization: Logilab
:copyright: 2007-2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""
__docformat__ = "restructuredtext en"
import os, os.path as osp
import tempfile
import shutil
import errno
from contextlib import contextmanager
from itertools import izip_longest

import hglib
from hglib import context
from hglib.error import CommandError
from hglib.util import cmdbuilder

from yams import ValidationError
from cubicweb import QueryError
from cubicweb.predicates import is_instance, score_entity
from cubicweb.view import EntityAdapter

from cubes.vcsfile import bridge
from cubes.vcsfile.hooks import repo_cache_dir


class HGRepo(EntityAdapter):
    __regid__ = 'VCSRepo'
    __select__ = (is_instance('Repository') &
                  score_entity(lambda repo: repo.type == u'mercurial'))
    configs = ['extensions.hgext.strip=']  # enable strip command
    path = None

    def entity_for_cset(self, ctx_hex):
        rset = self._cw.execute('Any X WHERE X from_repository R, R eid %(repo)s, X changeset %(cs)s',
                                {'repo': self.entity.eid, 'cs': unicode(ctx_hex)})
        if rset:
            return rset.one()
        return None

    def full_path(self, path):
        return osp.join(self.path, path)

    def __contains__(self, path):
        with self.hgrepo() as hgclient:
            return path in hgclient.manifest(all=True)

    def _create_repo(self):
        if osp.exists(self.path):
            return
        hglib.init(self.path)

    def __init__(self, *args, **kwargs):
        super(HGRepo, self).__init__(*args, **kwargs)
        cnx = self._cw
        try:
            security_enabled = cnx.security_enabled
        except AttributeError:
            # XXX Request objects don't have that method in cw 3.19
            security_enabled = cnx.cnx.security_enabled

        cacheroot = repo_cache_dir(self.entity._cw.vreg.config)
        # deactivate read security first, needed to get access to local_cache
        with security_enabled(read=False):
            if cacheroot is not None and self.entity.local_cache is not None:
                self.path = osp.join(cacheroot, self.entity.local_cache)

        if not self.path:
            raise ValidationError(self.entity.eid,
                    {'source_url': cnx._('no local access to repository')})

        if not osp.exists(self.path):
            self._create_repo() # ensure local cache exists

    @contextmanager
    def hgrepo(self):
        client = hglib.client.hgclient(self.path, encoding=self.entity.encoding,
                                       configs=self.configs, connect=False)
        client.hidden = True
        with client:
            yield client

    def manifest(self, rev):
        with self.hgrepo() as hgclient:
            return list(hgclient.manifest(rev=rev))

    def file_deleted(self, path, rev=None):
        with self.hgrepo() as repo:
            if rev is None:
                log = repo.log(files=[self.full_path(path)], removed=True, limit=1)
                if not log:
                    raise Exception('this file does not even exist')
                rev = log[0][1][:12]
            for file in repo.manifest(rev=rev):
                if file[4] == path:
                    return False
            return True

    def next_versions(self, rev, path, **args):
        with self.hgrepo() as repo:
            return repo.log(files=[self.full_path(path)], revrange='%s::' % rev.changeset,
                            **args)

    def previous_versions(self, rev, path, **args):
        with self.hgrepo() as repo:
            return repo.log(files=[self.full_path(path)], revrange='::%s' % rev.changeset,
                            **args)

    def root(self):
        with self.hgrepo() as repo:
            return repo.root()

    def head(self, path=None, **args):
        if path is not None:
            assert 'files' not in args
            args['files'] = [self.full_path(path)]
        with self.hgrepo() as repo:
            try:
                logs = repo.log(limit=1, removed=True, **args)
            except CommandError as exc:
                if 'unknown revision' in exc.err:
                    return None
                raise
        if logs:
            return logs[0]
        return None

    def log(self, path=None, **args):
        args.setdefault('removed', True)
        with self.hgrepo() as repo:
            if path is not None:
                args['files'] = [self.full_path(path)]
            return repo.log(**args)

    def log_rset(self, path=None, **args):
        """Returns a ResultSet of the Revisions
        """
        args.setdefault('removed', True)
        log = self.log(path, **args)
        # XXX what a funny joke
        # we need to split the big IN into several queries to
        # prevent a "Too many SQL variables" error
        rsets = []
        # itertools grouper pattern
        args = [iter(log)] * 50
        for partiallog in izip_longest(fillvalue=None, *args):
            rql = ('Revision R ORDERBY R DESC WHERE '
                   'R from_repository REPO, REPO eid %%(x)s, R changeset IN (%s)'
                   % ','.join('"%s"' % rev.node[:12].decode('ascii')
                              for rev in partiallog if rev is not None))
            rsets.append(self._cw.execute(rql,
                                          {'x': self.entity.eid}))
        if rsets:
            return reduce(lambda x, y: x+y, rsets)
        return self._cw.empty_rset()

    def status(self, cset):
        with self.hgrepo() as repo:
            return repo[cset].files()

    def cat(self, rev, path):
        with self.hgrepo() as repo:
            return repo.cat([self.full_path(path)], rev=rev)

    def strip_cset(self, cset):
        with self.hgrepo() as repo:
            args = cmdbuilder('strip', cset)
            repo.rawcommand(args)

    def add_revision(self, description, author, branch, parent, added, deleted):
        tmpdir = tempfile.mkdtemp()
        hglib.clone(self.path, tmpdir, rev=parent, updaterev=parent)
        try:
            with hglib.open(tmpdir) as client:
                if branch is not None:
                    client.branch(branch, force=True)
                for (file, content) in added:
                    path = osp.realpath(osp.join(tmpdir, file))
                    assert path.startswith(osp.realpath(tmpdir))
                    try:
                        os.makedirs(osp.dirname(path))
                    except OSError as exc:
                        if exc.errno != errno.EEXIST:
                            raise
                    with open(path, 'wb') as f:
                        while True:
                            buf = content.read(4096)
                            if not buf:
                                break
                            f.write(buf)
                for file in deleted:
                    path = osp.realpath(osp.join(tmpdir, file))
                    assert path.startswith(osp.realpath(tmpdir))
                    try:
                        os.unlink(path)
                    except OSError as exc:
                        if exc.errno == errno.ENOENT:
                            raise QueryError('%s is already deleted from the vcs' % file)
                        raise
                rev, cset = client.commit(message=description, addremove=True, user=author)
                client.push(rev=cset, force=True)
                return cset[:12]
        finally:
            shutil.rmtree(tmpdir)

    def pull(self):
        self._create_repo()
        if self.entity.source_url:
            with self.hgrepo() as hgrepo:
                try:
                    hgrepo.pull(source=self.entity.source_url)
                except CommandError as exc:
                    raise EnvironmentError('pull or clone from %s failed %s' %
                                           (self.entity.source_url, exc))

    def import_content(self, commitevery):
        cnx = self._cw
        try:
            self.pull()
        except EnvironmentError as exc:
            # repo at source_url may not be available, notify it but
            # go on since there might have new commits in local cache
            self.warning(str(exc))
        with self.hgrepo() as hgrepo:
            rset = cnx.execute('Any CSET WHERE R eid %(r)s, X from_repository R, '
                               'NOT CREV parent_revision X, X changeset CSET',
                               {'r': self.entity.eid})
            # we don't want no unicode
            knownheads = [str(row[0]) for row in rset]
            # detect stripped branches
            needsstrip = False
            while knownheads:
                # 100 at a time so we don't crash hg in a deep recursion
                csets = knownheads[:100]
                knownheads = knownheads[100:]
                try:
                    hgrepo.log(csets)
                except CommandError:
                    needsstrip = True
                    self.warning('%s: strip detected. One of %s is unknown in local cache',
                                 self.path, csets)
                    break

            if needsstrip:
                self.warning('%s: strip from %s.',
                             self.entity.dc_title(), self.path)
                revs = cnx.execute('Any R WHERE R is Revision, R from_repository REPO, '
                                   'REPO eid %(reid)s', {'reid': self.entity.eid})
                for reventity in revs.entities():
                    try:
                        hgrepo.log(reventity.changeset)
                    except CommandError:
                        reventity.cw_delete()

                cnx.commit()

            # update phases and visibility of already known revisions
            self.update_phases(cnx, hgrepo)
            self.update_hidden(cnx, hgrepo)
            # XXX we need to update obsolescence markers without new revision
            #     involved.
            # XXX the below would be a bit nicer, but makes mercurial explode due to too deep recursion
            #rset = cnx.execute(
            #        'Any CSET WHERE R eid %(r)s, X from_repository R, '
            #        'NOT CREV parent_revision X, X changeset CSET',
            #        {'r': self.entity.eid})
            #knownheads_cs = [str(row[0]) for row in rset if str(row[0]) in hgrepo]
            #revrange = ' and '.join(('not(::%s)' % i) for i in knownheads_cs) if knownheads_cs else None
            #missing = [int(rev[0]) for rev in hgrepo.log(revrange=revrange)]
            # XXX so we use this, which seems to need a lot of cpu instead :(
            rset = cnx.execute(
                    'Any CSET WHERE R eid %(r)s, X from_repository R, X changeset CSET',
                    {'r': self.entity.eid})
            knowncs = frozenset(str(row[0]) for row in rset)
            missing = sorted(int(rev[0]) for rev in hgrepo.log() if rev[1][:12] not in knowncs)
            missing.sort()
            while missing:
                for rev in missing[:commitevery]:
                    try:
                        self.import_revision(hgrepo, rev)
                    except Exception:
                        self.critical('error while importing revision %s of %s',
                                      rev, self.path, exc_info=True)
                        raise
                cnx.commit()
                del missing[:commitevery] # pop iterated value
            cnx.commit()

    def update_phases(self, cnx, hgrepo):
        """ update all phases (this potentially affects all revs since
        phase changes are not transactional) """
        repoeid = self.entity.eid
        for phase in (u'public', u'draft', u'secret'):
            revs = set(ctx.node[:12] for ctx in hgrepo.log(revrange='%s()' % phase))
            if revs:
                cnx.execute('SET R phase %%(phase)s WHERE R changeset IN (%s),'
                            'NOT R phase %%(phase)s, R from_repository REPO,'
                            'REPO eid %%(repo)s' %
                            ','.join(repr(rev) for rev in revs),
                            {'repo': repoeid, 'phase': phase})

    def update_hidden(self, cnx, hgrepo):
        """ maintain hidden status for all revs """
        repoeid = self.entity.eid
        oldhidden = set(num for num, in cnx.execute('Any CS WHERE R hidden True, '
                                                    'R from_repository H, '
                                                    'R changeset CS, H eid %(hg)s',
                                                    {'hg': repoeid}).rows)
        newhidden = set(rev.node[:12] for rev in hgrepo.log(revrange='hidden()'))
        hide = newhidden - oldhidden
        show = oldhidden - newhidden
        for revs, setto in ((hide, 'True'), (show, 'False')):
            if revs:
                cnx.execute('SET R hidden %s WHERE R from_repository H,'
                            'H eid %%(hg)s, R changeset IN (%s)' %
                            (setto, ','.join('"%s"' % cs for cs in revs)),
                            {'hg': self.entity.eid})

        # very partial handling of obsolescence relation added after a revision
        # issue #2731056
        # this tries to find explanation for changeset that becomes hidden
        # - does not work for changesets already hidden
        # - does not work for public changesets
        for new_hide in hide:
            ctx = hgrepo[new_hide]
            RQL = '''SET S obsoletes P
                     WHERE R eid %(r)s,
                     P from_repository R,
                     P changeset %(p)s,
                     S from_repository R,
                     S changeset %(s)s,
                     NOT S obsoletes P
            '''
            # unknown successors will create the relation at insertion time
            data = {'r': self.entity.eid,
                    'p': str(ctx)}
            successors_changesets = [cs.node[:12] for cs in hgrepo.log(revrange='successors(%s)' % ctx.node())]
            for succ in successors_changesets:
                data['s'] = str(succ)
                cnx.execute(RQL, data)

    def import_revision(self, hgrepo, i):
        self.info('importing revision %s from %s', i, self.entity.dc_title())
        cnx = self._cw
        execute = cnx.execute
        ctx = hgrepo[i]
        ctx_hex = ctx.node()[:12]
        if self.entity_for_cset(ctx_hex):
            self.warning('skip revision %s, seems already imported', ctx_hex)
            return
        revdata = {'date': ctx.date(),
                   'author': unicode(ctx.author(), self.entity.encoding),
                   'description': unicode(ctx.description(), self.entity.encoding),
                   'changeset': unicode(ctx_hex, self.entity.encoding),
                   'phase': unicode(ctx.phase()),
                   'branch': unicode(ctx.branch()),
                   'hidden': ctx.hidden(),
                   'vcstags': u','.join(ctx.tags()),
                   }
        # truncate author field if it's too long
        constraint = cnx.vreg.schema['Revision'].rdef('author').constraint_by_type('SizeConstraint')
        if constraint and constraint.max and len(revdata['author']) > constraint.max:
            revdata['author'] = revdata['author'][:constraint.max - 1] + u'…'
        #XXX workaround, parents may return None
        parent_changesets = hgrepo.parents(ctx_hex)
        parent_changesets = [n.node[:12] for n in parent_changesets] if parent_changesets else []
        precursors_changesets = [cs.node[:12] for cs in hgrepo.log(revrange='allprecursors(%s)' % i)]
        if not precursors_changesets:
            precursors = []
        else:
            precursors = execute(
                    'Any X WHERE X changeset XC, '
                    'X changeset IN (%s), X from_repository R, R eid %%(r)s'
                    % ','.join("'%s'" % cs for cs in precursors_changesets),
                    {'r': self.entity.eid})
        revdata['precursors'] = [p[0] for p in precursors]
        if not parent_changesets:
            parents = []
        else:
            parents = execute(
                    'Any X,XC WHERE X changeset XC, '
                    'X changeset IN (%s), X from_repository R, R eid %%(r)s'
                    % ','.join("'%s'"%cs for cs in parent_changesets),
                    {'r': self.entity.eid})
        revdata['parents'] = [r[0] for r in parents]
        reveid = bridge.import_revision(cnx, self.entity.eid, **revdata)
