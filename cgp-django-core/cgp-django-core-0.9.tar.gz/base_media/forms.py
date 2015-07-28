from django import forms
from django.db import models
from django.contrib import admin
from django.forms import widgets
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.html import escape

from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import *

class BaseAdminImageAddForm(forms.ModelForm):

    def full_clean(self):
        title_field = self.fields['title']
        title_field.required = False

        image_field = self.fields['image']
        image_field.required = True

        return super(BaseAdminImageAddForm, self).full_clean()
    

class BaseAdminDocumentAddForm(forms.ModelForm):
    
    def full_clean(self):
        title_field = self.fields['title']
        title_field.required = False

        media_field = self.fields['media_file']
        media_field.required = True

        return super(BaseAdminDocumentAddForm, self).full_clean()   


class BaseImageAddForm(forms.ModelForm):
    
    next = forms.CharField(required=False,)

    class Meta:
        fields = ['title','credit','image', 'users']

    def __init__(self, *args, **kwargs): 
        super(BaseImageAddForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(BaseImageAddForm, self).save(commit=False)
        if not instance.pk:
            instance.creator = self.cleaned_data['users'][0]
        instance.save()                
        #instance.users.clear()
        
        
        for user in self.cleaned_data['users']:
            instance.users.add(user)
        return instance

class BaseDocumentAddForm(forms.ModelForm):
    
    next = forms.CharField(required=False,)

    class Meta:
        fields = ['title','media_file', 'users']

    def __init__(self, *args, **kwargs): 
        super(BaseDocumentAddForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(BaseDocumentAddForm, self).save(commit=False)
        if not instance.pk:
            instance.creator = self.cleaned_data['users'][0]
        instance.save()                
        #instance.users.clear()
        
        
        for user in self.cleaned_data['users']:
            instance.users.add(user)
        return instance     


class SecureDocumentSetCreateForm(forms.ModelForm):
    class Meta:
        fields = ['title','description','expiration_date']


class SecureDocumentItemAccessForm(forms.Form):
    
    password = forms.CharField(widget=forms.PasswordInput)

class SecureDocumentSetAccessForm(forms.Form):
    
    password = forms.CharField(widget=forms.PasswordInput)

    


class SecureDocumentSetPasswordChangeForm(forms.Form):
    """
    A form used to change the password of a user in the admin interface.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password (again)"),
                                widget=forms.PasswordInput)

    def __init__(self, set, *args, **kwargs):
        self.set = set
        super(SecureDocumentSetPasswordChangeForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        """
        Saves the new password.
        """
        self.set.set_password(self.cleaned_data["password1"])
        if commit:
            self.set.save()
        return self.set

    def _get_changed_data(self):
        data = super(SecureDocumentSetPasswordChangeForm, self).changed_data
        for name in self.fields.keys():
            if name not in data:
                return []
        return ['password']
    changed_data = property(_get_changed_data)


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

class SecureDocumentItemChangeForm(SetPasswordForm):
    # password = PasswordHashField(label=_("Password"))
    class Meta:
        fields = ['title','description','expiration_date', 'password']

class SecureDocumentSetChangeForm(SetPasswordForm):

    class Meta:
        fields = ['title','description','expiration_date', 'password']




# class MediaSetForm(forms.ModelForm):
#     class Meta:
#         model = MediaSet

#     media_items = forms.ModelMultipleChoiceField(queryset=Media.objects.all())

#     def __init__(self, *args, **kwargs):
#         super(MediaSetForm, self).__init__(*args, **kwargs)
#         if self.instance:
#             self.fields['media_items'].initial = self.instance.media_set.all()

#     def save(self, *args, **kwargs):
#         # FIXME: 'commit' argument is not handled
#         # TODO: Wrap reassignments into transaction
#         # NOTE: Previously assigned Foos are silently reset
#         instance = super(MediaSetForm, self).save(commit=False)
#         self.fields['media_items'].initial.update(parent_set=None)
#         self.cleaned_data['media_items'].update(parent_set=instance)
#         return instance