from django.conf import settings


class NginxCertificateMiddleware(object):
    def process_request(self, request):
        request.certificate_subject = ''

        status = request.META.get(settings.CERTIFICATE_AUTH_STATUS_HEADER_NAME, settings.CERTIFICATE_AUTH_STATUS_FAILURE)

        if status == settings.CERTIFICATE_AUTH_STATUS_SUCCESS:
            subject = request.META.get(settings.CERTIFICATE_AUTH_SUBJECT_HEADER_NAME, '')

            for subject_part in subject.split('/'):
                if subject_part.startswith('CN='):
                    request.certificate_subject = subject_part[3:]
