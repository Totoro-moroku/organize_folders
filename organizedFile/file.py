import os
import re
import shutil
import macos_tags

from datetime import datetime
from pathlib import Path
from itertools import groupby
from typing import Union

IGNORE_FILES = [
    ".DS_Store",
    r"[0-9]{4}-[0-9]{2}-[0-9]{2}"
]


def isIgnoreFile(file_name: str):
    for ignore_file_name in IGNORE_FILES:
        if re.search(ignore_file_name, file_name):
            return True

    return False


def getFiles(path: str):
    p_path = Path(path)

    if p_path.is_file():
        return list(filter(lambda file: not isIgnoreFile(file.name), [p_path]))

    return list(filter(lambda file: not isIgnoreFile(file.name), p_path.iterdir()))


def getEndDirName(path: str):
    p_path = Path(path).resolve()

    if p_path.is_file():
        return p_path.parent.name

    return p_path.name


def moveFiles(m_files: list, new_path: str):
    for file in m_files:
        print(file)
        shutil.move(file, new_path)


def addTagsToFile(file, tags: list):
    for tag in tags:
        macos_tags.add(tag, file=file)


def addTagsToFiles(at_files: list, tags: Union[str, list]):
    if type(tags) is str:
        tags = [tags]

    for file in at_files:
        addTagsToFile(file, tags)

        if file.is_dir():
            childFile = getFiles(file)
            addTagsToFiles(childFile, tags)

    return at_files


def createDateFolders(dates: list, path: str):
    for date, files in dates:
        new_path = Path(path).resolve() / Path(date)

        print(new_path)

        if not new_path.is_dir() and not os.path.exists(new_path):
            os.mkdir(new_path)


def timestampToStringDate(timeStamp, format="%Y-%m-%d"):
    return datetime.fromtimestamp(timeStamp).strftime(format)


def diffPath(path: str, toPath: str):
    if path == toPath:
        toPath += "整理済み"
        os.mkdir(toPath)

    return toPath


def organizedFiles(path, toPath):

    addTagsToFiles(getFiles(path), getEndDirName(path))

    files = getFiles(path)

    # toPath = diffPath(path, toPath)

    print(files)

    files.sort(key=lambda file: timestampToStringDate(
        os.stat(file.resolve()).st_atime))

    groupbyDateFiles = groupby(
        files, key=lambda file: timestampToStringDate(os.stat(file).st_atime))

    createDateFolders(groupbyDateFiles, toPath)

    groupbyDateFiles = groupby(
        files, key=lambda file: timestampToStringDate(os.stat(file).st_atime))

    for date, dateFiles in groupbyDateFiles:

        newPath = Path(toPath).resolve() / Path(date)

        moveFiles(dateFiles, newPath)
