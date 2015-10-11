from ftw.jsondump.interfaces import IPartial
from Products.CMFCore.utils import getToolByName
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


class WorkflowPartial(object):
    implements(IPartial)
    adapts(Interface, Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.data = {}

    def __call__(self, config):
        self.workflow_chain()
        self.workflow_history()
        return self.data

    def workflow_chain(self):
        workflows = {}
        self.data.update({'_workflow_chain': workflows})
        wftool = getToolByName(self.context, "portal_workflow")

        for wf_id in wftool.getChainForPortalType(self.context.portal_type):
            status = wftool.getStatusOf(wf_id, self.context)
            if status:
                workflows[wf_id] = status.get('review_state', '')

    def workflow_history(self):
        history = {}
        self.data.update({'_workflow_history': history})

        workflow_histories = getattr(self.context, 'workflow_history', {})
        for name, workflow_history in workflow_histories.items():
            history[name] = map(self.convert_history_entry, workflow_history)

    def convert_history_entry(self, workflow_history):
        return {'action': workflow_history['action'],
                'review_state': workflow_history['action'],
                'comments': workflow_history['comments'],
                'actor': workflow_history['actor'],
                'time': str(workflow_history['time'])}
