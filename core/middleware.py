import datetime, os
from django.conf import settings

class AuditoriaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.log_file = os.path.join(settings.BASE_DIR, 'audit.log')

    def __call__(self, request):
        # Intercepta el Request
        if request.user.is_authenticated and request.method == 'POST':
            ip = request.META.get('REMOTE_ADDR')
            accion = f"Acción POST en {request.path}"
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.datetime.now()}] USER: {request.user.username} | IP: {ip} | {accion}\n")
        
        response = self.get_response(request)
        return response