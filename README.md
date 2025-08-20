# 🚀 Prueba Técnica MVS Backend

¡Bienvenido! Este proyecto es una API RESTful para la gestión de tareas, desarrollada con Flask y siguiendo buenas prácticas y principios SOLID.

## 📦 Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   └── task.py
│   └── routes/
│       └── tasks_routes.py
├── config.py
├── extensions.py
├── run.py
└── README.md
```

## ⚙️ Configuración

1. **Clona el repositorio:**
   ```bash
   git clone <url-del-repo>
   cd backend
   ```
2. **Crea y activa un entorno virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configura las variables de entorno:**
   - Puedes editar `config.py` o usar variables de entorno:
     - `SECRET_KEY`: Clave secreta para Flask.
     - `DATABASE_URL`: URL de la base de datos (por defecto usa MySQL).


## 🛠️ Migraciones de Base de Datos

Este proyecto usa **Flask-Migrate** para gestionar cambios en el modelo de datos.

1. **Inicializa las migraciones:**
   ```bash
   flask db init
   ```
2. **Crea una migración (cuando cambies modelos):**
   ```bash
   flask db migrate -m "Descripción del cambio"
   ```
3. **Aplica la migración a la base de datos:**
   ```bash
   flask db upgrade
   ```

Si ya tienes una migración creada, solo ejecuta el último comando para actualizar la base de datos.

## 🗄️ Inicialización de la Base de Datos

Ejecuta el siguiente script en Python para crear las tablas:
```python
from app import create_app
from extensions import db

app = create_app()
with app.app_context():
    db.create_all()
```

## 🚦 Ejecución

Inicia el servidor con:
```bash
python run.py
```

## 📚 Endpoints

- `GET /tasks` — Obtiene todas las tareas
- `POST /tasks` — Crea una nueva tarea
- `PUT /tasks/<id>` — Actualiza una tarea existente
- `DELETE /tasks/<id>` — Elimina una tarea

## 🧑‍💻 Ejemplo de petición (cURL)

```bash
curl -X POST http://localhost:5000/tasks \
     -H "Content-Type: application/json" \
     -d '{"title": "Nueva tarea", "description": "Descripción"}'
```

## 🏆 Buenas prácticas
- Código modular y limpio
- Uso de Blueprints y modelos
- Principios SOLID
- Configuración flexible

---

✨ ¡Listo para usar y escalar!
