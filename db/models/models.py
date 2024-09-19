# This file is used to create the metadata of all the models in the project.

# importing every model _mdl file from the directory
from db.models import token_mdl, user_mdl

# setting the metadata to getting exported to the alembic/env.py file
base_metadata = user_mdl.Base.metadata