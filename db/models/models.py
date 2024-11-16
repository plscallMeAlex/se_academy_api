# This file is used to create the metadata of all the models in the project.

# importing every model _mdl file from the directory
from db.models import (
    user_mdl,
    token_mdl,
    category_mdl,
    enrolled_mdl,
    course_mdl,
    achievement_mdl,
    quiz_mdl,
)

# setting the metadata to getting exported to the alembic/env.py file
base_metadata = user_mdl.Base.metadata
