# In forms.py...
from django import forms
from django.forms.util import flatatt
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.html import format_html, format_html_join
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX, identify_hasher

class UploadFileForm(forms.Form):
    file  = forms.FileField(required=True)



"""
Simple password update model form. Object should implement 'set_password(password)'
"""
class PasswordHashWidget(widgets.MultiWidget):


    def __init__(self, attrs=None):  
        
        _widgets = (
            widgets.TextInput(attrs={
                'readonly':'readonly', 
                'label':'password', 
                'style':'width:278px;margin-bottom:10px;'
            }), 
            widgets.TextInput(attrs={
                'label':'New Password', 
                'placeholder':"New Password", 
                # 'type':"password", 
                'style':'width:48%;margin-right:4%;'
            }),
            widgets.TextInput(attrs={
                'label':'New Password (repeat)', 
                'placeholder':"New Password (repeat)", 
                # 'type':"password", 
                'style':'width:48%;'
            }),
            widgets.CheckboxInput(attrs={
                # 'label':'Clear Password', 
                # 'style':'width:278px'
            }),
        )

        super(PasswordHashWidget, self).__init__(_widgets, attrs)
    
    def render(self, name, value, attrs=None):
        self.rendered_value = value
        self.id = attrs['id']

        return super(PasswordHashWidget, self).render(name, value, attrs)

    def decompress(self, value):
        if value:
            return [value, None, None, False]
        return [None, None, None, False]

    def format_output(self, rendered_widgets):
        
        #Indentify current password
        encoded = None if not self.rendered_value else self.rendered_value

        #Assemble password summary
        if not encoded or encoded.startswith(UNUSABLE_PASSWORD_PREFIX):
            summary = mark_safe(u"<strong>%s</strong>" % ugettext("No password set."))            
        else:
            try:
                hasher = identify_hasher(encoded)
            except ValueError:
                summary = mark_safe(u"<strong>%s</strong><br />" % ugettext(
                    "Invalid password format or unknown hashing algorithm."))
            else:
                summary = '<strong>Current Password:</strong> <br />'+format_html_join('',
                   u"<strong>{0}</strong>: {1} <br />",
                   ((ugettext(key), value)
                    for key, value in hasher.safe_summary(encoded).items())
                   )
        
        label_for_id = u"%s_3"%(self.id)
        rendered_checkbox = u'{0}<label for="{1}"><span>Clear password</span></label>'.format(rendered_widgets[3], label_for_id)
        return u'<table style="width:100%;border:0px;"><tr><td style="width: 278px;">{0}</td>\
            <td>{1}</td><td>{2}</td></tr></table>'.format(summary, u''.join(rendered_widgets[1:3]), rendered_checkbox)
        

    def value_from_datadict(self, data, files, name):
        #Return only the first password value
        default = [widget.value_from_datadict(data, files, name + '_%s' % i) for i, widget in enumerate(self.widgets)]
        return default



class PasswordHashField(forms.Field):
    widget = PasswordHashWidget

    def _has_changed(self, initial, data):
        if data[1] != None and data[1] != '':
            return True
        if data[3] == True:
            return True
        return False

class SetPasswordForm(forms.ModelForm):
    
    password = PasswordHashField(label=_("Password"))
    
    def clean_password(self):

        password = self.cleaned_data.get('password')
        password1 = password[1]
        password2 = password[2]
        clear_password = password[3]
        
        if clear_password:
            return ''        
        else:
            if(password1 and password1 != password2):
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )

            return password1

    def save(self, commit=True):
        
        item = super(SetPasswordForm, self).save(commit=False)        

        password = self.cleaned_data["password"]
        print 'Set password: %s'%(password)
        if password == '':
            item.password = None
        else:
            item.set_password(password)

        if commit:
            item.save()
        return item

