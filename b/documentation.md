# Documentación del Backend

====================================================================================================================================

## Endpoints disponibles

### Autenticación ------------------------------------------------------------------------------------------------------------------

- `POST /login`: Inicia sesión con credenciales de administrador. Requiere `username` y `password` en el cuerpo de la solicitud.
- `POST /logout`: Cierra la sesión actual.

### Personas -----------------------------------------------------------------------------------------------------------------------

- `GET /persons`: Obtiene todas las personas registradas. Devuelve un array de objetos Person.
- `POST /persons`: Crea una nueva persona. Requiere `firstname`, `lastname`, y opcionalmente `location` y `urlsite`.
- `PUT /persons/<int:person_id>`: Actualiza una persona existente. Acepta campos parciales para actualizar.
- `DELETE /persons/<int:person_id>`: Elimina una persona y sus relaciones asociadas.

### Roles -------------------------------------------------------------------------------------------------------------------------

- `GET /roles`: Obtiene todos los roles disponibles.
- `POST /roles`: Crea un nuevo rol. Requiere `description`.
- `PUT /roles/<int:role_id>`: Actualiza la descripción de un rol.
- `DELETE /roles/<int:role_id>`: Elimina un rol y sus relaciones asociadas.

### Stakeholders ------------------------------------------------------------------------------------------------------------------

- `GET /stakeholders`: Obtiene todos los stakeholders registrados.
- `POST /stakeholders`: Crea un nuevo stakeholder. Requiere `person_id` y `role_id`.
- `PUT /stakeholders/<int:stakeholder_id>`: Actualiza un stakeholder existente.
- `DELETE /stakeholders/<int:stakeholder_id>`: Elimina un stakeholder y sus relaciones con proyectos.

### Niveles -----------------------------------------------------------------------------------------------------------------------

- `GET /levels`: Obtiene todos los niveles disponibles.
- `POST /levels`: Crea un nuevo nivel. Requiere `description`.
- `PUT /levels/<int:level_id>`: Actualiza la descripción de un nivel.
- `DELETE /levels/<int:level_id>`: Elimina un nivel y sus proyectos asociados.

### Proyectos ---------------------------------------------------------------------------------------------------------------------

- `GET /projects`: Obtiene todos los proyectos con sus detalles.
- `POST /projects`: Crea un nuevo proyecto. Requiere `name`, `description`, `agno` y `level_id`. Opcionalmente acepta `image_path` y `keywords`.
- `PUT /projects/<int:project_id>`: Actualiza un proyecto existente. Acepta campos parciales.
- `DELETE /projects/<int:project_id>`: Elimina un proyecto y todas sus relaciones.

### Gestión de imágenes de proyectos

- `POST /projects/<int:project_id>/upload-image`: Sube una imagen para un proyecto. Requiere un archivo en el campo `file`.
- `GET /projects/<int:project_id>/image`: Devuelve la imagen asociada a un proyecto.
- `DELETE /projects/<int:project_id>/delete-image`: Elimina la imagen de un proyecto.
- `PUT /projects/<int:project_id>/update-image`: Reemplaza la imagen de un proyecto.

### Relaciones Proyecto-Stakeholder -----------------------------------------------------------------------------------------------

- `GET /project_stakeholders`: Obtiene todas las relaciones entre proyectos y stakeholders.
- `POST /project_stakeholders`: Crea una nueva relación. Requiere `project_id` y `stakeholder_id`.
- `PUT /project_stakeholders/<int:prj_stk_id>`: Actualiza una relación existente.
- `DELETE /project_stakeholders/<int:prj_stk_id>`: Elimina una relación específica.

====================================================================================================================================

## Estructura de la base de datos

### Credentials -------------------------------------------------------------------------------------------------------------------

- `id_credentials` (PK): Identificador único
- `auth_user`: Nombre de usuario
- `auth_pass`: Contraseña (almacenada como texto plano, cambiar en producción)

### Person ------------------------------------------------------------------------------------------------------------------------

- `person_id` (PK): Identificador único
- `person_firstname`: Nombre
- `person_lastname`: Apellido
- `person_location`: Ubicación (opcional)
- `person_urlsite`: URL personal (opcional)

### Role --------------------------------------------------------------------------------------------------------------------------

- `role_id` (PK): Identificador único
- `role_description`: Descripción del rol

### Stakeholder -------------------------------------------------------------------------------------------------------------------

- `stakeholder_id` (PK): Identificador único
- `person_id` (FK): Referencia a Person
- `role_id` (FK): Referencia a Role

### Level -------------------------------------------------------------------------------------------------------------------------

- `level_id` (PK): Identificador único
- `level_description`: Descripción del nivel

### Project -----------------------------------------------------------------------------------------------------------------------

- `project_id` (PK): Identificador único
- `project_name`: Nombre del proyecto
- `project_description`: Descripción detallada
- `project_agno`: Año del proyecto
- `level_id` (FK): Referencia a Level
- `project_image_path`: Ruta de la imagen (opcional)
- `project_keywords`: Palabras clave (opcional)

### ProjectStakeholder ------------------------------------------------------------------------------------------------------------

- `prj_stk_id` (PK): Identificador único
- `project_id` (FK): Referencia a Project
- `stakeholder_id` (FK): Referencia a Stakeholder
