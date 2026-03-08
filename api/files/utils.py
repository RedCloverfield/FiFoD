from os import stat_result

import asyncio
from pathlib import Path


async def scan_directory(directory: Path) -> list[Path]:
    '''
    Возвращает список экземляров класса :class:`Path` - файлов, загруженных на
    сервер.
    '''
    return await asyncio.to_thread(lambda: list(directory.iterdir()))


async def get_file_meta(path: Path) -> stat_result:
    '''
    Возвращает метаданные файла.
    '''
    return await asyncio.to_thread(path.stat)
