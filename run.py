import os
import sys


def generatefile():

    #rootpath = "directories/env/9999c/"
    rootpath = sys.argv[1]
    newfile = sys.argv[2]

    # Delete old text file
    #os.remove("textfiles/env.txt")
    if os.path.exists(newfile):
        os.remove(newfile)

    for path, dirs, files in os.walk(rootpath):
        with open(newfile, "a") as out_file:
            relpath = os.path.relpath(path, rootpath)
            out_file.write(relpath+'\n')
            for f in files:
                out_file.write("!"+path+'/'+f+','+relpath+'/#'+f+'\n')
            out_file.close()

generatefile()
