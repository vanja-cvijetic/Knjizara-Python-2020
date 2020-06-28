from tkinter import *
import threading
import time
import sqlite3
from tkinter import messagebox
import json
from tkinter import font
import os

class Knjiga:
    def __init__(self, id, naslov, autor, cena):
        self.id = id
        self.naslov = naslov
        self.autor = autor
        self.cena = cena

    def to_json(self):
        return json.dumps(self.__dict__)  # dumps konvertuje u json format

    @classmethod
    def from_json(cls, json_str):
        json_dict = json.loads(json_str)  # loads vraca u objekat klase
        return cls(**json_dict)

def napraviBazu():
    conn = sqlite3.connect('knjige.db')
    c = conn.cursor()

    # proverava da li tabela knjige već postoji
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='knjige' ''')

    # ako izbroji 1, tabela postoji
    if c.fetchone()[0] == 1:
        conn.close()
        print('Baza vec postoji')
    else:
        queryCreate = 'CREATE TABLE KNJIGE(ID INT PRIMARY KEY NOT NULL,NASLOV TEXT NOT NULL,AUTOR TEXT NOT NULL,CENA INT NOT NULL)'
        knjiga1 = "INSERT INTO KNJIGE \
                        VALUES (1, 'Harry Potter', 'J K Rowling', 990)"
        knjiga2 = "INSERT INTO KNJIGE \
                        VALUES (2, 'Lord of the Rings', 'J R R Tolkien', 750)"
        knjiga3 = "INSERT INTO KNJIGE \
                        VALUES (3, 'The Hunger Games', 'Susan Collins', 500)"
        knjiga4 = "INSERT INTO KNJIGE \
                                VALUES (4, 'Twillight', 'Stephenie Meyer', 400)"
        knjiga5 = "INSERT INTO KNJIGE \
                                VALUES (5, 'Rising Strong', 'Brene Brown', 1210)"
        conn.execute(queryCreate)
        conn.execute(knjiga1)
        conn.execute(knjiga2)
        conn.execute(knjiga3)
        conn.execute(knjiga4)
        conn.execute(knjiga5)
        conn.commit()
        conn.close()

def citajIzBaze():
    conn = sqlite3.connect("knjige.db")
    c = conn.cursor()
    myquery = ("SELECT * FROM knjige")
    c.execute(myquery)
    tempTuple = tuple(c.fetchall())
    return tempTuple

listaIzbrisanih = list()

def ukloniKnjigu():
    knjiga = lbKnjige.get(lbKnjige.curselection())
    print("Uklanja se: " + str(knjiga))

    id_knjige = knjiga.split("ID: ")[1]
    id_knjige = int(id_knjige.split(",")[0])

    print(id_knjige)

    niz_knjige = knjiga.split(", ")
    naslov_knjige = niz_knjige[1]
    autor_knjige = niz_knjige[2]
    cena_knjige = niz_knjige[3]

    knjiga = Knjiga(id_knjige,naslov_knjige,autor_knjige,cena_knjige)

    conn = sqlite3.connect("knjige.db")
    c = conn.cursor()
    myquery = ("DELETE FROM knjige WHERE id=" + str(id_knjige))
    c.execute(myquery)
    conn.commit()
    popuniListBoxKnjige()

    knjigaJson = knjiga.to_json()

    naslovKnjige = knjiga.naslov.replace(" ", "")

    if not os.path.exists("obrisane/" + naslovKnjige + ".json"):
        open("obrisane/" + naslovKnjige + ".json", "w+")
        print("Kreiran json fajl!")
        f = open("obrisane/" + naslovKnjige + ".json", "a")
        f.write(knjigaJson)
        f.flush()
        f.close()
        print("Sadrzaj uspesno unet u json fajl!")
    else:
        f = open("obrisane/" + naslovKnjige + ".json", "w")
        f.write(knjigaJson)
        f.flush()
        f.close()
        print("Sadrzaj uspesno unet u json fajl!")

def dodajKnjigu():
    global naslov
    global autor
    global cena
    conn = sqlite3.connect("knjige.db")
    c = conn.cursor()
    myquery1 = ("SELECT MAX(id) FROM knjige")
    c.execute(myquery1)
    for row in c:
        noviId = int(str(row)[1])+1
    noviNaslov = naslov.get()
    noviAutor = autor.get()
    novaCena = int(cena.get())
    myquery2 = f"INSERT INTO KNJIGE (ID,NASLOV,AUTOR,CENA) \
                VALUES ({noviId},\"{noviNaslov}\",\"{noviAutor}\",{novaCena})"
    conn.execute(myquery2)
    conn.commit()
    popuniListBoxKnjige()

root = Tk()
root.title("ADMINISTRATOR")
font1 = font.Font(root, family="Times New Roman", size=14, weight="bold")

lbl0 = Label(root, text='Dodavanje nove knjige u bazu', font=font1, bg='orange', fg='black')
lbl0.pack(fill=BOTH, expand=True)

lbl1 = Label(root, text='Naslov:', bg='orange', fg='black', anchor=W)
lbl1.pack(fill=BOTH, expand=True)

naslov = StringVar()
entryNaslov = Entry(root, textvariable=naslov)
entryNaslov.pack(fill=BOTH, expand=True)

lbl2 = Label(root, text='Autor:', bg='orange', fg='black', anchor=W)
lbl2.pack(fill=BOTH, expand=True)

autor = StringVar()
entryAutor = Entry(root, textvariable=autor)
entryAutor.pack(fill=BOTH, expand=True)

lbl3 = Label(root, text='Cena (RSD):', bg='orange', fg='black', anchor=W)
lbl3.pack(fill=BOTH, expand=True)

cena = StringVar()
entryCena = Entry(root, textvariable=cena)
entryCena.pack(fill=BOTH, expand=True)

btnDodaj = Button(root, text="DODAJ KNJIGU", bg="gray", fg="black", bd=4, command=dodajKnjigu)
btnDodaj.pack(fill=BOTH, expand=True)

lbl4 = Label(root, text='Izaberite knjigu koja više nije na stanju:', bg='orange', fg='black', anchor=W)
lbl4.pack(fill=BOTH, expand=True)

lbKnjige = Listbox(root, selectmode=SINGLE, width=60)

def popuniListBoxKnjige():
    lbKnjige.delete('0', 'end')
    lista = citajIzBaze()
    i = 0
    for knjiga in lista:
        lbKnjige.insert(i, "ID: " + str(knjiga[0]) + ", " + knjiga[1] + ", " + knjiga[2] + ", " + str(knjiga[3]))
        i += 1
    lbKnjige.pack(fill=BOTH)

popuniListBoxKnjige()

btnIzbrisi = Button(root, text="UKLONI KNJIGU", bg="gray", fg="black", bd=4, command=ukloniKnjigu)
btnIzbrisi.pack(fill=BOTH, expand=True)

root.mainloop()