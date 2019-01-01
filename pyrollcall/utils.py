# -*- encoding: utf-8 -*-

from datetime import datetime
from pathlib import Path

def mkdir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)

def get_datestamp():
    return datetime.now().strftime("%Y/%m/%d")

def get_datetimestamp():
    return datetime.now().strftime("%Y/%m/%d %H:%M")
