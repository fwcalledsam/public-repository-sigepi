from models import (
    db,
    Person,
    Role,
    Stakeholder,
    Level,
    Project,
    ProjectStakeholder,
    Credentials,
)


# ----------------- LOGIN -----------------
def verify_admin_credentials(username, password):
    admin = Credentials.query.filter_by(auth_user=username).first()
    if admin and admin.auth_pass == password:
        return True
    return False


# ----------------- PERSON -----------------
def create_person_service(data):
    new_person = Person(
        person_firstname=data["firstname"],
        person_lastname=data["lastname"],
        person_location=data.get("location"),
        person_urlsite=data.get("urlsite"),
    )
    db.session.add(new_person)
    db.session.commit()
    return new_person


def get_all_persons_service():
    return Person.query.all()


def update_person_service(person_id, data):
    person = Person.query.get_or_404(person_id)
    person.person_firstname = data.get("firstname", person.person_firstname)
    person.person_lastname = data.get("lastname", person.person_lastname)
    person.person_location = data.get("location", person.person_location)
    person.person_urlsite = data.get("urlsite", person.person_urlsite)
    db.session.commit()
    return person


def delete_person_service(person_id):
    person = Person.query.get_or_404(person_id)
    db.session.delete(person)
    db.session.commit()
    return person_id


# ----------------- ROLE -----------------
def create_role_service(data):
    new_role = Role(role_description=data["description"])
    db.session.add(new_role)
    db.session.commit()
    return new_role


def get_all_roles_service():
    return Role.query.all()


def update_role_service(role_id, data):
    role = Role.query.get_or_404(role_id)
    role.role_description = data.get("description", role.role_description)
    db.session.commit()
    return role


def delete_role_service(role_id):
    role = Role.query.get_or_404(role_id)
    db.session.delete(role)
    db.session.commit()
    return role_id


# ----------------- STAKEHOLDER -----------------
def create_stakeholder_service(data):
    new_stakeholder = Stakeholder(person_id=data["person_id"], role_id=data["role_id"])
    db.session.add(new_stakeholder)
    db.session.commit()
    return new_stakeholder


def get_all_stakeholders_service():
    return Stakeholder.query.all()


def update_stakeholder_service(stakeholder_id, data):
    stakeholder = Stakeholder.query.get_or_404(stakeholder_id)
    stakeholder.person_id = data.get("person_id", stakeholder.person_id)
    stakeholder.role_id = data.get("role_id", stakeholder.role_id)
    db.session.commit()
    return stakeholder


def delete_stakeholder_service(stakeholder_id):
    stakeholder = Stakeholder.query.get_or_404(stakeholder_id)
    db.session.delete(stakeholder)
    db.session.commit()
    return stakeholder_id


# ----------------- LEVEL -----------------
def create_level_service(data):
    new_level = Level(level_description=data["description"])
    db.session.add(new_level)
    db.session.commit()
    return new_level


def get_all_levels_service():
    return Level.query.all()


def update_level_service(level_id, data):
    level = Level.query.get_or_404(level_id)
    level.level_description = data.get("description", level.level_description)
    db.session.commit()
    return level


def delete_level_service(level_id):
    level = Level.query.get_or_404(level_id)
    db.session.delete(level)
    db.session.commit()
    return level_id


# ----------------- PROJECT -----------------
def create_project_service(data):
    new_project = Project(
        project_name=data["name"],
        project_description=data["description"],
        project_agno=data["agno"],
        level_id=data["level_id"],
        project_image_path=data.get("image_path", None),
        project_keywords=data.get("keywords", None),
    )
    db.session.add(new_project)
    db.session.commit()
    return new_project


def get_all_projects_service():
    return Project.query.all()


def update_project_service(project_id, data):
    project = Project.query.get_or_404(project_id)
    project.project_name = data.get("name", project.project_name)
    project.project_description = data.get("description", project.project_description)
    project.project_agno = data.get("agno", project.project_agno)
    project.level_id = data.get("level_id", project.level_id)
    project.project_image_path = data.get("image_path", project.project_image_path)
    project.project_keywords = data.get("keywords", project.project_keywords)
    db.session.commit()
    return project


def delete_project_service(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return project_id


# ----------------- PROJECT STAKEHOLDER -----------------
def create_project_stakeholder_service(data):
    new_ps = ProjectStakeholder(
        project_id=data["project_id"], stakeholder_id=data["stakeholder_id"]
    )
    db.session.add(new_ps)
    db.session.commit()
    return new_ps


def get_all_project_stakeholders_service():
    return ProjectStakeholder.query.all()


def update_project_stakeholder_service(prj_stk_id, data):
    ps = ProjectStakeholder.query.get_or_404(prj_stk_id)
    ps.project_id = data.get("project_id", ps.project_id)
    ps.stakeholder_id = data.get("stakeholder_id", ps.stakeholder_id)
    db.session.commit()
    return ps


def delete_project_stakeholder_service(prj_stk_id):
    ps = ProjectStakeholder.query.get_or_404(prj_stk_id)
    db.session.delete(ps)
    db.session.commit()
    return prj_stk_id
