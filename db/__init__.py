from settings import get_settings
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

setting = get_settings()
def validate_database():
     engine = create_engine(setting.DB_URL) 
     if not database_exists(engine.url): # Checks for the first time  
         create_database(engine.url)     # Create new DB    
         print("New Database Created") # Verifies if database is there or not.
     else:
         print("Database Already Exists")

validate_database()