from django import forms
from .models import Picture


class PicForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ('image', )


class CropForm(forms.Form):
    """Django form for accepting the information passed after cropping a loaded
    image
    """
    imgUrl = forms.CharField(max_length=250)  # your image path (the one we received after successful upload)
    imgInitW = forms.DecimalField() 	      # your image original width (the one we received after upload)
    imgInitH = forms.DecimalField()	          # your image original height (the one we received after upload)
    imgW = forms.DecimalField()		          # your new scaled image width
    imgH = forms.DecimalField()		          # your new scaled image height
    imgX1 = forms.DecimalField()		      # top left corner of the cropped image in relation to scaled image
    imgY1 = forms.DecimalField()		      # top left corner of the cropped image in relation to scaled image
    cropW = forms.DecimalField()		      # cropped image width
    cropH = forms.DecimalField()		      # cropped image height
