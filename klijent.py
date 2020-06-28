from socket import socket, gethostname
from tkinter import *
from tkinter import font
import threading
import time
import json
import sqlite3

poslato = False
def posaljiZahtev():
    global poslato
    s = socket()
    host = gethostname()
    port = 3000
    s.connect((host, port))
    poslato = False

    if imePrezime.get() != "" and adresa.get() != "" and grad.get() != "" and brojTel.get() != "":
        if brojTel.get().startswith("06") and (len(brojTel.get()) == 9 or len(brojTel.get()) == 10):

            poslateKnjige = list()
            for k in lbKnjige.curselection():
                poslateKnjige.append(lbKnjige.get(k))

            if poslateKnjige.__len__() != 0:
                s.send(f"{imePrezime.get()},{adresa.get()},{grad.get()},{brojTel.get()}+{poslateKnjige}".encode())
                print('Poslato')
                poslato = True
            else:
                lbOdgovor.insert(0, "Niste odabrali nijednu knjigu.")
                s.close()
                return

        else:
            lbOdgovor.insert(0, "Molimo unesite validan broj telefona.")
            s.close()
            return
    else:
        lbOdgovor.insert(0, "Morate popuniti sve svoje podatke!")
        s.close()
        return

    if poslato:
        res = s.recv(1024).decode()
        lbOdgovor.insert(0, res)
    s.close()

def animacija():
    while True:
        rec = "Knjizara"
        temp = ""
        index = 0
        font1 = font.Font(root, family="Times New Roman", size=22, weight="bold")
        for slovo in rec:
            temp += rec[index]
            index += 1
            txtKnjizara = canvas.create_text(150, 40, fill="red", font=font1, text=temp)
            time.sleep(0.5)
            if temp == "Knjizara":
                temp = ""
                index = 0
            canvas.delete(txtKnjizara)
    else:
        canvas.delete(txtKnjizara)
        canvas.create_text(150, 40, fill="red", font=font.Font(root, family="Times New Roman", size=22, weight="bold"), text="Knjizara")

root = Tk()
root.title("KUPAC")

canvas = Canvas(root, bg="light goldenrod", height=80, width=300)
coord = 35, 45, 280, 170
canvas.pack(expand=True, fill=BOTH)

t1 = threading.Thread(target=animacija)
t1.setDaemon(True)
t1.start()

lbl0 = Label(root, text='Popunite Vaše podatke', bg='black', fg='orange', anchor=S)
lbl0.pack(fill=BOTH, expand=True)

lbl1 = Label(root, text='Vaše ime i prezime:', bg='orange', fg='black', anchor=W)
lbl1.pack(fill=BOTH, expand=True)

imePrezime = StringVar()
entryIme = Entry(root, textvariable=imePrezime)
entryIme.pack(fill=BOTH, expand=True)

lbl2 = Label(root, text='Vaša adresa:', bg='orange', fg='black', anchor=W)
lbl2.pack(fill=BOTH, expand=True)

adresa = StringVar()
entryAdresa = Entry(root, textvariable=adresa)
entryAdresa.pack(fill=BOTH, expand=True)

lbl3 = Label(root, text='Grad:', bg='orange', fg='black', anchor=W)
lbl3.pack(fill=BOTH, expand=True)

grad = StringVar()
entryGrad = Entry(root, textvariable=grad)
entryGrad.pack(fill=BOTH, expand=True)

lbl4 = Label(root, text='Broj telefona:', bg='orange', fg='black', anchor=W)
lbl4.pack(fill=BOTH, expand=True)

brojTel = StringVar()
entryTel = Entry(root,textvariable=brojTel)
entryTel.pack(fill=BOTH, expand=True)

lbl1 = Label(root, text='Označite knjige koje želite da poručite', bg='black', fg='orange', anchor=S)
lbl1.pack(fill=BOTH, expand=True)

def citajIzBaze():
    conn = sqlite3.connect("knjige.db")
    c = conn.cursor()
    myquery = ("SELECT * FROM knjige")
    c.execute(myquery)
    tempTuple = tuple(c.fetchall())
    return tempTuple

lbKnjige = Listbox(root, selectmode=MULTIPLE)

def popuniListBoxKnjige():
    lista = citajIzBaze()
    i = 0
    for knjiga in lista:
        lbKnjige.insert(i, knjiga[1] + " (" + knjiga[2] + ") CENA: " + str(knjiga[3]) + " din")
        i += 1
    lbKnjige.pack(fill=BOTH)

popuniListBoxKnjige()

dugme = Button(root, text="NARUČI", bg="green2", bd=2, command=posaljiZahtev)
dugme.pack(fill=BOTH, expand=True)

lblKnjizara = Label(root, text='Potvrda o narudžbini:')
lblKnjizara.pack(fill=BOTH, expand=True)

lbOdgovor = Listbox(root, selectmode=SINGLE)
lbOdgovor.pack(fill=BOTH, expand=True)

root.mainloop()