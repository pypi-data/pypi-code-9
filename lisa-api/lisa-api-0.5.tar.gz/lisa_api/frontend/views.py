from django.shortcuts import render, RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from lisa_api.lisa.plugin_manager import PluginManager
from distutils.version import StrictVersion
from lisa_api.lisa.logger import logger
from django.http import HttpResponseNotFound, HttpResponse
import requests
import mistune


@login_required()
def dashboard(request):
    context_instance = RequestContext(request)
    return render(request, 'dashboard.html', context_instance)


def _get_global_plugins():
    r = requests.get('https://raw.githubusercontent.com/project-lisa/lisa/master/lisa-plugins/lisa-plugins.json')
    if r.ok:
        logger.debug('Refreshing plugin list')
        lisa_all_plugins = r.json()
        return lisa_all_plugins
    else:
        return False


@login_required()
def plugin_changelog(request, plugin_name=None):
    lisa_all_plugins = request.session.get('lisa_all_plugins', False)
    if lisa_all_plugins:
        for remote_plugin in lisa_all_plugins:
            if remote_plugin == plugin_name:
                plugin = lisa_all_plugins[plugin_name]
                user, repo = plugin['repo_url'].split("/")[-2:]
                changelog_request = requests.get(
                    'https://raw.githubusercontent.com/{user}/{repo}/master/{changelog_file}'.format(
                        user=user,
                        repo=repo,
                        changelog_file='CHANGELOG.md'
                    )
                )
                if changelog_request.ok:
                    return HttpResponse(mistune.markdown(changelog_request.content.decode()))
                else:
                    return HttpResponseNotFound("<h4>The plugin's changelog was not found on his repository</h4>")
        return HttpResponseNotFound('<h4>The plugin was not found on the plugin list</h4>')
    return HttpResponseNotFound('<h4>The plugin was not found on the plugin list</h4>')


@login_required
@ensure_csrf_cookie
def plugins(request):
    pm = PluginManager()

    lisa_all_plugins = _get_global_plugins()
    if lisa_all_plugins:
        request.session['lisa_all_plugins'] = lisa_all_plugins
        lisa_template_plugins = {}

        for plugin_name in lisa_all_plugins:
            plugin = lisa_all_plugins[plugin_name]

            local_version = pm.get_version(plugin_name=plugin_name)
            if not local_version:
                local_version = False

            is_enabled = False
            if plugin_name in pm.plugins:
                is_enabled = True

            should_upgrade = False
            if local_version:
                if StrictVersion(local_version) < StrictVersion(plugin['version']):
                    should_upgrade = True

            lisa_template_plugins[plugin_name] = {
                'name': plugin['name'],
                'remote_version': plugin['version'],
                'local_version': local_version,
                'summary': plugin['summary'],
                'is_enabled': is_enabled,
                'should_upgrade': should_upgrade,
                'author': plugin['author'],
                'repo_url': plugin['repo_url'],
                'keywords': plugin['keywords']
            }
        context = {
            'lisa_plugins': lisa_template_plugins
        }
    else:
        context = {'error': 'Could not retrieve the plugin list'}
    context_instance = RequestContext(request)
    return render(request, 'plugins.html', context, context_instance)
