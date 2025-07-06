import os
from flask import send_from_directory, current_app
from models import db, Project

# ruta para almacenar las imágenes
UPLOAD_FOLDER = "uploads"


# ----------------- SUBIR IMAGEN -----------------
def upload_image(project_id, file):
    # existe el proyecto ?
    project = Project.query.get(project_id)
    if not project:
        return {"error": "Proyecto no encontrado"}, 404

    # no existe la carpeta ? = crear
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # guardar la imagen
    filename = f"project_{project_id}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # actualizar la ruta en la base de datos
    project.project_image_path = filename
    db.session.commit()

    return {"message": "Imagen subida exitosamente", "image_path": filename}, 200


# ----------------- OBTENER IMAGEN -----------------
# obtiene la imagen desde la carpeta de almacenamiento.
def get_image(project_id):
    project = Project.query.get(project_id)

    if not project or not project.project_image_path:
        return {"error": "Imagen no encontrada"}, 404

    filepath = os.path.join(
        current_app.config["UPLOAD_FOLDER"], project.project_image_path
    )

    try:
        return send_from_directory(
            current_app.config["UPLOAD_FOLDER"], project.project_image_path
        )
    except FileNotFoundError:
        return {"error": "Imagen no encontrada"}, 404


# ----------------- ELIMINAR IMAGEN -----------------
def delete_image(project_id):
    # elimina la imagen asociada a un proyecto.
    project = Project.query.get(project_id)
    if project and project.project_image_path:
        filepath = os.path.join(UPLOAD_FOLDER, project.project_image_path)
        # existe la imagen ? = eliminarla
        if os.path.exists(filepath):
            os.remove(filepath)
        project.project_image_path = None
        db.session.commit()
        return {"message": "Imagen eliminada exitosamente"}, 200
    else:
        return {"error": "Proyecto sin imagen"}, 404


# ----------------- ACTUALIZAR IMAGEN -----------------
def update_image(project_id, file):
    project = Project.query.get(project_id)
    if not project:
        return {"error": "Proyecto no encontrado"}, 404

    # existe imagen anterior ? = eliminarla
    if project.project_image_path:
        delete_image(project_id)

    # subir nueva imagen
    return upload_image(project_id, file)
