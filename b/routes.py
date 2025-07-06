from flask import Blueprint, jsonify, request, redirect, send_file

from services import (
    # CREATE
    create_person_service,
    create_role_service,
    create_stakeholder_service,
    create_level_service,
    create_project_service,
    create_project_stakeholder_service,
    # GET
    get_all_persons_service,
    get_all_roles_service,
    get_all_stakeholders_service,
    get_all_levels_service,
    get_all_projects_service,
    get_all_project_stakeholders_service,
    # UPDATE
    update_person_service,
    update_role_service,
    update_stakeholder_service,
    update_level_service,
    update_project_service,
    update_project_stakeholder_service,
    # DELETE
    delete_person_service,
    delete_role_service,
    delete_stakeholder_service,
    delete_level_service,
    delete_project_service,
    delete_project_stakeholder_service,
)
from image_service import upload_image, get_image, delete_image, update_image
from models import (
    person_schema,
    persons_schema,
    role_schema,
    roles_schema,
    stakeholder_schema,
    stakeholders_schema,
    level_schema,
    levels_schema,
    project_schema,
    projects_schema,
    project_stakeholder_schema,
    project_stakeholders_schema,
    Credentials,
)


api = Blueprint("api", __name__)


# ----------------- REDIRECCION-AUTOMATICA -----------------
@api.route("/", methods=["GET"])
def redirect_to_default():
    return redirect("/documentation", code=302)


@api.route("/documentation", methods=["GET"])
def get_documentation():
    try:
        return send_file("documentation.md", mimetype="text/markdown")
    except FileNotFoundError:
        return jsonify({"error": "Documentación no encontrada"}), 404


# ----------------- LOGIN -----------------
@api.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Buscar las credenciales en la base de datos
    admin = Credentials.query.filter_by(auth_user=username).first()

    if admin and admin.auth_pass == password:
        return jsonify({"message": "Login exitoso", "redirect": "/admin"}), 200
    else:
        return jsonify({"message": "Credenciales incorrectas"}), 401


@api.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logout exitoso"}), 200


# ----------------- PERSON -----------------
# READ
@api.route("/persons", methods=["GET"])
def get_persons():
    persons = get_all_persons_service()
    return jsonify(persons_schema.dump(persons))


# CREATE
@api.route("/persons", methods=["POST"])
def create_person():
    data = request.json
    new_person = create_person_service(data)
    return (
        jsonify({"message": "Persona creada exitosamente", "id": new_person.person_id}),
        201,
    )


# UPDATE
@api.route("/persons/<int:person_id>", methods=["PUT"])
def update_person(person_id):
    data = request.json
    update_person_service(person_id, data)
    return jsonify({"message": "Persona actualizada exitosamente"}), 200


# DELETE
@api.route("/persons/<int:person_id>", methods=["DELETE"])
def delete_person(person_id):
    delete_person_service(person_id)
    return jsonify({"message": "Persona eliminada exitosamente"}), 200


# ----------------- ROLE -----------------
@api.route("/roles", methods=["GET"])
def get_roles():
    roles = get_all_roles_service()
    return jsonify(roles_schema.dump(roles))


@api.route("/roles", methods=["POST"])
def create_role():
    data = request.json
    new_role = create_role_service(data)
    return jsonify({"message": "Rol creado exitosamente", "id": new_role.role_id}), 201


@api.route("/roles/<int:role_id>", methods=["PUT"])
def update_role(role_id):
    data = request.json
    update_role_service(role_id, data)
    return jsonify({"message": "Rol actualizado exitosamente"}), 200


@api.route("/roles/<int:role_id>", methods=["DELETE"])
def delete_role(role_id):
    delete_role_service(role_id)
    return jsonify({"message": "Rol eliminado exitosamente"}), 200


# ----------------- STAKEHOLDER -----------------
@api.route("/stakeholders", methods=["GET"])
def get_stakeholders():
    stakeholders = get_all_stakeholders_service()
    return jsonify(stakeholders_schema.dump(stakeholders))


@api.route("/stakeholders", methods=["POST"])
def create_stakeholder():
    data = request.json
    new_stakeholder = create_stakeholder_service(data)
    return (
        jsonify(
            {
                "message": "Stakeholder creado exitosamente",
                "id": new_stakeholder.stakeholder_id,
            }
        ),
        201,
    )


