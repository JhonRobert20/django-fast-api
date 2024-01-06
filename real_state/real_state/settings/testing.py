import os

from real_state.settings.base import *  # noqa

MONGO_DB_DATABASE = os.environ.get("MONGO_DB_DATABASE", "test")

# These users will be removed after tests
CSV_FILE_PATH = "users_testing.csv"
