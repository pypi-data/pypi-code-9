from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render

from threebot.models import Workflow
from threebot_stats.utils import response_time_series, count_logs, impact
from threebot.utils import get_my_orgs


def index(request):
    return HttpResponse("Hello, world.")


def detail(request, workflow_slug):
    default_graph_items = 10
    orgs = get_my_orgs(request)
    workflow = get_object_or_404(Workflow, owner__in=orgs, slug=workflow_slug)
    graph_items = request.GET.get('graph-items', default_graph_items)

    try:
        graph_items = int(graph_items)
    except ValueError:
        graph_items = default_graph_items

    data = {
        'num_logs': count_logs(workflow),
        'impact': impact(workflow),
        'response_time_series': response_time_series(workflow, n=graph_items),
    }

    return render(request, 'threebot_stats/workflow_stats.html', {'data': data, 'workflow': workflow})
