from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()
ma = Marshmallow()

##############################################
# ----------------- MODELS ----------------- #
##############################################


# ----------------- LOGIN -----------------
class Credentials(db.Model):
    __tablename__ = "credentials"
    id_credentials = db.Column(db.Integer, primary_key=True)
    auth_user = db.Column(db.String(50), nullable=False)
    auth_pass = db.Column(db.String(255), nullable=False)


print("El modelo de credentials creado")


# ----------------- PERSON -----------------
class Person(db.Model):
    __tablename__ = "person"

    person_id = db.Column(db.Integer, primary_key=True)
    person_firstname = db.Column(db.String(50), nullable=False)
    person_lastname = db.Column(db.String(50), nullable=False)
    person_location = db.Column(db.String(200), nullable=True)
    person_urlsite = db.Column(db.String(255), nullable=True)

    # definir relaciones entre tablas
    stakeholders = db.relationship(
        "Stakeholder", backref="person", cascade="all, delete"
    )


print("El modelo de Person creado")


# ----------------- ROLE -----------------
class Role(db.Model):
    __tablename__ = "role"

    role_id = db.Column(db.Integer, primary_key=True)
    role_description = db.Column(db.String(50), nullable=False)

    stakeholders = db.relationship("Stakeholder", backref="role", cascade="all, delete")


print("El modelo de Role creado")


# ----------------- STAKEHOLDER -----------------
class Stakeholder(db.Model):
    __tablename__ = "stakeholder"

    stakeholder_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(
        db.Integer,
        db.ForeignKey("person.person_id", ondelete="CASCADE"),
        nullable=False,
    )
    role_id = db.Column(
        db.Integer, db.ForeignKey("role.role_id", ondelete="CASCADE"), nullable=False
    )

    project_stakeholders = db.relationship(
        "ProjectStakeholder", backref="stakeholder", cascade="all, delete"
    )


print("El modelo de Stakeholder creado")


# ----------------- LEVEL -----------------
class Level(db.Model):
    __tablename__ = "level"

    level_id = db.Column(db.Integer, primary_key=True)
    level_description = db.Column(db.String(50), nullable=False)

    projects = db.relationship("Project", backref="level", cascade="all, delete")


print("El modelo de Level creado")


# ----------------- PROJECT -----------------
class Project(db.Model):
    __tablename__ = "project"

    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(200), nullable=False)
    project_description = db.Column(db.String(2500), nullable=False)
    project_agno = db.Column(db.Integer, nullable=False)
    level_id = db.Column(
        db.Integer, db.ForeignKey("level.level_id", ondelete="CASCADE"), nullable=False
    )
    project_image_path = db.Column(db.String(255), nullable=True)
    project_keywords = db.Column(db.String(200), nullable=True)

    project_stakeholders = db.relationship(
        "ProjectStakeholder", backref="project", cascade="all, delete"
    )


print("El modelo de Project creado")


# ----------------- PROJECT STAKEHOLDER -----------------
class ProjectStakeholder(db.Model):
    __tablename__ = "project_stakeholder"

    prj_stk_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(
        db.Integer,
        db.ForeignKey("project.project_id", ondelete="CASCADE"),
        nullable=False,
    )
    stakeholder_id = db.Column(
        db.Integer,
        db.ForeignKey("stakeholder.stakeholder_id", ondelete="CASCADE"),
        nullable=False,
    )


print("El modelo de Project-Stakeholder creado")

###############################################
# ----------------- SCHEMAS ----------------- #
###############################################


# ----------------- PERSON -----------------
# esquema de serialización
class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        load_instance = True
        sqla_session = db.session


# instancias
person_schema = PersonSchema()  # un solo objeto
persons_schema = PersonSchema(many=True)  # multiples objetos

print("El esquema de Person creado")


# ----------------- ROLE -----------------
class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        load_instance = True
        sqla_session = db.session


role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

print("El esquema de Rol creado")


# ----------------- STAKEHOLDER -----------------
class StakeholderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Stakeholder
        load_instance = True
        sqla_session = db.session

    stakeholder_id = ma.auto_field()
    person_id = ma.auto_field()
    role_id = ma.auto_field()


stakeholder_schema = StakeholderSchema()
stakeholders_schema = StakeholderSchema(many=True)

print("El esquema de Stakeholder creado")


# ----------------- LEVEL -----------------
class LevelSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Level
        load_instance = True
        sqla_session = db.session


level_schema = LevelSchema()
levels_schema = LevelSchema(many=True)

print("El esquema de Level creado")


# ----------------- PROJECT -----------------
class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        load_instance = True
        sqla_session = db.session

    level_id = ma.auto_field()
    project_image_path = ma.auto_field()
    project_keywords = ma.auto_field()


project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

print("El esquema de Project creado")


# ----------------- PROJECT STAKEHOLDER -----------------
class ProjectStakeholderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProjectStakeholder
        load_instance = True
        sqla_session = db.session

    prj_stk_id = ma.auto_field()
    project_id = ma.auto_field()
    stakeholder_id = ma.auto_field()


project_stakeholder_schema = ProjectStakeholderSchema()
project_stakeholders_schema = ProjectStakeholderSchema(many=True)

print("El esquema de Project-Stakeholder creado")
