import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from PyPDF2 import PdfReader
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from google.cloud import storage
import os


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/90531/Documents/=EworldPartner/report-app-666-1d6bc3944d21.json"
storage_client = storage.Client()
cred = credentials.Certificate("C:/Users/90531/Documents/=EworldPartner/report-app-666-firebase-adminsdk-13k54-2f736e34e8.json")
firebase_admin.initialize_app(cred)



def get_check_exists():
    db = firestore.Client()
    # [START firestore_data_get_as_map]
    doc_ref = db.collection(u'User').document(u'e4RuH26D0yo7iFKJrRpd')

    doc = doc_ref.get()
    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
    else:
        print(u'No such document!')

get_check_exists()
# Root window
root = tk.Tk()
root.title('RepApp')
root.resizable(False, False)
root.geometry('550x250')

def readPdf(filename):
    reader = PdfReader(open(filename, 'rb'))
    for page in reader.pages:
        print(page.extractText())


def open_text_file():
    # file type
    filetypes = (
        ('text files', '*.pdf'),
        ('All files', '*.*')
    )
    # show the open file dialog
    f = fd.askopenfilename(filetypes=filetypes)
    # read the text file and show its content on the Text
    readPdf(f)


# open file button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=open_text_file
)


open_button.pack(expand=True)


# run the application
root.mainloop()
