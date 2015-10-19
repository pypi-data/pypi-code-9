# -*- encoding: utf-8 -*-
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from gerencianet.entities import GatewayPlan
from gerencianet.gateway import get_payment_link, get_notification_info


@csrf_exempt
def get_payment_link_view(request, *args, **kwargs):
    if request.method == 'POST':
        code = request.POST.get('code')
        email = request.POST.get('email')
        plan = GatewayPlan(code, 1990, u'Plano Básico', 1, False, 100)
        identifier = 'myIdentifier'
        gateway_payment = get_payment_link(email, plan, identifier=identifier)
        return HttpResponse(gateway_payment)

    return HttpResponse('Unack')


@csrf_exempt
def get_notification_info_view(request, *args, **kwargs):
    if request.method == 'POST':
        notification = request.POST.get('notificacao')
        info = get_notification_info(notification)
        return HttpResponse(info)
    return HttpResponse('Unack')