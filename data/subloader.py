import os

from ujson import loads # pip install ujson
import aiofiles # pip install aiofiles


async def get_json(filename: str) -> list:
    path = f"data/{filename}"

    if os.path.exists(path):
        async with aiofiles.open(path, "r", encoding="utf-8") as file:
            return loads(await file.read())
    return []

async def show_message(text: str, to_show_hint: bool = False, hint: str = ""):
    if to_show_hint:
        text = f"{text}\n\n<i>Подсказка:\n<span class='tg-spoiler'>{hint}</span></i>"
    return text