"""tracker test application"""

from datetime import date

from cubicweb.devtools.testlib import CubicWebTC, AutomaticWebTest


class AutomaticWebTest(AutomaticWebTest):

    def to_test_etypes(self):
        return set(('Project', 'Ticket', 'Version'))

    def list_startup_views(self):
        return ('stats', 'versionsinfo')

    def post_populate(self, cnx):
        cnx.commit()
        for version in cnx.execute('Version X').entities():
            version.cw_adapt_to('IWorkflowable').change_state('published')
        cnx.commit()


class VersionCalendarViews(CubicWebTC):
    """specific tests for calendar views"""

    def setup_database(self):
        with self.admin_access.repo_cnx() as cnx:
            cnx.create_entity('Version', num=u'0.1.0', publication_date=date(2006, 2, 1))
            cnx.create_entity('Version', num=u'0.2.0', publication_date=date(2006, 4, 1))
            cnx.create_entity('Project', name=u"MyProject")
            cnx.execute('SET V version_of P where V is Version, P is Project')
            cnx.commit()

    def test_calendars_for_versions(self):
        with self.admin_access.web_request() as req:
            rset = req.execute('Version V')
            for vid in ('onemonthcal', 'oneweekcal'):
                yield self.view, vid, rset, req.reset_headers()

if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
