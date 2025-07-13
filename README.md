# Advanced Task Manager

Un **gestor de tareas tipo Trello** construido con **Django**, **Bootstrap 5** y **SCSS**, pensado para:

- **Practicar** integración de Django, DRF y frontend moderno.  
- **Aprender** patrones de diseño (apps independientes, mixins, adapters).  
- **Portafolio**: demostrar un proyecto real, completo y listo para producción.

---

## 🛠 Tecnologías

- **Backend**: Python 3.11, Django 5.2, Django-Allauth, Django REST Framework  
- **Frontend**: Bootstrap 5, SCSS (variables, mixins, componentes, overrides)  
- **Herramientas**: npm (Sass CLI), PostCSS/PurgeCSS, Git y GitHub  
- **Base de datos**: SQLite (desarrollo) / cualquier otro SQL en producción  
- **Email en dev**: `console.EmailBackend` (no envía, muestra en consola)

---

## 📂 Estructura del proyecto

```
config/       # Settings, URLs, WSGI
accounts/     # Extensión de User, perfil, allauth adapter
boards/       # Tableros y TaskLists (views, URLs, admin)
tasks/        # Tasks, API REST para reordenación
static/
├─ scss/      # SCSS (abstracts, components, layout, pages)
└─ css/       # CSS compilado (main.css, main.min.css, main.purged.css)
templates/
├─ account/   # allauth overrides (login, signup, logout…)
├─ boards/    # plantillas de tableros
└─ tasks/     # plantillas de tareas
```

yaml
Copiar
Editar

---

## 🚀 Instalación y puesta en marcha

1. **Clona el repositorio**  
   ```bash
   git clone https://github.com/TU_USUARIO/advanced-task-manager-django.git
   cd advanced-task-manager-django
   ```

### Entorno virtual y dependencias

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### Variables de entorno

Copia el ejemplo y edita tu .env:

```bash
cp .env.example .env
# Ajusta SECRET_KEY, DEBUG, ALLOWED_HOSTS…
```

### Migraciones y superusuario

```bash
python manage.py migrate
python manage.py createsuperuser
```

### Frontend: instalar y compilar SCSS

```bash
npm install
# Compilación de desarrollo
npm run build:css
# Para producción (minified + PurgeCSS)
npm run build:css:prod
npm run purge:css
```

### Ejecutar servidor

```bash
python manage.py runserver
```

Accede en tu navegador a <http://127.0.0.1:8000>.

---

## ⚙️ Uso y comandos Git

```bash
# Añadir todo al stage
git add .

# Primer commit
git commit -m "chore: initial project setup, Django + Bootstrap + SCSS"

# Conectar repo remoto (si no lo has hecho)
git remote add origin git@github.com:TU_USUARIO/advanced-task-manager-django.git

# Subir a GitHub
git push -u origin main
```

A partir de aquí, crea ramas `feature/...`, haz commits atómicos, y usa Pull Requests para revisar cambios.

---

## 📋 Funcionalidades destacadas

- **Autenticación**: login, signup, logout, recuperación y cambio de contraseña.
- **Perfil de usuario**: avatar, bio, edición de perfil.
- **Boards**: CRUD completo, slug URLs, permisos de propietario/miembros.
- **TaskLists & Tasks**: CRUD, drag & drop con API REST, posiciones ajustadas.
- **Asignación**: asigna tareas a usuarios, establece prioridad y fecha límite.
- **Exportación**: descarga todas las tareas de un board en CSV o JSON.
- **Responsive**: mobile-first, tests en todos los breakpoints de Bootstrap.
- **SCSS**: variables de marca, mixins, overrides de Bootstrap y responsive tweaks.
- **Mensajes Flash**: alerts dismissibles, popovers de ayuda.

---

## 📝 Licencia

MIT License © 2025 – Tu Nombre

¡Gracias por llegar hasta aquí! Este proyecto muestra cómo integrar de manera realista un stack completo Django + Bootstrap + SCSS con buenas prácticas, ideal tanto para tu aprendizaje como para tu portafolio.
