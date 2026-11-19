import datetime, os
from django.conf import settings

class AuditoriaMedicaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.log_file = os.path.join(settings.BASE_DIR, 'auditoria_medica.log')

    def __call__(self, request):
        if request.user.is_authenticated:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.datetime.now()}] USER: {request.user.username} | ACCEDIÓ A: {request.path}\n")
        return self.get_response(request)