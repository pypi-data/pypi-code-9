from django.conf.urls.static import static
from django.conf.urls import patterns, url, include

from .views import *

urlpatterns = patterns('',
    
    # url( r'^media/images/$', ImageListView.as_view(), name='image_list_view'), 
    # url( r'^media/images/add/$', ImageAddView.as_view(), name='image_add_view'),  
    # url( r'^media/images/(?P<pk>\d+)/edit/$', ImageEditView.as_view(), name='image_edit_view'),  
    # url( r'^media/images/(?P<pk>\d+)/delete/$', ImageDeleteView.as_view(), name='image_delete_view'),  
    # url( r'^media/imagepicker/$', ImagepickerView.as_view(), name='imagepicker_view'),  
    # #url( r'^media/documents/$', DocumentListView.as_view(), name='document_list_view'),  
    # # url( r'^media/documents/add/$', DocumentAddView.as_view(), name='document_add_view'),  
    # url(r'admin/media/image_mediapicker$', ImageMediaPicker.as_view(), name="admin_image_media_mediapicker"), 

    # url(r'admin/media/images/batch/$', ImageBatchView.as_view(), name="admin_image_batch_view"), 
    # url(r'admin/media/secureimages/batch/$', SecureImageBatchView.as_view(), name="admin_secureimage_batch_view"), 
    # url(r'admin/media/documents/batch/$', DocumentBatchView.as_view(), name="admin_document_batch_view"), 
    # url(r'admin/media/securedocuments/batch/$', SecureDocumentBatchView.as_view(), name="admin_securedocument_batch_view"), 

  
    # url( r'^media/images/(?P<pk>\d+)/(?P<variant_name>[\w-]+)/$', ImageVariantRedirectView.as_view(), name='image_variant_redirect_view'),  
    # url( r'^media/documents/(?P<pk>\d+)/$', DocumentRedirectView.as_view(), name='document_redirect_view'),  
    # url(r'^secure/document/(?P<slug>[\w-]+)/$', SecureDocumentView.as_view(), name='secure_document_view'),
    # url(r'^secure/documents/(?P<slug>[\w-]+)/$', SecureDocumentSetView.as_view(), name='secure_document_set_view'),
    # url(r'^secure/documents/(?P<slug>[\w-]+)/access/$', SecureDocumentSetAccessView.as_view(), name='secure_document_access_view'),
    # url(r'^secure/documents/(?P<slug>[\w-]+)/expired/$', SecureDocumentSetExpiredView.as_view(), name='secure_document_expired_view'),
    # url(r'^secure/documents/(?P<set_slug>[\w-]+)/(?P<slug>[\w-]+)/$', SecureDocumentSetItemView.as_view(), name='secure_document_set_item_view'),
    
)