@api.route("/stakeholders/<int:stakeholder_id>", methods=["PUT"])
def update_stakeholder(stakeholder_id):
    data = request.json
    update_stakeholder_service(stakeholder_id, data)
    return jsonify({"message": "Stakeholder actualizado exitosamente"}), 200


@api.route("/stakeholders/<int:stakeholder_id>", methods=["DELETE"])
def delete_stakeholder(stakeholder_id):
    delete_stakeholder_service(stakeholder_id)
    return jsonify({"message": "Stakeholder eliminado exitosamente"}), 200


# ----------------- LEVEL -----------------
@api.route("/levels", methods=["GET"])
def get_levels():
    levels = get_all_levels_service()
    return jsonify(levels_schema.dump(levels))


@api.route("/levels", methods=["POST"])
def create_level():
    data = request.json
    new_level = create_level_service(data)
    return (
        jsonify({"message": "Nivel creado exitosamente", "id": new_level.level_id}),
        201,
    )


@api.route("/levels/<int:level_id>", methods=["PUT"])
def update_level(level_id):
    data = request.json
    update_level_service(level_id, data)
    return jsonify({"message": "Nivel actualizado exitosamente"}), 200


@api.route("/levels/<int:level_id>", methods=["DELETE"])
def delete_level(level_id):
    delete_level_service(level_id)
    return jsonify({"message": "Nivel eliminado exitosamente"}), 200


# ----------------- PROJECT -----------------
@api.route("/projects", methods=["GET"])
def get_projects():
    projects = get_all_projects_service()
    return jsonify(projects_schema.dump(projects))


@api.route("/projects", methods=["POST"])
def create_project():
    data = request.json
    new_project = create_project_service(data)
    return (
        jsonify(
            {"message": "Proyecto creado exitosamente", "id": new_project.project_id}
        ),
        201,
    )


@api.route("/projects/<int:project_id>", methods=["PUT"])
def update_project(project_id):
    data = request.json
    update_project_service(project_id, data)
    return jsonify({"message": "Proyecto actualizado exitosamente"}), 200


@api.route("/projects/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    delete_project_service(project_id)
    return jsonify({"message": "Proyecto eliminado exitosamente"}), 200


# ----------------- PROJECT STAKEHOLDER -----------------
@api.route("/project_stakeholders", methods=["GET"])
def get_project_stakeholders():
    project_stakeholders = get_all_project_stakeholders_service()
    return jsonify(project_stakeholders_schema.dump(project_stakeholders))


@api.route("/project_stakeholders", methods=["POST"])
def create_project_stakeholder():
    data = request.json
    new_ps = create_project_stakeholder_service(data)
    return (
        jsonify(
            {
                "message": "Project Stakeholder creado exitosamente",
                "id": new_ps.prj_stk_id,
            }
        ),
        201,
    )


@api.route("/project_stakeholders/<int:prj_stk_id>", methods=["PUT"])
def update_project_stakeholder(prj_stk_id):
    data = request.json
    update_project_stakeholder_service(prj_stk_id, data)
    return jsonify({"message": "Project Stakeholder actualizado exitosamente"}), 200


@api.route("/project_stakeholders/<int:prj_stk_id>", methods=["DELETE"])
def delete_project_stakeholder(prj_stk_id):
    delete_project_stakeholder_service(prj_stk_id)
    return jsonify({"message": "Project Stakeholder eliminado exitosamente"}), 200


# --------------------------------------------------------------------------------
# -------------------- ENDPOINTS PREPARADOS PARA PROD ----------------------------
# --------------------------------------------------------------------------------


# ------------------------- I M A G E N -------------------------------
# ----------------- SUBIR OBTENER ACTUALIZAR ELIMINAR -----------------
@api.route("/projects/<int:project_id>/upload-image", methods=["POST"])
def upload_project_image(project_id):
    if "file" not in request.files:
        return jsonify({"error": "No se encontró ningún archivo"}), 400

    file = request.files["file"]
    return upload_image(project_id, file)


@api.route("/projects/<int:project_id>/image", methods=["GET"])
def serve_image(project_id):
    return get_image(project_id)


@api.route("/projects/<int:project_id>/delete-image", methods=["DELETE"])
def remove_project_image(project_id):
    return delete_image(project_id)


@api.route("/projects/<int:project_id>/update-image", methods=["PUT"])
def update_project_image(project_id):
    if "file" not in request.files:
        return jsonify({"error": "No se encontró ningún archivo"}), 400

    file = request.files["file"]
    return update_image(project_id, file)
