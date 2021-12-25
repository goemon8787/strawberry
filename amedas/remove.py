import os

path = "/home/yamashitakeisuke/Documents/strawberry/data/amedas/"
dirlist = [d for d in os.listdir(path) if os.path.isdir(path + d)]

for d in dirlist:
    dpath = path + d
    filelist = os.listdir(dpath)
    for f in filelist:
        if f[0] != "d":
            os.remove(dpath + os.sep + f)
