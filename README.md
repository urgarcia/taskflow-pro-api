# 🚀 Task Management API

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)
[![AWS](https://img.shields.io/badge/AWS-Lambda-orange.svg)](https://aws.amazon.com/lambda/)
[![Status](https://img.shields.io/badge/Status-Production-success.svg)](https://e7j8m0r1hf.execute-api.us-east-1.amazonaws.com/dev)

Una API REST moderna y escalable para gestión de tareas, construida con Flask y desplegada en AWS Lambda. Implementa autenticación JWT con AWS Cognito y sigue principios de arquitectura limpia.

## 🌟 Características

- ✨ **API RESTful** con operaciones CRUD completas
- 🔐 **Autenticación JWT** integrada con AWS Cognito
- 🏗️ **Arquitectura limpia** con separación de responsabilidades
- ☁️ **Serverless** desplegado en AWS Lambda con Zappa
- 🗄️ **Base de datos** MySQL en Amazon RDS
- 🌍 **CORS** configurado para desarrollo frontend
- 📚 **Documentación** completa de endpoints
- 🛡️ **Seguridad** implementada en todas las rutas sensibles

## 🏛️ Arquitectura

```
backend/
├── app/
│   ├── __init__.py          # Configuración de Flask
│   ├── models/              # Modelos de datos (SQLAlchemy)
│   │   ├── task.py          # Modelo de tareas
│   │   └── user.py          # Modelo de usuarios
│   ├── repositories/        # Capa de acceso a datos
│   │   ├── task_repository.py
│   │   └── user_repository.py
│   ├── services/            # Lógica de negocio
│   │   ├── task_service.py
│   │   ├── user_service.py
│   │   └── jwt_service.py   # Autenticación JWT
│   └── routes/              # Controladores REST
│       ├── tasks_routes.py
│       └── auth_routes.py
├── migrations/              # Migraciones de base de datos
├── application.py          # Punto de entrada para Zappa
├── extensions.py          # Extensiones de Flask
├── requirements.txt       # Dependencias
└── zappa_settings.json   # Configuración de despliegue
```

### 🎯 Principios de Diseño

- **SOLID**: Separación clara entre modelos, servicios, repositorios y rutas
- **Repository Pattern**: Abstracción de acceso a datos
- **Service Layer**: Lógica de negocio centralizada
- **Dependency Injection**: Bajo acoplamiento entre componentes

## 🚀 Despliegue

### Entorno de Producción
- **URL Base**: `https://e7j8m0r1hf.execute-api.us-east-1.amazonaws.com/dev`
- **Infraestructura**: AWS Lambda + API Gateway
- **Base de datos**: Amazon RDS (MySQL)
- **Autenticación**: AWS Cognito User Pool

### Variables de Entorno
```bash
DATABASE_URL=mysql+pymysql://user:pass@host:port/db
COGNITO_POOL_ID=us-east-1_Zo904D2He
COGNITO_REGION=us-east-1
COGNITO_APP_CLIENT_ID=1u6mep85s45jigl31n5ijnqkui
```

## 🔐 Autenticación

La API utiliza **AWS Cognito** para autenticación con tokens JWT:

1. **Autenticarse** con AWS Cognito desde el frontend
2. **Obtener token** JWT del response de Cognito
3. **Enviar token** en el header `Authorization: Bearer <token>`
4. **Acceder** a los endpoints protegidos

### Ejemplo de Autenticación (JavaScript)
```javascript
// 1. Autenticación con AWS Cognito
const session = await Auth.signIn(username, password);
const token = session.getAccessToken().getJwtToken();

// 2. Uso del token en requests
const response = await fetch('/tasks', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
});
```

## 📚 Endpoints

### 🏠 Health Check
- `GET /` - Estado de la API

### 👤 Autenticación
- `POST /register` - Registro de usuario
- `POST /login` - Login (referencia - usar Cognito)
- `GET /profile` 🔒 - Perfil del usuario

### 📋 Tareas
- `GET /tasks` 🔒 - Listar todas las tareas
- `GET /tasks/{id}` 🔒 - Obtener tarea específica
- `POST /tasks` 🔒 - Crear nueva tarea
- `PUT /tasks/{id}` 🔒 - Actualizar tarea
- `DELETE /tasks/{id}` 🔒 - Eliminar tarea

*🔒 = Requiere autenticación JWT*

## 💡 Desarrollo Local

### Prerrequisitos
- Python 3.11+
- MySQL/MariaDB
- AWS CLI configurado
- Cuenta de AWS con Cognito User Pool

### Instalación

```bash
# Clonar repositorio
git clone <repository-url>
cd backend

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
export DATABASE_URL="mysql+pymysql://user:pass@localhost:3306/tasks_db"
export COGNITO_POOL_ID="your-pool-id"
export COGNITO_REGION="us-east-1"
export COGNITO_APP_CLIENT_ID="your-app-client-id"

# Ejecutar migraciones
flask db upgrade

# Ejecutar localmente (opción 1)
python run.py

# O ejecutar con Flask CLI (opción 2)
flask run
```

### Despliegue a AWS
```bash
# Actualizar en Lambda
zappa update dev

# Ver logs
zappa tail dev

# Estado del despliegue
zappa status dev
```

## 📊 Modelos de Datos

### Task
```python
{
  "id": int,
  "title": string,
  "description": string,
  "completed": boolean
}
```

### User
```python
{
  "id": int,
  "username": string,
  "name": string
}
```

## 🛠️ Stack Tecnológico

### Backend
- **Framework**: Flask 3.1.2
- **ORM**: SQLAlchemy
- **Migraciones**: Flask-Migrate
- **JWT**: PyJWT 1.7.1
- **CORS**: Flask-CORS

### Cloud & Infrastructure
- **Compute**: AWS Lambda
- **API Gateway**: AWS API Gateway
- **Database**: Amazon RDS (MySQL)
- **Authentication**: AWS Cognito
- **Deployment**: Zappa

### DevOps
- **Dependency Management**: pip + requirements.txt
- **Environment**: Virtual Environment
- **Configuration**: Environment Variables

## � Características Técnicas

### Seguridad
- ✅ JWT Token validation con AWS Cognito
- ✅ CORS configurado para desarrollo
- ✅ Validación de entrada en todos los endpoints
- ✅ Manejo seguro de contraseñas con hash

### Performance
- ✅ Serverless architecture (escalamiento automático)
- ✅ Connection pooling para base de datos
- ✅ Respuestas JSON optimizadas

### Mantenibilidad
- ✅ Arquitectura modular y testeable
- ✅ Separación clara de responsabilidades
- ✅ Código documentado y tipado
- ✅ Principios SOLID aplicados

## 📈 Próximas Mejoras

- [ ] Tests unitarios e integración
- [ ] Paginación en listado de tareas
- [ ] Filtros y búsqueda avanzada
- [ ] Rate limiting
- [ ] Logging estructurado
- [ ] Monitoreo y métricas
- [ ] Cache con Redis

## 👨‍💻 Desarrollo

Desarrollado con ❤️ utilizando mejores prácticas de desarrollo, arquitectura limpia y tecnologías modernas en la nube.

---

> **Nota**: Esta API está optimizada para producción con AWS Lambda y sigue estándares de la industria para APIs RESTful modernas.

---

✨ ¡Listo para usar y escalar!
