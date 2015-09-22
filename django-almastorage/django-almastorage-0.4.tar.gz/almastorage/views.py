from django.shortcuts import render, render_to_response
from django.views.generic import ListView
from .models import SwiftFile, SwiftContainer
from django.http import HttpResponseRedirect
import swiftclient
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from .models import USERNAME, KEY, AUTH_URL

# class ContainerListView(ListView):
#     model = SwiftContainer
#     paginate_by = 10
#     queryset = SwiftFile.objects.all()
#     template_name='swift_file/templates/swift_file/swiftfile_list.html'
#     context_object_name = 'container'

# def upload_file(request):
#     if request.method == 'GET':
#         return render(request, 'swift_file/upload_form.html',{'form':UploadFileForm()})
#     elif request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         conn = swiftclient.Connection(user=USERNAME, key=KEY, authurl=AUTH_URL)
#         SwiftFile.upload_file(User.objects.first(), conn, request.FILES['file'].read(), request.FILES['file'].name, request.FILES['file'].content_type)
#         if form.is_valid():
#             return HttpResponseRedirect('/')
#         pass

def download_file(request, file_id):
    if request.method == 'GET':
        base_file = SwiftFile.objects.get(id=file_id)
        obj_tuple = base_file.download()
        response = HttpResponse(obj_tuple[1], content_type=base_file.content_type)
        response['Content-Disposition'] = 'attachment; filename='+base_file.filename.encode('utf-8')
        return response