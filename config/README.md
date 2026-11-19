# Sistema Web de Gestión de Préstamos - Caso 1

**Universidad Nacional del Centro del Perú**
**Facultad de Ingeniería de Sistemas**
**Curso:** Desarrollo de Aplicaciones Web (IS093A)
**Semana 12:** Gestión de Formularios, Django Admin, Middleware y Seguridad

## 👨‍💻 Autor
*   **Antezana Villegas Jhojan Manuel**

## 📌 Descripción del Proyecto
Este proyecto digitaliza el proceso de préstamo de equipos del laboratorio de la Facultad de Ingeniería de Sistemas. Permite a los docentes solicitar equipos con validaciones estrictas, a los administradores gestionar el inventario mediante un panel personalizado, y garantiza la seguridad mediante middleware de auditoría, autenticación por roles y sesiones controladas.

## 🚀 Tecnologías Utilizadas
*   Python 3.x
*   Django 5.x (o 6.x)
*   SQLite (Base de datos)
*   HTML5 / CSS3

## ⚙️ Instalación y Ejecución
1. Clonar el repositorio:
   ```bash
   git clone [URL_DE_TU_REPOSITORIO]
Crear y activar el entorno virtual:

bash
python -m venv venv
venv\Scripts\activate
Instalar dependencias:

bash
pip install -r requirements.txt
Ejecutar migraciones:

bash
python manage.py makemigrations
python manage.py migrate
Crear superusuario:

bash
python manage.py createsuperuser
Iniciar el servidor:

bash
python manage.py runserver
🛡️ Funcionalidades Implementadas (Rúbrica)
Formularios y Validación: ModelForm con validación cruzada (clean()) para evitar que un docente tenga más de 3 préstamos activos y validaciones clean_<campo>() (fechas pasadas, regex, sanitización). Incluye un formulario clásico (BusquedaEquipoForm).

Django Admin: Personalización de list_display, filtros por fecha/estado, búsqueda, campos calculados (dias_retraso) y acciones masivas (marcar mantenimiento).

Middleware de Auditoría: Intercepta cada petición POST y registra al usuario, IP y acción en un archivo audit.log.

Autenticación y Sesiones: Rutas protegidas con @login_required, control de sesión expirando a los 30 minutos y protección CSRF estricta.