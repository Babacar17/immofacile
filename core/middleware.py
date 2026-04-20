import time
import logging

req_logger = logging.getLogger('immofacile.requests')
sec_logger = logging.getLogger('immofacile.security')
app_logger = logging.getLogger('immofacile')


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start    = time.monotonic()
        response = self.get_response(request)
        ms       = (time.monotonic() - start) * 1000
        ip       = self._get_ip(request)
        user     = request.user.username if request.user.is_authenticated else 'anon'

        req_logger.info('%s %s %s %s %.0fms user=%s',
                        ip, request.method, request.path, response.status_code, ms, user)

        if response.status_code == 403:
            sec_logger.warning('403 ip=%s path=%s user=%s', ip, request.path, user)
        elif response.status_code >= 500:
            app_logger.error('5xx ip=%s path=%s status=%s', ip, request.path, response.status_code)

        return response

    @staticmethod
    def _get_ip(request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        return xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR', '-')
