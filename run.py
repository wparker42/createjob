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
        self.statusmsgtxt = tk.StringVar()

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

        self.statusmsg = tk.Label(self, textvariable=self.statusmsgtxt)
        self.statusmsg.grid(row=5, column=1, columnspan=5, sticky="W")

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
        self.submit.grid(row=4,column=4)

        r = 1
        for txt, val in departments:
            self.departselect = tk.Radiobutton(
                self,
                indicatoron=0,
                text=txt,
                width=20,
                padx=20,
                variable=self.deptvar,
                value=val
            )
            self.departselect.grid(row=r,column=0)
            r+=1


    def on_browse(self):
        self.targetdirectory = filedialog.askdirectory()
        self.drivevar.set(self.targetdirectory)


    def validate_form(self):
        # department was selected
        if self.deptvar.get() == 0:
            self.statusmsgtxt.set("Select department.")
            raise ValueError("Department selection out of range")
        else:
            self.departnum = self.deptvar.get()
            self.templatesource = templatepathdict[self.departnum]
            # structural think's they're special
            self.is_structural = True if self.departnum == 3 else False

        # job number isnt blank
        if self.jobnum.get() is "":
            self.statusmsgtxt.set("Enter number.")
            raise ValueError("Job number out of range")
        else:
            self.jobnumtxt = self.jobnum.get()

        # job name isnt blank
        if self.jobname.get() is "":
            self.statusmsgtxt.set("Enter name.")
            raise ValueError("Job name out of range")
        else:
            self.jobnametxt = self.jobname.get()

        # target directory doesnt already exist
        intent_dir = self.drivevar.get() + '/' + self.jobnum.get()
        if self.is_structural:
            intent_dir = intent_dir + " " + self.jobnametxt
        if os.path.isdir(intent_dir):
            self.statusmsgtxt.set("Folder already exists.")
            raise ValueError("Folder already exists")
        else:
            self.intent_dir = intent_dir

        # target directory is valid
        if not os.path.exists(self.drivevar.get()):
            self.statusmsgtxt.set("Invalid target directory.")
            raise ValueError("Invalid target")
        else:
            disp = 'Parsing Master Folder and cloning into ' + intent_dir
            self.statusmsgtxt.set(disp)

        self.statusmsgtxt.set("Validation passed.")
        return True


    def createjobfolder(self):
        if self.validate_form():
            departmentname, templatepath = self.templatesource

            # Copy tree operation
            try:
                shutil.copytree(templatepath, self.intent_dir)
            # Directories are the same
            except shutil.Error as e:
                print('Directory not copied. Error: %s' % e)
            # Any error saying that the directory doesn't exist
            except OSError as e:
                print('Directory not copied. Error: %s' % e)

            # Rename file & folder operation
            for root, dirs, files in os.walk(self.intent_dir):
                # Exclude hidden files and folders
                files = [f for f in files if not f[0] == '.']
                dirs[:] = [d for d in dirs if not d[0] == '.']
                for f in files:
                    oldfilepath = os.path.join(root, f)
                    newfilename = self.jobnumtxt + ' - ' + f
                    newfilepath = os.path.join(root, newfilename)
                    os.rename(oldfilepath, newfilepath)
                for d in dirs:
                    if d[:1] == "_":
                        olddirectoryname = os.path.join(root, d)
                        newdirectoryname = "_" + self.jobnametxt
                        newdirpath = os.path.join(root, newdirectoryname)
                        os.rename(olddirectoryname, newdirpath)


    def on_submit(self):
        self.createjobfolder()
        self.statusmsgtxt.set("Job folder created.")


if __name__ == "__main__":
    w = CreateJobApp()
    w.mainloop()
