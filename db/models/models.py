# This file is used to create the metadata of all the models in the project.

# importing every model _mdl file from the directory
from .models import users_mdl

# setting the metadata to getting exported to the alembic/env.py file
base_metadata = users_mdl.Base.metadata