INSTALLED_APPS = [
    # ... apps de django ...
    'core',
    'django_extensions',
]

LANGUAGE_CODE = "es"
TIME_ZONE = "America/Lima"

# Seguridad (Requisito)
SESSION_COOKIE_AGE = 1800  # 30 minutos (Requisito RF3)
SESSION_COOKIE_HTTPONLY = True