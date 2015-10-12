from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from tribe_client import utils
from .app_settings import *
import json


def connect_to_tribe(request):
    if 'tribe_token' not in request.session:
        return render(request, 'establish_connection.html', {'tribe_url': TRIBE_URL, 'access_code_url': ACCESS_CODE_URL, 'client_id': TRIBE_ID, 'scope': 'write'})
    else:
        return display_genesets(request)

def logout_from_tribe(request):
    request.session.clear()
    return connect_to_tribe(request)

def get_token(request):
    access_code = request.GET.__getitem__('code')
    access_token = utils.get_access_token(access_code)
    request.session['tribe_token'] = access_token
    request.session['tribe_user'] = utils.retrieve_user_object(access_token)
    return redirect('display_genesets')

def display_genesets(request):
    if 'tribe_token' in request.session:
        access_token = request.session['tribe_token']
        get_user = utils.retrieve_user_object(access_token)

        if (get_user == 'OAuth Token expired' or get_user == []):
            request.session.clear()
            return connect_to_tribe(request)

        else:  # The user must be logged in and has access to her/himself
            genesets = utils.retrieve_user_genesets(access_token, {'full_genes': 'true', 'limit': 100})
            tribe_user = get_user
            return render(request, 'display_genesets.html', {'tribe_url': TRIBE_URL, 'genesets': genesets, 'tribe_user': tribe_user})

    else:
        return connect_to_tribe(request)

def display_versions(request, geneset):
    if 'tribe_token' in request.session:
        access_token = request.session['tribe_token']
        get_user = utils.retrieve_user_object(access_token)

        if (get_user == 'OAuth Token expired' or get_user == []):
            request.session.clear()
            return connect_to_tribe(request)

        else:
            versions = utils.retrieve_user_versions(access_token, geneset)
            for version in versions:
                version['gene_list'] = []
                for annotation in version['annotations']:
                    version['gene_list'].append(annotation['gene']['standard_name'])
            return render(request, 'display_versions.html', {'versions': versions})

def return_access_token(request):
    if 'tribe_token' in request.session:
        data = { 'access_token': request.session['tribe_token'] }
    else:
        data = { 'access_token': 'No access token' }
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')

def create_geneset(request):

    geneset_info = request.POST.get('geneset')
    geneset_info = json.loads(geneset_info)
    genes = request.POST.get('genes')
    genes = genes.split(",")
    num_genes = len(genes)
    geneset_info['selectedGenes'] = genes
    geneset_info['xrdb'] = CROSSREF
    geneset_info['description'] = 'Initial version containing the first ' + str(num_genes) + ' genes.'

    if 'tribe_token' in request.session:
        tribe_token = request.session['tribe_token']
        is_token_valid = utils.retrieve_user_object(tribe_token)
        if (is_token_valid =='OAuth Token expired'):
            tribe_token = None
            tribe_response = {'response': 'Not Authorized'}
        else:
            tribe_response = utils.create_remote_geneset(tribe_token, geneset_info)
            slug = tribe_response['slug']
            creator = tribe_response['creator']['username']

            geneset_url = TRIBE_URL + "/#/use/detail/" + creator + "/" + slug
            tribe_response = {'geneset_url': geneset_url}


    else:
        tribe_token = None
        tribe_response = {'response': 'Not Authorized'}

    json_response = json.dumps(tribe_response)

    return HttpResponse(json_response, content_type='application/json')

def return_user_obj(request):

    if 'tribe_token' in request.session:
        tribe_token = request.session['tribe_token']

    else:
        tribe_token = None

    tribe_response = utils.return_user_object(tribe_token)

    json_response = json.dumps(tribe_response)
    return HttpResponse(json_response, content_type='application/json')