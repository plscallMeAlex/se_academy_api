# This file is used to create the metadata of all the models in the project.

# importing every model _mdl file from the directory
from db.models import token_mdl, user_mdl

# setting the metadata to getting exported to the alembic/env.py file
base_metadata = user_mdl.Base.metadata

# storing all enum types
from enum import Enum

class RoleEnum(str, Enum):
    freshman = "freshman"
    sophomore = "sophomore"
    junior = "junior"
    senior = "senior"
    graduate = "graduate"
    admin = "admin"

class StatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"