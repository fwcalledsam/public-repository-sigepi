# Sistema de Gestión de Proyectos de Investigación

## Descripción General

El **Sistema de Gestión de Proyectos de Investigación** es una aplicación web orientada a servicios que permite gestionar proyectos de investigación, incluyendo la administración de personas, roles, niveles, asignaciones y recursos asociados a los proyectos. Este sistema está diseñado para facilitar la colaboración y el seguimiento de proyectos en un entorno académico o de investigación.

---

## Estructura del Proyecto

El proyecto está organizado en tres partes principales:

**Base de Datos (db/)**: PostgreSQL con scripts de inicialización y configuración Docker.

```plaintext
db/
├── Dockerfile                # Configuración de contenedor Docker para PostgreSQL
└── project_management.sql    # Script de inicialización de la base de datos
```

**Backend (b/)**: Implementado con Flask, proporciona una API RESTful para la gestión de datos.

```plaintext
b/
├── uploads/                  # Carpeta para almacenar imágenes de proyectos
├── config.py                 # Configuración de la aplicación
├── Dockerfile                # Configuración de contenedor Docker para el backend
├── image_service.py          # Servicio para manejar operaciones con imágenes
├── models.py                 # Definición de los modelos de datos
├── requirements.txt          # Dependencias del proyecto
├── routes.py                 # Definición de endpoints de la API
├── run.py                    # Punto de entrada de la aplicación
└── services.py               # Servicios y lógica de negocio
```

**Frontend (f/)**: Implementado con Vue 3 y Vite, ofrece una interfaz de usuario interactiva.

```plaintext
f/
├── Dockerfile                # Configuración de contenedor Docker para el frontend
├── index.html                # Punto de entrada HTML
├── nginx.conf                # Configuración del servidor web Nginx
├── package.json              # Dependencias y scripts
├── postcss.config.js         # Configuración de PostCSS
├── tailwind.config.js        # Configuración de TailwindCSS
├── vite.config.js            # Configuración de Vite
├── public/                   # Recursos estáticos
│   ├── guideTemplate.html  
│   ├── image.svg 
│   ├── landpage.png  
│   └── placeholder.svg 
└── src/  
    ├── App.vue               # Componente raíz
    ├── main.js               # Punto de entrada JavaScript
    ├── assets/               # Recursos estáticos
    │   ├── fonts/            # Fuentes Geist y configuración
    │   └── icons/            # Iconos y logo del sistema
    ├── components/           # Componentes reutilizables
    │   ├── cards/            # Tarjetas (proyectos, investigadores)
    │   ├── common/           # Componentes base (botones, badges)
    │   ├── layout/           # Componentes de diseño
    │   └── modals/           # Ventanas modales
    ├── layouts/              # Plantillas de diseño
    ├── lib/                  # Utilidades (API, cache, archivos)
    ├── router/               # Configuración de rutas
    ├── stores/               # Estado global con Pinia
    ├── utils/                # Funciones auxiliares
    └── views/                # Páginas de la aplicación
        ├── admin/            # Vistas administrativas
        ├── auth/             # Autenticación
        └── user/             # Vistas de usuario
```

## Backend

### Tecnologías Backend Utilizadas

- **Flask**: Framework ligero y flexible para construir la API RESTful
- **Flask-SQLAlchemy**: ORM robusto para la gestión eficiente de la base de datos
- **Flask-Marshmallow**: Biblioteca para serialización y validación de datos
- **PostgreSQL**: Sistema de gestión de base de datos relacional de alto rendimiento
- **Python 3.11+**: Lenguaje de programación principal

### Endpoints de ejemplo

| Método | Endpoint                          | Descripción                                   |
|--------|-----------------------------------|-----------------------------------------------|
| GET    | `/api/projects`                   | Obtener todos los proyectos.                  |
| POST   | `/api/projects`                   | Crear un nuevo proyecto.                      |
| PUT    | `/api/projects/<id>`              | Actualizar un proyecto existente.             |
| DELETE | `/api/projects/<id>`              | Eliminar un proyecto.                         |
| POST   | `/api/projects/<id>/upload-image` | Subir una imagen para un proyecto.            |
| GET    | `/api/projects/<id>/image`        | Obtener la imagen de un proyecto.             |

