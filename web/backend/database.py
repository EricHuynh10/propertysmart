from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from config import db_config
from sqlalchemy import text


SQLALCHEMY_DATABASE_URL = '{type}://{user}:{password}@{host}/{schema}'.format(
    type=db_config['type'],
    user=db_config['user'],
    password=db_config['password'],
    host=db_config['host'],
    schema=db_config['schema'],
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Test the database connection
'''
try:
    session = SessionLocal()
    session.execute(text("SELECT 1"))
    print("Database connection successful")
except Exception as e:
    print("Error connecting to the database:", str(e))
finally:
    session.close()
'''
