import os
import copy
import shutil
import macos_tags

from datetime import datetime
from pathlib import Path
from itertools import groupby
from typing import Union

IGNORE_FILES = [
  ".DS_Store"
]

def isIgnoreFile(file_name: str):
  return file_name in IGNORE_FILES

def getFiles(path: str):
  p_path = Path(path)

  if p_path.is_file():
    return list(filter(lambda file: not isIgnoreFile(file.name), [p_path]))

  return  list(filter(lambda file: not isIgnoreFile(file.name), p_path.iterdir()))


def getEndDirName(path: str):
  p_path = Path(path).resolve()

  if p_path.is_file():
    return p_path.parent.name

  return p_path.name


def moveFiles(m_files:list , new_path: str):
  for file in m_files:
    print(file)
    shutil.move(file, new_path)


def addTagsToFile(file, tags:list):
  for tag in tags:
    macos_tags.add(tag, file = file)


def addTagsToFiles(at_files:list, tags:Union[str,list]):
  if type(tags) is str:
    tags = [tags]

  for file in at_files:
    addTagsToFile(file, tags)

    if file.is_dir():
      childFile = getFiles(file)
      addTagsToFiles(childFile, tags)

  return at_files



def createDateFolders(dates: list, path:str):
  for date, files in dates:
    new_path = Path(path).resolve() / Path(date)

    print(new_path)

    if not new_path.is_dir():
      os.mkdir(new_path)


def timestampToStrinDate(timeStamp,format="%Y-%m-%d"):
  return datetime.fromtimestamp(timeStamp).strftime(format)


def organizedFiles(path, toPath):
  addTagsToFiles(getFiles(path), getEndDirName(path))

  files = getFiles(path)

  files.sort(key=lambda file: timestampToStrinDate(os.stat(file.resolve()).st_atime))

  groupbyDateFiles = groupby(files, key=lambda file: timestampToStrinDate(os.stat(file).st_atime))

  createDateFolders(groupbyDateFiles, toPath)

  groupbyDateFiles =  groupby(files, key=lambda file: timestampToStrinDate(os.stat(file).st_atime))

  for date ,dateFiles in groupbyDateFiles:

    newPath = Path(toPath).resolve() / Path(date)

    moveFiles(dateFiles, newPath)