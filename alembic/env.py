import sys
import os
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Ensure the project root is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

# Import models after fixing sys.path
from app.models.base import Base 
from app.models.company import CarCompany
from app.models.models import CarModel
from app.models.spare import SparePart
from app.models.user import User
from app.models.errorlog import ErrorLog

# Load environment variables
load_dotenv()

# Fetching database credentials
POSTGRES_USER = os.getenv("POSTGRES_USER", "caruser")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "caruser123")
POSTGRES_DB = os.getenv("POSTGRES_DB", "carspare")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5434")

# Update Alembic config
target_metadata = Base.metadata
config = context.config
config.set_main_option(
    "sqlalchemy.url",
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
