import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from PyPDF2 import PdfReader
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from google.cloud import storage
import os
import time
import datetime
import re


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/90531/Documents/=EworldPartner/report-app-666-1d6bc3944d21.json"
cred = credentials.Certificate("C:/Users/90531/Documents/=EworldPartner/report-app-666-firebase-adminsdk-13k54-2f736e34e8.json")
firebase_admin.initialize_app(cred)
db = firestore.Client()
tasks_ref = db.collection(u'tasks')
################Config End########################


class Task(object):
    def __init__(self, title, stage, lastActivity, members = [], dueDate = None):
        self.title = title
        self.stage = stage
        self.lastActivity = lastActivity
        self.members = members
        self.dueDate = dueDate

    def to_dict(self):
        query = {
            u'Title': self.title,
            u'Stage': self.stage,
            u'Members': self.members,
            u'dueDate': self.dueDate,
            u'lastActivity': self.lastActivity
        }

        return query

    def __repr__(self):
        return(
            f'tasks(\
                Title={self.title}, \
                Stage={self.stage}, \
                lastActivity={self.lastActivity}, \
                Members={self.members}, \
                dueDate={self.dueDate}\
            )'
        )


##############APP#################
root = tk.Tk()
root.title('RepApp')
root.resizable(False, False)
root.geometry('550x250')

def readPdf(filename):
    rtrn = ""
    buffer = []
    pdfTxt = ""
    reader = PdfReader(open(filename, 'rb'))
    for page in reader.pages:
        pdfTxt += page.extractText()
    buffer = pdfTxt.split('\n')

    buf_iter = iter(buffer)
    for i in buf_iter:
        #print(i)
        if i.find("| Trello") != -1:
            next(buf_iter)
            next(buf_iter)
            next(buf_iter)
            next(buf_iter)
            next(buf_iter)
            continue
        elif i.find("Haftalık Görev Dağılımı") != -1:
            continue
        elif i.find("2022, ") != -1:
            i = i[0:len(i)-17]
            continue
        else:
            rtrn += i
            rtrn += "\n"
    #print(rtrn)
    return rtrn

def makeTasks(toParse):
    tasks = []
    stage = ""
    title = ""
    members = []
    dueDate = ""
    lastActivity = ""
    buffer = toParse.split('\n')

    buf_iter = iter(buffer)
    for line in buf_iter:
        if  line.find("Yapılması Gerekenler") != -1:
            stage = "Yapılması Gerekenler"
            continue
        elif line.find("Başladım") != -1:
            stage = "Başladım"
            continue
        elif line.find("Kontrol edilmeli") != -1:
            stage = "Kontrol edilmeli"
            continue
        elif line.find("Bitti") != -1:
            stage = "Bitti"
            continue
        elif line.find("Düzeltilecek") != -1:
            stage = "Düzeltilecek"
            continue
        elif line.find("SABİT GÖREVLER") != -1:
            stage = "SABİT GÖREVLER"
            continue
        elif line.find("Her Cuma/Hafta") != -1:
            stage = "Her Cuma/Hafta"
            continue
        elif line.find("Her Ay") != -1:
            stage = "Her Ay"
            continue

        if line.find(":") == -1:
            title = line
            continue
        elif line.find("Members") != -1:
            members = line.split(", ")
            members[0] = members[0].replace("Members: ", '')
            continue
        elif line.find("Due Date") != -1:
            dueDate = line
            dueDate = dueDate.replace("Due Date: ", '')
            continue
        elif line.find("Last Activity") != -1:
            lastActivity = line
            lastActivity = lastActivity.replace("Last Activity: ", '')
            tasks.append(Task(title, stage, lastActivity, members, dueDate))
            title = ""
            lastActivity = ""
            members = []
            dueDate = ""
            continue
    #print(tasks)
    return tasks

def open_text_file():
    # file type
    filetypes = (
        ('text files', '*.pdf'),
        ('All files', '*.*')
    )
    # show the open file dialog
    f = fd.askopenfilename(filetypes=filetypes)
    # read the text file and show its content on the Text
    text = readPdf(f)
    tasks = makeTasks(text)
    for task in tasks:
        print(task, "\n")
        tasks_ref.document().set(task.to_dict())

open_button = ttk.Button(
    root,
    text='Open a File',
    command=open_text_file
)


open_button.pack(expand=True)


# run the application
root.mainloop()
