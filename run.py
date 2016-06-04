import os
import sys
import tkinter as tk

class CreateJobApp(tk.Tk):
    """docstring for CreateJobApp"""
    def __init__(self):
        tk.Tk.__init__(self)

        departments = [
            ('Civil',1),
            ('Environmental',2),
            ('Structural',3)
        ]

        deptvar = tk.IntVar()

        self.wm_title("Create Job")

        tk.Label(
            self, 
            text="Select Department",
            padx=20
        ).grid(row=0,column=0)

        tk.Label(
            self,
            text="Job Number"
        ).grid(row=0,column=3)

        self.jobnum = tk.Entry(self).grid(row=1,column=3)

        r = 1
        for txt, val in departments:
            self.departselect = tk.Radiobutton(
                self,
                indicatoron=0,
                text=txt,
                width=20,
                padx=20, 
                variable=deptvar,
                value=val).grid(row=r,column=0)
            r+=1

w = CreateJobApp()
w.mainloop()


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
                out_file.write("!"+path+'/'+f+'|'+relpath+'/#'+f+'\n')
            out_file.close()

generatefile()
