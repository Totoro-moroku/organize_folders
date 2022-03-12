import os
import shutil
from datetime import datetime
from itertools import groupby
import schedule
from time import sleep

import macos_tags

import config


def timestampToStrinDate(timeStamp,format="%Y%m%d"):
  return datetime.fromtimestamp(timeStamp).strftime(format)


def createIfFolderNo(path):
  if not os.path.exists(path):
    os.mkdir(path)


def createTag(path):
 return(os.path.split(os.path.dirname(path))[1])


def moveFiles(files,new_path,tag):
  for file in files:
    print("file:",file)

    if file == ".DS_Store":
      continue

    print("new_path:",new_path)
    macos_tags.add(tag,file = file)
    shutil.move(file, new_path)


def createDateFolder(dates,tag):
  for date,files in dates:

    strDate = date

    path = os.path.join(config.AFTER_ORGANIZE_PATH,strDate)

    createIfFolderNo(path)

    print(path)

    moveFiles(files, path,tag)

  return dates



def organizedFiles(path):
  os.chdir(path)

  files = os.listdir()

  files.sort(key=lambda file:timestampToStrinDate(os.stat(file).st_atime))
  groupbyDateFiles = groupby(files, key=lambda file:timestampToStrinDate(os.stat(file).st_atime))

  print("data",groupbyDateFiles)

  tag= createTag(path)
  createDateFolder(groupbyDateFiles,tag)


def task():
  organizedFiles(config.BRAVE_PATH)
  organizedFiles(config.SLACK_PATH)



schedule.every().days.at("00:00").do(task)

while True:
    schedule.run_pending()
    sleep(1)

