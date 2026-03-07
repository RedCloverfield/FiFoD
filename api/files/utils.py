from os import stat_result

import asyncio
from pathlib import Path


async def scan_directory(directory: Path) -> list[Path]:
    return await asyncio.to_thread(lambda: list(directory.iterdir()))


async def get_file_meta(path: Path) -> stat_result:
    return await asyncio.to_thread(path.stat)
