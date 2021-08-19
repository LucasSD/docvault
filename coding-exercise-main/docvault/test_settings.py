from .settings import *

# avoid accessing file system
DEFAULT_FILE_STORAGE = "inmemorystorage.InMemoryStorage"

SECRET_KEY = "dev"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
