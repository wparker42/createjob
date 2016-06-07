import os
import sys
import tkinter as tk
import shutil
from tkinter import filedialog
from mastertemplates import templatepathdict
import re


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

    def createjobfolder(self):
        departmentname, templatepath = self.templatesource
        intent_dir = self.intent_dir
        print(departmentname, templatepath)
        print('Parsing Master Folder and cloning into ' + intent_dir)
        try:
            shutil.copytree(templatepath, intent_dir)
        # Directories are the same
        except shutil.Error as e:
            print('Directory not copied. Error: %s' % e)
        # Any error saying that the directory doesn't exist
        except OSError as e:
            print('Directory not copied. Error: %s' % e)

        for root, dirs, files in os.walk(intent_dir):
            # Exclude hidden files and folders
            files = [f for f in files if not f[0] == '.']
            dirs[:] = [d for d in dirs if not d[0] == '.']
            for f in files:
                oldfilepath = os.path.join(root, f)
                newfilename = self.jobnumtxt + ' - ' + f
                newfilepath = os.path.join(root, newfilename)
                os.rename(oldfilepath, newfilepath)
        pass

    def on_submit(self):
        self.jobnametxt = self.jobname.get()
        self.jobnumtxt = self.jobnum.get()
        self.departnum = self.deptvar.get()
        self.templatesource = templatepathdict[self.departnum]
        self.checkiffolderexists()
        self.createjobfolder()
        print("Done.")

if __name__ == "__main__":
    w = CreateJobApp()
    w.mainloop()

