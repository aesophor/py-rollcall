# -*- encoding: utf-8 -*-

from datetime import datetime
from pathlib import Path
from imutils import paths

def mkdir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)

def list_images(path: str):
    return list(paths.list_images(path))

def get_datestamp():
    return datetime.now().strftime("%Y/%m/%d")

def get_datetimestamp():
    return datetime.now().strftime("%Y/%m/%d %H:%M")
