# python
from __future__ import unicode_literals
# libs
# local
from .base import APIClient


# Membership
class membership(object):
    _application_name = 'Membership'
    address = APIClient(application=_application_name,
                        service_uri='Address/')
    address_link = APIClient(application=_application_name,
                             service_uri='Address/{idAddress}/Link/')
    country = APIClient(application=_application_name,
                        service_uri='Country/')
    currency = APIClient(application=_application_name,
                         service_uri='Currency/')
    department = APIClient(application=_application_name,
                           service_uri='Member/{idMember}/Department/')
    language = APIClient(application=_application_name,
                         service_uri='Language/')
    member = APIClient(application=_application_name,
                       service_uri='Member/')
    member_link = APIClient(application=_application_name,
                            service_uri='Member/{idMember}/Link/')
    notification = APIClient(application=_application_name,
                             service_uri='Address/{idAddress}/Notification/')
    profile = APIClient(application=_application_name,
                        service_uri='Member/{idMember}/Profile/')
    subdivision = APIClient(application=_application_name,
                            service_uri='Country/{idCountry}/Subdivision/')
    team = APIClient(application=_application_name,
                     service_uri='Member/{idMember}/Team/')
    territory = APIClient(application=_application_name,
                          service_uri='Member/{idMember}/Territory/')
    timezone = APIClient(application=_application_name,
                         service_uri='Timezone/')
    transaction_type = APIClient(application=_application_name,
                                 service_uri='TransactionType/')
    user = APIClient(application=_application_name,
                     service_uri='User/')


# Antenna services
class antenna(object):
    _application_name = 'Antenna'
    antenna = APIClient(application=_application_name,
                        service_uri='Antenna/')


# Contacts Services
class contacts(object):
    _application_name = 'Contacts'
    campaign = APIClient(application=_application_name,
                         service_uri='Campaign/')
    group = APIClient(application=_application_name,
                      service_uri='Group/')
    contact = APIClient(application=_application_name,
                        service_uri='Contact/')
    campaign_contact = APIClient(
        application=_application_name,
        service_uri='Campaign/{idCampaign}/Contact/')
    group_contact = APIClient(
        application=_application_name,
        service_uri='Group/{idGroup}/Contact/')
    opportunity = APIClient(application=_application_name,
                            service_uri='Opportunity/')
    opportunity_history = APIClient(
        application=_application_name,
        service_uri='Opportunity/{idOpportunity}/History/')
    opportunity_contact = APIClient(
        application=_application_name,
        service_uri='Opportunity/{idOpportunity}/Contact/')


# DNS Services
class dns(object):
    _application_name = 'DNS'
    asn = APIClient(application=_application_name,
                    service_uri='ASN/')
    allocation = APIClient(application=_application_name,
                           service_uri='Allocation/')
    subnet = APIClient(application=_application_name,
                       service_uri='Subnet/')
    subnet_space = APIClient(
        application=_application_name,
        service_uri='Allocation/{idAllocation}/Subnet_space/')
    ipaddress = APIClient(application=_application_name,
                          service_uri='IPAddress/')
    recordptr = APIClient(application=_application_name,
                          service_uri='RecordPTR/')
    domain = APIClient(application=_application_name,
                       service_uri='Domain/')
    record = APIClient(application=_application_name,
                       service_uri='Record/')
    aggregated_blacklist = APIClient(application=_application_name,
                                     service_uri='AggregatedBlacklist/')
    blacklist = APIClient(application=_application_name,
                          service_uri='CIXBlacklist/')
    whitelist = APIClient(application=_application_name,
                          service_uri='CIXWhitelist/')
    blacklist_source = APIClient(application=_application_name,
                                 service_uri='BlacklistSource/')


# Documentation Services
class documentation(object):
    _application_name = 'Documentation'
    application = APIClient(application=_application_name,
                            service_uri='Application/')


# App Manager Services (Beta)
class app_manager(object):
    _application_name = 'AppManager'
    app = APIClient(application=_application_name,
                    service_uri='App/')
    app_menu = APIClient(application=_application_name,
                         service_uri='App/{idApp}/MenuItem/')
    menu_item_user = APIClient(application=_application_name,
                               service_uri='MenuItem/User/{idUser}/')


# Support Framework Services (Beta)
class support_framework(object):
    _application_name = 'SupportFramework'
    exception_code = APIClient(application=_application_name,
                               service_uri='ExceptionCode/')


# Training (Beta)
class training(object):
    _application_name = 'Training'
    syllabus = APIClient(application=_application_name,
                         service_uri='Syllabus/')
    cls = APIClient(application=_application_name,
                    service_uri='Class/')
    student = APIClient(application=_application_name,
                        service_uri='Student/')


# Scheduler (Beta)
class scheduler(object):
    _application_name = 'Scheduler'
    task = APIClient(application=_application_name,
                     service_uri='Task/')
    task_log = APIClient(application=_application_name,
                         service_uri='TaskLog/')
    execute_task = APIClient(application=_application_name,
                             service_uri='Task/{idTask}/execute/')


# HelpDesk (Beta)
class helpdesk(object):
    _application_name = 'HelpDesk'
    ticket = APIClient(application=_application_name,
                       service_uri='Ticket/{idTransactionType}/')
    ticket_history = APIClient(
        application=_application_name,
        service_uri='Ticket/{idTransactionType}/'
                    '{transactionSequenceNumber}/History/')
    status = APIClient(application=_application_name,
                       service_uri='Status/')
    reason_for_return = APIClient(application=_application_name,
                                  service_uri='ReasonForReturn/')
    reason_for_return_translation = APIClient(
        application=_application_name,
        service_uri='ReasonForReturn/{idReasonForReturn}/Translation/')
    ticket_question = APIClient(application=_application_name,
                                service_uri='TicketQuestion/')
    ticket_type = APIClient(application=_application_name,
                            service_uri='TicketType/')
    ticket_type_question = APIClient(
        application=_application_name,
        service_uri='TicketType/{id}/TicketQuestion/')
