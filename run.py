import os
import sys
import tkinter as tk
from tkinter import messagebox as tkMessageBox
import shutil
from pathvalidate import ValidationError, validate_filename, validate_filepath
from mastertemplates import *
import re


class CreateJobApp(tk.Tk):
    """docstring for CreateJobApp"""
    def __init__(self):
        # Initialize the gui
        tk.Tk.__init__(self)

        departments = [
            ('Civil',1),
            ('Environmental',2),
            ('Structural',3)
        ]

        self.deptvar = tk.IntVar()
        self.statusmsgtxt = tk.StringVar()

        self.wm_title("Create Job")

        tk.Label(
            self, 
            text="Select Department",
            padx=20
        ).grid(row=0,column=0)
        
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
                value=val,
                command=self.on_select_department
            )
            self.departselect.grid(row=r,column=0)
            r+=1

    def trace_calls_and_returns(frame, event, arg):
        co = frame.f_code
        func_name = co.co_name
        if func_name == 'write':
            # Ignore write() calls from print statements
            return
        line_no = frame.f_lineno
        filename = co.co_filename
        if event == 'call':
            print('Call to %s on line %s of %s' % (func_name, line_no, filename))
            return trace_calls_and_returns
        elif event == 'return':
            print('%s => %s' % (func_name, arg))
        return

    def validate_form(self):
        # department was selected and template is accessible
        if self.deptvar.get() == 0:
            self.statusmsgtxt.set("Select department.")
            raise ValueError("Department selection out of range.")
        else:
            self.departnum = self.deptvar.get()
            self.templatesource = templatepathdict[self.departnum]
            if not os.path.exists(self.templatesource[1]):
                self.statusmsgtxt.set(
                    "Cannot locate template. Check network connection."
                    )
                raise ValueError(
                    "Cannot locate template. Check network connection."
                    )
            # structural think's they're special
            self.is_structural = True if self.departnum == 3 else False

        # job number isnt blank
        if self.jobnum.get() == "":
            self.statusmsgtxt.set("Enter number.")
            raise ValueError("Job number out of range")
        else:
            self.jobnumtxt = self.jobnum.get()

        # job name isnt blank
        if self.jobname.get() == "":
            self.statusmsgtxt.set("Enter name.")
            raise ValueError("Job name out of range")
        else:
            self.jobnametxt = self.jobname.get()

        # Server has been selected
        if (self.server_var.get() is None) or (self.server_var.get() == ""):
            self.statusmsgtxt.set("Select a target drive.")
            raise ValueError("No target server selected")
        else:
            pass

        # Job name and number dont have illegal charachters
        try:
            validate_filename(self.jobnametxt)
        except ValidationError as e:
            self.statusmsgtxt.set(e.reason.name)
            raise ValueError("{}\n".format(e))

        try:
            validate_filename(self.jobnumtxt)
        except ValidationError as e:
            self.statusmsgtxt.set(e.reason.name)
            raise ValueError("{}\n".format(e))

        # target directory is valid and doesnt already exist
        intent_dir = self.server_path + '/' + self.jobnum.get()
        if self.is_structural: #structural adds the name to the path
            intent_dir = intent_dir + " " + self.jobnametxt
        
        try:
            validate_filepath(intent_dir, "auto")
        except ValidationError as e:
            self.statusmsgtxt.set(e.reason.name)
            raise ValueError(e)

        if os.path.isdir(intent_dir):
            self.statusmsgtxt.set("Folder already exists.")
            raise ValueError("Folder already exists")
        else:
            self.intent_dir = intent_dir

        # target directory is valid
        if not os.path.exists(self.server_path):
            self.statusmsgtxt.set("Invalid target directory.")
            raise ValueError("Invalid target")
        else:
            pass

        popup_text = 'Press OK to begin. Process may take a while.'
        if tkMessageBox.askokcancel("Alert", popup_text):
            self.statusmsgtxt.set(" ")
            return True
        else:
            self.statusmsgtxt.set("Cancelled by user.")
            raise ValueError("Cancelled by User")

    def createjobfolder(self):
        if self.validate_form():
            print("Validation passed, initializing...")
            departmentname, templatepath = self.templatesource

            print("Fetching templates")

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

            # Copy the MasterC3D.dwt (if civil job)
            if self.departnum == 1: #i.e. is civil
                template_dest = self.intent_dir + '/' + r'\Drawings\Templates'
                try:
                    shutil.copytree(masterc3d_source, template_dest, dirs_exist_ok=True)
                except shutil.Error as e:
                    print('Directory not coppied. Error: %s' % e)

            print("Copy operation completed.")

            tkMessageBox.showinfo("Success", "Job Folder Created")
            self.destroy()

    def set_server(self, arg):
        self.server_name = self.server_var.get()
        #print('server name: ' + self.server_name)
        self.server_path = serverpathdict[self.server_name]
        #print('server path: ' + self.server_path)

    def on_select_department(self):
        try:
            self.serverlabel.destroy()
            self.pathentry.destroy()
        except:
            pass

        self.serverlabel = tk.Label(
            self,
            text="Server"
        )
        self.serverlabel.grid(row=0,column=3)

        self.server_var = tk.StringVar(self)
        dept_var = self.deptvar.get()
        server_list = serverlistdict[dept_var]
        optionlist = []
        for pair in server_list:
            optionlist.append(pair)

        self.pathentry = tk.OptionMenu(
            self,
            self.server_var,
            *optionlist,
            command=self.set_server
        )
        self.pathentry.grid(row=0,column=4)


    def on_submit(self):
        self.statusmsgtxt.set(" ")
        self.createjobfolder()


if __name__ == "__main__":
    w = CreateJobApp()
    w.mainloop()
