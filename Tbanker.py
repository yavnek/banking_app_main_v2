#imports
from tkinter import *
import os
from PIL import ImageTk, Image
import socket
import threading



#Main Screen
master = Tk()
master.title('Banking Workers App')

#Image import
img = Image.open('secure.png')
img = img.resize((150,150))
img = ImageTk.PhotoImage(img)

#Labels
Label(master, text = "Banking Work Terminal", font=('Calibri',14)).grid(row=0,sticky=N,pady=10)
Label(master, text = "We make clients happy by making us happy", font=('Calibri',12)).grid(row=1,sticky=N)
Label(master, image=img).grid(row=2,sticky=N,pady=15)

#Buttons
Button(master, text="Login", font=('Calibri',12),width=20).grid(row=3,sticky=N,pady=10)
Button(master, text="Close", command = master.destroy, font=('Calibri',12)).grid(row=4,sticky=N,pady=10,padx=10)
master.mainloop()
