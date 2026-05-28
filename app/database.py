import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("postgresql://postgres:WbJuliJYuqrrdrbADgZOLiZboKdhQeaC@postgres-vdl5.railway.internal:5432/railway")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql://",
        1
    )

engine = create_engine(DATABASE_URL)