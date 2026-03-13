from pathlib import Path
from ..config import settings

APPROPRIATE_FILE_EXT = ('.jpg', '.png', '.gif', '.jpeg', '.bmp')
FILES_STORAGE_PATH = Path(settings.files_storage_dir)
API_ROOT_URL = '/api/v1'
