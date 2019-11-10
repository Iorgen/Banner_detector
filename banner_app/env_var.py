import os
os.environ["POSTGRES_USER"] = 'py_dev'
os.environ["POSTGRES_PASSWORD"] = "panta1494"
os.environ["POSTGRES_DB"] = "banner_database"
os.environ["DEBUG"] = '1'
os.environ["SECRET_KEY"] = "=!e0lr$&cx8@9%8^*7a-c6i*2+%xqoyr^-0fz7m@6&qm(z!*uv"
os.environ["DJANGO_ALLOWED_HOSTS"] = 'localhost'
os.environ["SQL_ENGINE"] = "django.db.backends.postgresql_psycopg2"
os.environ["SQL_DATABASE"] = "banner_database"
os.environ["SQL_USER"] = "py_dev"
os.environ["SQL_PASSWORD"] = "panta1494"
os.environ["SQL_HOST"] = "db"
os.environ["SQL_PORT"] = ""
os.environ["DATABASE"] = "postgres"
