# Configuración de la base de datos Supabase
class Config:
    # Configuración para Connection Pooling (Recomendado)
    DB_USER = "postgres.eedovnydbqlypoifuzje"  # Nota: incluye tu project ID
    DB_PASS = "databaseAccount1901"  # La contraseña que muestras
    DB_HOST = "aws-0-us-east-2.pooler.supabase.com"  # Host correcto para tu región
    DB_PORT = "6543"  # Puerto para Transaction Pooler
    DB_NAME = "postgres"

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# import os


# # facilita la gestion de diferentes entornos (modularidad y reutilizacion)
# class Config:
#     DB_USER = os.getenv("DB_USER", "postgres")
#     DB_PASS = os.getenv("DB_PASS", "1957")
#     DB_HOST = os.getenv("DB_HOST", "localhost") # para desarrollo local
#     # DB_HOST = os.getenv("DB_HOST", "db")  # para docker
#     DB_PORT = os.getenv("DB_PORT", "5432")
#     DB_NAME = os.getenv("DB_NAME", "project_management")
#     SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False  # advertencia del sistema de eventos
