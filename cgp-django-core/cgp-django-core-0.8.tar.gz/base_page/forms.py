from django import forms
from django.conf import settings

from ckeditorfiles.widgets import CKEditorWidget


# ------------------------------------------------------------------------------
#  CK RICH TEXT EDITOR CONFIGS
# ------------------------------------------------------------------------------

CKEDITOR_TOOLBAR = {
    #'filebrowserImageBrowseUrl': '/admin/media/mediapicker',
    #'filebrowserImageWindowWidth': '640',
    #'filebrowserImageWindowHeight': '480',
    'height': '500px',
    'toolbar': [
        {
            'name': 'styles',
            'items': ['Format','Styles']
        },
        {
            'name': 'basicstyles',
            'items': ['Bold', 'Italic', 'Underline']
        },
        {
            'name': 'semantic',
            'items': ['Superscript']
        },
        {
            'name': 'paragraph',
            'groups': ['list'],
            'items': ['NumberedList', 'BulletedList', 'Blockquote']
        },
        {
            'name': 'media',
            'items': ['Image', 'CreateDiv']
        },
        {
            'name': 'links',
            'items': ['Link', 'Unlink', 'Anchor']
        },
        {
            'name': 'insert',
            'items': ['HorizontalRule', 'SpecialChar']
        },
        {
            'name': 'pasting',
            'items': ['PasteText', 'PasteFromWord', 'RemoveFormat']
        },
        {
            'name': 'tools',
            'items': ['Maximize']
        },
        {
            'name': 'source',
            'items': ['Source']
        }
    ],
    'allowedContent' : 
        'h1 h2 h3 p blockquote strong em sup u;'\
        'ol ul li;'\
        'figure{width,height,display,float};'\
        'figcaption;'\
        'img[!src,alt,width,height,align,data-caption];'\
        'div;',
    'removeButtons' : '',
    'stylesSet' :  [
        { 
            'name': 'Section Title', 
            'element': 'h2', 
            'attributes': {
                'class': "section-title"
            },
        },
        { 
            'name': 'Leadin', 
            'element': 'p', 
            'attributes': {
                'class': "leadin"
            }
        }
    ]
}

class PageContentWidget(CKEditorWidget):
    try:
        default_config = settings.PAGES_CKEDITOR_TOOLBAR        
    except AttributeError:
        default_config = CKEDITOR_TOOLBAR


class LinkItemForm(forms.ModelForm):
    # class Meta:
    #     model = LinkItem
    
    def __init__(self, *args, **kwargs):
        super(LinkItemForm, self).__init__(*args, **kwargs)
        self.fields['content_type'].help_text = 'To set this link to an existing\
        item in the cms, choose a Content Type and Object ID.'
        
        self.fields['path_override'].help_text = 'To set this link to an external \
        URL or absolute path, use the Path Override field.<br /><br />\
        External URLs should use this format "http://www.example.com" and absolute \
        URLs should use this format "/path/to/page/"'

