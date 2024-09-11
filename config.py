from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

bd_url = 'mysql://root:4188@localhost:3306/gestao_usuarios'
engine = create_engine(bd_url)
Base = declarative_base()