### Configuración (Conexion database - backend)

El archivo `config.py` contiene la configuración de la base de datos y otras variables de entorno.

### Base de Datos

El esquema de la base de datos está definido en los scripts SQL:

- `project_management.sql`

---

## Frontend

### Tecnologías Frontend Utilizadas

- **Vue 3**: Framework moderno y reactivo para interfaces de usuario
- **Vite**: Herramienta de desarrollo rápido con soporte para HMR
- **TailwindCSS**: Framework de utilidades CSS para diseño responsivo
- **Pinia**: Gestor de estado modular y tipado para Vue
- **Axios**: Cliente HTTP para comunicación con el backend

### Módulos Principales

#### Módulo de Administración

- Gestión de proyectos y sus detalles
- Administración de personas y roles
- Control de niveles académicos
- Asignaciones y responsabilidades

#### Módulo de Usuario

- Exploración de proyectos
- Visualización de investigadores
- Detalles de proyectos específicos

#### Características Destacadas

- Interfaz responsiva y moderna
- Gestión de imágenes de proyectos
- Sistema de caché para mejor rendimiento
- Validación de datos en tiempo real
- Soporte para carga masiva de datos

### Configuración (Conexion backend - frontend)

El archivo `vite.config.js` define la configuración del servidor de desarrollo y el proxy para la API.

### Scripts de Desarrollo

- Iniciar el servidor de desarrollo:

  ```bash
  npm run dev
  ```

- Construir la aplicación para producción:

  ```bash
  npm run build
  ```

---

## Instrucciones de Uso

### Requisitos del Sistema

#### Backend

- PostgreSQL 14 o superior
- Python 3.11 o superior
- pip (gestor de paquetes de Python)
- Dependencias específicas:

  ```bash
  cd b
  pip install -r requirements.txt
  ```

#### Frontend

- Node.js 18 o superior
- npm 9 o superior
- Dependencias específicas:

  ```bash
  cd f
  npm install
  ```

#### Otros Requisitos

- Servidor web (nginx recomendado para producción)
- Al menos 2GB de RAM disponible
- 1GB de espacio en disco para instalación básica

### Guía de Instalación y Despliegue

#### 1. Configuración de la Base de Datos

**Opción A: Usando línea de comandos**

```sql
psql -U postgres -f db/project_management.sql
```

**Opción B: Usando pgAdmin**

1. Abrir pgAdmin y autenticarse
2. Crear nueva base de datos
3. Abrir Query Tool
4. Importar y ejecutar `project_management.sql`

#### 2. Configuración del Backend

**Desarrollo local**

```bash
cd b
python run.py
```

**Producción con Docker**

```bash
docker-compose up backend
```

#### 3. Configuración del Frontend

**Desarrollo local**

```bash
cd f
npm run dev
```

**Producción con Docker**

```bash
docker-compose up frontend
```

#### 4. Acceso al Sistema

- **Aplicación Web**: `http://localhost:5173`
- **API Backend**: `http://localhost:5000`

#### 5. Verificación

1. Comprobar conexión a base de datos
2. Verificar servicios backend activos
3. Confirmar acceso a interfaz web
4. Validar autenticación de usuario

---

## Documentación Adicional

### Docker y Despliegue

- `docker-compose.yml`: Configuración de servicios Docker

### Scripts de Utilidad

- `init_server.bat`: Script de inicialización del servidor en local

## Soporte y Contribución

Para reportar problemas o sugerir mejoras:

1. Abrir un issue en el repositorio
2. Proporcionar detalles del problema/sugerencia
3. Incluir pasos para reproducir (si aplica)

## Licencias

- Software: MIT License
- Fuente "Geist": SIL Open Font License 1.1
- Documentación: Creative Commons Attribution 4.0
