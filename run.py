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

        self.deptvar = tk.IntVar()

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

        tk.Label(
            self,
            text="Job Name"
        ).grid(row=2,column=3)

        self.jobnum = tk.Entry(self)
        self.jobnum.grid(row=1,column=3)

        self.jobname = tk.Entry(self)
        self.jobname.grid(row=3,column=3)

        self.submit = tk.Button(
            self,
            text="Create Job",
            command=self.on_button
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

    def on_button(self):
        print(self.jobname.get())
        self.jobnametxt = self.jobname.get()
        print(self.jobnum.get())
        self.jobnumtxt = self.jobnum.get()
        print(self.deptvar.get())
        self.departselecttxt = self.deptvar.get()

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
