import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from PyPDF2 import PdfReader

# Root window
root = tk.Tk()
root.title('RepApp')
root.resizable(False, False)
root.geometry('550x250')

def readPdf(filename):
    reader = PdfReader(open(filename, 'rb'))
    page = reader.pages[0]
    print(page.extract_text())
    page = reader.pages[1]
    print(page.extract_text())
    filename.close()


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
