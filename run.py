import os
import sys
import tkinter as tk
from tkinter import filedialog
from mastertemplates import templatepathdict as paths


class CreateJobApp(tk.Tk):
    """docstring for CreateJobApp"""
    def __init__(self):
        tk.Tk.__init__(self)

        departments = [
            ('Civil',1),
            ('Environmental',2),
            ('Structural',3)
        ]

        self.deptvar = tk.IntVar()
        self.drivevar = tk.StringVar()

        # Remove after testing
        self.drivevar.set("/Users/tynan/Documents/Projects/createjob/directories/outputs")

        self.wm_title("Create Job")

        tk.Label(
            self, 
            text="Select Department",
            padx=20
        ).grid(row=0,column=0)
        
        tk.Label(
            self,
            text="Drive"
        ).grid(row=0,column=3)

        tk.Label(
            self,
            text="Job Number"
        ).grid(row=1,column=3)

        tk.Label(
            self,
            text="Job Name"
        ).grid(row=3,column=3)

        self.pathentry = tk.Entry(self, textvariable=self.drivevar)
        self.pathentry.grid(row=0,column=4)

        self.drivebrowse = tk.Button(
            self,
            text="Browse",
            command=self.on_browse
        )
        self.drivebrowse.grid(row=0,column=5)

        self.jobnum = tk.Entry(self)
        self.jobnum.grid(row=1,column=4)

        self.jobname = tk.Entry(self)
        self.jobname.grid(row=3,column=4)

        self.submit = tk.Button(
            self,
            text="Create Job",
            command=self.on_submit
        )
        self.submit.grid(row=4,column=0)

        r = 1
        for txt, val in departments:
            self.departselect = tk.Radiobutton(
                self,
                indicatoron=0,
                text=txt,
                width=20,
                padx=20, 
                variable=self.deptvar,
                value=val)
            self.departselect.grid(row=r,column=0)
            r+=1

    def on_browse(self):
        self.targetdirectory = filedialog.askdirectory()
        print(self.targetdirectory)
        self.drivevar.set(self.targetdirectory)

    def checkiffolderexists(self):
        print("Checking target directory...")
        intent_dir = self.drivevar.get() + '/' + self.jobnumtxt
        if os.path.isdir(intent_dir):
            raise ValueError("Folder already exists")
        else:
            self.intent_dir = intent_dir
            pass

    def generatejobfolder(self):
        self.checkiffolderexists()
        destdirectory = self.intent_dir
        if not os.path.exists(destdirectory):
            os.makedirs(destdirectory)

        exlcudes = ['.','!']
        with open(self.textfile, 'r') as f:
            lines = f.read().splitlines()

            for line in lines:
                if line[:1] not in exlcudes:
                    newdirectory = destdirectory + '/' + line
                    print(newdirectory)
                    os.makedirs(newdirectory)

            f.close()
        pass

    def generatefile(self):
        departmentname, dirpaths = self.departmentpair
        rootdirectory, textfile = dirpaths
        self.textfile = textfile

        # Delete old text file
        if os.path.exists(textfile):
            os.remove(textfile)

        print('Parsing Master Folder and creating outputs...')
        for root, dirs, files in os.walk(rootdirectory):
            # Exclude hidden files and folders
            files = [f for f in files if not f[0] == '.']
            dirs[:] = [d for d in dirs if not d[0] == '.']
            with open(textfile, "a") as out_file:
                relpath = os.path.relpath(root, rootdirectory)
                out_file.write(relpath+'\n')
                for f in files:
                    out_file.write("!"+root+'/'+f+'|'+relpath+'/#'+f+'\n')
                out_file.close()
        self.generatejobfolder()

    def on_submit(self):
        self.jobnametxt = self.jobname.get()
        self.jobnumtxt = self.jobnum.get()
        self.departnum = self.deptvar.get()
        self.departmentpair = paths[self.departnum]
        self.generatefile()

if __name__ == "__main__":
    w = CreateJobApp()
    w.mainloop()

