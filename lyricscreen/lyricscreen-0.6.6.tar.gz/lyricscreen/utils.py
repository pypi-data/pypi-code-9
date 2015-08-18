import os

def directory_entries(dir, base=".", mustEndWith="", mustStartWith=""):
    entries = []
    baseDir = dir
    for dirName, subDirs, files in os.walk(baseDir):
        bd = base + dirName.replace(baseDir, '').replace('\\', '/')
        for f in files:
            if f.endswith(mustEndWith) and f.startswith(mustStartWith):
                entries.append(bd + '/' + f)
    return entries
