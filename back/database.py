from sqlalchemy import create_engine#connects to the database
from sqlalchemy.orm import declarative_base, sessionmaker# base
import os 
from dotenv import load_dotenv
#class for models and also talked to the channels
#evrythign is sqlalchemy

load_dotenv()
SQLALCHEMY_DATABASE_URL=os.getenv("DATABASE_URL")

Base = declarative_base()# so without this everything will just look like
#regular python
engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})
sessionLocal= sessionmaker(autocommit = False, autoflush=False, bind=engine)
def get_db():
    with sessionLocal() as db:
        yield db
        #creates a db session
#gives it to your route in main.py so that we can keep track of which request we are doing
#after request-> it closes automatically 
