from __future__ import with_statement
from logilab.mtconverter import xml_escape

from cubicweb.predicates import is_instance, has_related_entities
from cubicweb.predicates import authenticated_user
from cubicweb.web.views.idownloadable import DownloadBox
from cubicweb.web.component import EntityCtxComponent
from cubicweb.web.views import primary, calendar
from cubicweb.web.views.ajaxcontroller import ajaxfunc

_ = unicode

class TalkPrimaryView(primary.PrimaryView):
    __select__ = is_instance('Talk',)

    def render_entity_title(self, entity):
        self.w(u'<h1><span class="etype">%s</span> %s</h1>'
               % (entity.dc_type().capitalize(), xml_escape(entity.dc_title())))
        self.w(u'<table class="talk"><tr><td>')
        self.render_talk_info(entity)
        self.w(u'</td><td>')
        self.w(u'</td></tr></table>')

    def render_talk_info(self, entity):
        self.w(u'<div>')
        self.w(u'<span class="speaker">%s %s</span>' % (
                self._cw._(u'Presented by'),
                self._cw.view('csv', entity.related('leads', 'object'),
                              subvid='outofcontext')))
        if entity.track:
            self.w(u' %s <span>' % self._cw._(u'in'))
            self.w(u'%s </span> ' % entity.track.view('incontext'))
        self.render_talk_time_place(entity)
        self.w(u'</div>')

    def render_talk_time_place(self, entity):
        _ = self._cw._
        if entity.start_time or entity.end_time:
            self.w(u'<span class="talktime">')
            if entity.start_time and entity.end_time:
                self.w(_(u"on %(sdate)s from %(stime)s to %(etime)s") %
                       ({'sdate': self._cw.format_date(entity.start_time),
                         'stime': self._cw.format_time(entity.start_time),
                         'etime': self._cw.format_time(entity.end_time)}))
            self.w(u'</span>')
        if entity.location:
            self.w(u'<span> %s %s</span>' % (_(u'in room'), xml_escape(entity.location)))

    def render_entity_attributes(self, entity):
        if entity.description:
            self.w(u'<h5>%s</h5>' % self._cw._(u'Abstract'))
            self.w(u'<div>%s</div>' % entity.dc_description('text/html'))

class AttendanceComponent(EntityCtxComponent):
    __regid__ = 'attendance'
    __select__ = (EntityCtxComponent.__select__ & is_instance('Talk') &
                  authenticated_user())
    context = 'ctxtoolbar'

    def init_rendering(self):
        _ = unicode
        self._cw.add_js('cubes.conference.js')
        user = self._cw.user
        eid = self.entity.eid
        rset = self._cw.execute('Any X WHERE U attend X, U eid %(u)s, X eid %(x)s',
                                {'u': user.eid, 'x': eid})
        if rset.rowcount:
            # user is already attending this talk
            self.klass = 'delete_attend'
            self.title = _('click here if you do not plan to attend this talk')
            self.label, self.label_id = _('You plan to attend'), 'attend'
        else:
            # user is not attending the talk
            self.klass = 'set_attend'
            self.title = _('click here if you plan to attend this talk')
            self.label, self.label_id = _('You do not plan to attend'), 'unattend'
        # count attendees
        rql = 'Any COUNT(U) WHERE U attend X, X eid %s' % eid
        self.nb_person = self._cw.execute(rql)[0][0]

    def render_body(self, w):
        w(u'<div class="%s" id="%s" data-eid="%s">' % (self.__regid__, self.domid, self.entity.eid))
        w(u'<div class="attendbutton %s" title="%s" id="%s">'
               u'<div id="attendinfo">%s</div><div>(%s %s)</div></div>'
               % (self.klass, self._cw._(self.title),
                  self.label_id, self._cw._(self.label), self.nb_person,
                  self._cw._('people plan to attend')))
        w(u'</div>')


@ajaxfunc
def conference_delete_attend(self, talkeid):
    usereid = self._cw.user.eid
    self._cw.execute('DELETE U attend X WHERE U eid %(u)s, X eid %(x)s', {'u': usereid, 'x': talkeid})

@ajaxfunc
def conference_set_attend(self, talkeid):
    usereid = self._cw.user.eid
    self._cw.execute('SET U attend X WHERE U eid %(u)s, X eid %(x)s', {'u': usereid, 'x': talkeid})


class TalkCalendarItem(calendar.CalendarItemView):
    __select__ = is_instance('Talk')

    def cell_call(self, row, col, dates=False):
        talk = self.cw_rset.complete_entity(row)
        persons = self._cw.execute('Any P WHERE P leads X, X eid %(x)s', {'x': talk.eid}).entities()
        self.w(u'<a href="%s">%s - %s</a>' % (talk.absolute_url(), xml_escape(talk.dc_title()),
                                              xml_escape(', '.join(p.dc_long_title() for p in persons))))
        if talk.location:
            self.w(u'<div>[%s %s]</div>' % (self._cw._(u'room'), talk.location))


class AttachmentsDownloadBox(DownloadBox):
    """A box containing all downloadable attachments of a Talk"""
    __regid__ = 'attachments_downloads_box'
    __select__ = is_instance('Talk') & has_related_entities('has_attachments', 'subject')
    title = _('Attachments')

    def init_rendering(self):
        self.items = self.entity.has_attachments
