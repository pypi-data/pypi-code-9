# -*- coding: utf-8 -*-
#
# Copyright (C) 2012-2013 Edgewall Software
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://trac.edgewall.org/wiki/TracLicense.
#
# This software consists of voluntary contributions made by many
# individuals. For the exact contribution history, see the revision
# history and logs, available at http://trac.edgewall.org/log/.

from __future__ import with_statement

import unittest
from datetime import datetime, timedelta

from trac.perm import DefaultPermissionPolicy, DefaultPermissionStore,\
                      PermissionCache
from trac.test import Mock, EnvironmentStub
from trac.ticket import default_workflow, web_ui
from trac.ticket.batch import BatchModifyModule
from trac.ticket.model import Ticket
from trac.util.datefmt import utc
from trac.web.chrome import web_context


class BatchModifyTestCase(unittest.TestCase):

    def setUp(self):
        self.env = EnvironmentStub(default_data=True,
            enable=[default_workflow.ConfigurableTicketWorkflow,
                    DefaultPermissionPolicy, DefaultPermissionStore,
                    web_ui.TicketModule])
        self.env.config.set('trac', 'permission_policies',
                            'DefaultPermissionPolicy')
        self.req = Mock(href=self.env.href, authname='anonymous', tz=utc)
        self.req.session = {}
        self.req.perm = PermissionCache(self.env)

    def assertCommentAdded(self, ticket_id, comment):
        ticket = Ticket(self.env, int(ticket_id))
        changes = ticket.get_changelog()
        comment_change = [c for c in changes if c[2] == 'comment'][0]
        self.assertEqual(comment_change[2], comment)

    def assertFieldChanged(self, ticket_id, field, new_value):
        ticket = Ticket(self.env, int(ticket_id))
        changes = ticket.get_changelog()
        field_change = [c for c in changes if c[2] == field][0]
        self.assertEqual(field_change[4], new_value)

    def _change_list_test_helper(self, original, new, new2, mode):
        batch = BatchModifyModule(self.env)
        return batch._change_list(original, new, new2, mode)

    def _add_list_test_helper(self, original, to_add):
        return self._change_list_test_helper(original, to_add, '', '+')

    def _remove_list_test_helper(self, original, to_remove):
        return self._change_list_test_helper(original, to_remove, '', '-')

    def _add_remove_list_test_helper(self, original, to_add, to_remove):
        return self._change_list_test_helper(original, to_add, to_remove,
                                             '+-')

    def _assign_list_test_helper(self, original, new):
        return self._change_list_test_helper(original, new, '', '=')

    def _insert_ticket(self, summary, **kw):
        """Helper for inserting a ticket into the database"""
        ticket = Ticket(self.env)
        for k, v in kw.items():
            ticket[k] = v
        return ticket.insert()

    def test_ignore_summary_reporter_and_description(self):
        """These cannot be added through the UI, but if somebody tries
        to build their own POST data they will be ignored."""
        batch = BatchModifyModule(self.env)
        self.req.args = {}
        self.req.args['batchmod_value_summary'] = 'test ticket'
        self.req.args['batchmod_value_reporter'] = 'anonymous'
        self.req.args['batchmod_value_description'] = 'synergize the widgets'
        values = batch._get_new_ticket_values(self.req)
        self.assertEqual(len(values), 0)

    def test_add_batchmod_value_data_from_request(self):
        batch = BatchModifyModule(self.env)
        self.req.args = {}
        self.req.args['batchmod_value_milestone'] = 'milestone1'
        values = batch._get_new_ticket_values(self.req)
        self.assertEqual(values['milestone'], 'milestone1')

    def test_selected_tickets(self):
        self.req.args = { 'selected_tickets' : '1,2,3' }
        batch = BatchModifyModule(self.env)
        selected_tickets = batch._get_selected_tickets(self.req)
        self.assertEqual(selected_tickets, ['1', '2', '3'])

    def test_no_selected_tickets(self):
        """If nothing is selected, the return value is the empty list."""
        self.req.args = { 'selected_tickets' : '' }
        batch = BatchModifyModule(self.env)
        selected_tickets = batch._get_selected_tickets(self.req)
        self.assertEqual(selected_tickets, [])

    # Assign list items

    def test_change_list_replace_empty_with_single(self):
        """Replace emtpy field with single item."""
        changed = self._assign_list_test_helper('', 'alice')
        self.assertEqual(changed, 'alice')

    def test_change_list_replace_empty_with_items(self):
        """Replace emtpy field with items."""
        changed = self._assign_list_test_helper('', 'alice, bob')
        self.assertEqual(changed, 'alice, bob')

    def test_change_list_replace_item(self):
        """Replace item with a different item."""
        changed = self._assign_list_test_helper('alice', 'bob')
        self.assertEqual(changed, 'bob')

    def test_change_list_replace_item_with_items(self):
        """Replace item with different items."""
        changed = self._assign_list_test_helper('alice', 'bob, carol')
        self.assertEqual(changed, 'bob, carol')

    def test_change_list_replace_items_with_item(self):
        """Replace items with a different item."""
        changed = self._assign_list_test_helper('alice, bob', 'carol')
        self.assertEqual(changed, 'carol')

    def test_change_list_replace_items(self):
        """Replace items with different items."""
        changed = self._assign_list_test_helper('alice, bob', 'carol, dave')
        self.assertEqual(changed, 'carol, dave')

    def test_change_list_replace_items_partial(self):
        """Replace items with different (or not) items."""
        changed = self._assign_list_test_helper('alice, bob', 'bob, dave')
        self.assertEqual(changed, 'bob, dave')

    def test_change_list_clear(self):
        """Clear field."""
        changed = self._assign_list_test_helper('alice bob', '')
        self.assertEqual(changed, '')

    # Add / remove list items

    def test_change_list_add_item(self):
        """Append additional item."""
        changed = self._add_list_test_helper('alice', 'bob')
        self.assertEqual(changed, 'alice, bob')

    def test_change_list_add_items(self):
        """Append additional items."""
        changed = self._add_list_test_helper('alice, bob', 'carol, dave')
        self.assertEqual(changed, 'alice, bob, carol, dave')

    def test_change_list_remove_item(self):
        """Remove existing item."""
        changed = self._remove_list_test_helper('alice, bob', 'bob')
        self.assertEqual(changed, 'alice')

    def test_change_list_remove_items(self):
        """Remove existing items."""
        changed = self._remove_list_test_helper('alice, bob, carol',
                                                'alice, carol')
        self.assertEqual(changed, 'bob')

    def test_change_list_remove_idempotent(self):
        """Ignore missing item to be removed."""
        changed = self._remove_list_test_helper('alice', 'bob')
        self.assertEqual(changed, 'alice')

    def test_change_list_remove_mixed(self):
        """Ignore only missing item to be removed."""
        changed = self._remove_list_test_helper('alice, bob', 'bob, carol')
        self.assertEqual(changed, 'alice')

    def test_change_list_add_remove(self):
        """Remove existing item and append additional item."""
        changed = self._add_remove_list_test_helper('alice, bob', 'carol',
                                                'alice')
        self.assertEqual(changed, 'bob, carol')

    def test_change_list_add_no_duplicates(self):
        """Existing items are not duplicated."""
        changed = self._add_list_test_helper('alice, bob', 'bob, carol')
        self.assertEqual(changed, 'alice, bob, carol')

    def test_change_list_remove_all_duplicates(self):
        """Remove all duplicates."""
        changed = self._remove_list_test_helper('alice, bob, alice', 'alice')
        self.assertEqual(changed, 'bob')

    # Save

    def test_save_comment(self):
        """Comments are saved to all selected tickets."""
        first_ticket_id = self._insert_ticket('Test 1', reporter='joe')
        second_ticket_id = self._insert_ticket('Test 2', reporter='joe')
        selected_tickets = [first_ticket_id, second_ticket_id]

        batch = BatchModifyModule(self.env)
        batch._save_ticket_changes(self.req, selected_tickets, {}, 'comment',
                                   'leave')

        self.assertCommentAdded(first_ticket_id, 'comment')
        self.assertCommentAdded(second_ticket_id, 'comment')

    def test_save_values(self):
        """Changed values are saved to all tickets."""
        first_ticket_id = self._insert_ticket('Test 1', reporter='joe',
                                              component='foo')
        second_ticket_id = self._insert_ticket('Test 2', reporter='joe')
        selected_tickets = [first_ticket_id, second_ticket_id]
        new_values = { 'component' : 'bar' }

        batch = BatchModifyModule(self.env)
        batch._save_ticket_changes(self.req, selected_tickets, new_values, '',
                                   'leave')

        self.assertFieldChanged(first_ticket_id, 'component', 'bar')
        self.assertFieldChanged(second_ticket_id, 'component', 'bar')

    def test_action_with_state_change(self):
        """Actions can have change status."""
        self.env.config.set('ticket-workflow', 'embiggen', '* -> big')

        first_ticket_id = self._insert_ticket('Test 1', reporter='joe',
                                              status='small')
        second_ticket_id = self._insert_ticket('Test 2', reporter='joe')
        selected_tickets = [first_ticket_id, second_ticket_id]

        batch = BatchModifyModule(self.env)
        batch._save_ticket_changes(self.req, selected_tickets, {}, '',
                                   'embiggen')

        self.assertFieldChanged(first_ticket_id, 'status', 'big')
        self.assertFieldChanged(second_ticket_id, 'status', 'big')

    def test_action_with_side_effects(self):
        """Actions can have operations with side effects."""
        self.env.config.set('ticket-workflow', 'buckify', '* -> *')
        self.env.config.set('ticket-workflow', 'buckify.operations',
                                               'set_owner')
        self.req.args = {}
        self.req.args['action_buckify_reassign_owner'] = 'buck'

        first_ticket_id = self._insert_ticket('Test 1', reporter='joe',
                                              owner='foo')
        second_ticket_id = self._insert_ticket('Test 2', reporter='joe')
        selected_tickets = [first_ticket_id, second_ticket_id]

        batch = BatchModifyModule(self.env)
        batch._save_ticket_changes(self.req, selected_tickets, {}, '',
                                   'buckify')

        self.assertFieldChanged(first_ticket_id, 'owner', 'buck')
        self.assertFieldChanged(second_ticket_id, 'owner', 'buck')

    def test_timeline_events(self):
        """Regression test for #11288"""
        tktmod = web_ui.TicketModule(self.env)
        now = datetime.now(utc)
        start = now - timedelta(hours=1)
        stop = now + timedelta(hours=1)
        events = tktmod.get_timeline_events(self.req, start, stop,
                                            ['ticket_details'])
        self.assertEqual(True, all(ev[0] != 'batchmodify' for ev in events))

        ids = []
        for i in xrange(20):
            ticket = Ticket(self.env)
            ticket['summary'] = 'Ticket %d' % i
            ids.append(ticket.insert())
        ids.sort()
        new_values = {'summary': 'batch updated ticket',
                      'owner': 'ticket11288', 'reporter': 'ticket11288'}
        batch = BatchModifyModule(self.env)
        batch._save_ticket_changes(self.req, ids, new_values, '', 'leave')
        # shuffle ticket_change records
        with self.env.db_transaction as db:
            rows = db('SELECT * FROM ticket_change')
            db.execute('DELETE FROM ticket_change')
            rows = rows[0::4] + rows[1::4] + rows[2::4] + rows[3::4]
            db.executemany('INSERT INTO ticket_change VALUES (%s)' %
                           ','.join(('%s',) * len(rows[0])),
                           rows)

        events = tktmod.get_timeline_events(self.req, start, stop,
                                            ['ticket_details'])
        events = [ev for ev in events if ev[0] == 'batchmodify']
        self.assertEqual(1, len(events))
        batch_ev = events[0]
        self.assertEqual('anonymous', batch_ev[2])
        self.assertEqual(ids, sorted(batch_ev[3][0]))
        self.assertEqual('updated', batch_ev[3][1])

        context = web_context(self.req)
        self.assertEqual(
            self.req.href.query(id=','.join(str(t) for t in ids)),
            tktmod.render_timeline_event(context, 'url', batch_ev))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BatchModifyTestCase))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
