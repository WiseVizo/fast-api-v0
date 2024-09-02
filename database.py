from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'mysql+pymysql://root:root@localhost:3306/blogapp'
engine = create_engine(URL_DATABASE)
sesion_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

base = declarative_base()

# err: sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:msql.pymysql