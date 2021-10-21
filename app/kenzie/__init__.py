import os
import dotenv

dotenv.load_dotenv()

directory = os.environ.get('FILES_DIRECTORY')
extensions = os.environ.get('ALLOWED_EXTENSIONS')

if not os.path.isdir(directory):
    os.mkdir(directory)

# ALLOWED_EXTENSIONS = os.environ.get('ALLOWED_EXTENSIONS')

MAX_CONTENT_LENGTH = os.environ.get('MAX_CONTENT_LENGTH')

