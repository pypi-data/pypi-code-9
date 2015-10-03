__author__ = 'vahid'

from tgext.crud import EasyCrudRestController

def just_editable_actions_maker(table_filler, obj):
    primary_fields = table_filler.__provider__.get_primary_fields(table_filler.__entity__)
    pklist = '/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
    #value = '<div><div>&nbsp;<a href="'+pklist+'/edit" style="text-decoration:none">edit</a></div></div>'
    return '''
    <a href="%s/edit" class="btn btn-primary">
        <span class="glyphicon glyphicon-pencil"></span>
    </a>
    ''' % pklist


class JustEditableCrudRestController(EasyCrudRestController):

    def post(self, *args, **kw):
        """This is not allowed."""
        pass

    def post_delete(self, *args, **kw):
        """This is not allowed."""
        pass
