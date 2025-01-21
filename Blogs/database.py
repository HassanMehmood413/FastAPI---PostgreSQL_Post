from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# steps to make url 
# postgresql://username:password@localhost:5432/database_name

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


# for sqllite you need to add one more parameter in engine 
#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

engine = create_engine(SQLALCHEMY_DATABASE_URL)


sessionlocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()






# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# def get_database_connection():
#     while True:
#         try: 
#             conn = psycopg2.connect(
#                 dbname="data2",
#                 user="postgres",
#                 password="CreatePassword123",
#                 host="localhost",
#                 port="5432"
#             )
#             cursor = conn.cursor(cursor_factory=RealDictCursor)
#             print("Connected to the database")
#             return conn, cursor
#         except Exception as error:
#             print("Connection Failed")
#             print('Error is :', error)
#             print("Retrying in 2 seconds")
#             time.sleep(2)