from socket import socket, gethostname
import tkinter
from datetime import datetime
import threading
import sqlite3
import json
import os

upisano = False

def upisUDatoteku(kupac, knjige, postoji):
    global upisano
    if postoji:
        f = open("narudzbine/" + kupac['imePrezime'] + ".txt", "a")
        f.write("\nNOVA NARUDZBINA\n"
                + "Ime i prezime: " + kupac['imePrezime'] + '\n'
                + "Adresa: " + kupac['adresa'] + '\n'
                + "Grad: " + kupac['grad'] + '\n'
                + "Broj telefona: " + kupac['brojTelefona'] + '\n'
                + knjige + '\n'
                + "Datum narudzbine: " + str(datetime.now().strftime("%d.%m.%Y. %H:%M:%S")))
        f.flush()
        f.close()
        upisano = True
        print("Sadrzaj uspesno unet u txt fajl!")
    else:
        f = open("narudzbine/" + kupac['imePrezime'] + ".txt", "w")
        f.write("NOVA NARUDZBINA\n"
                +"Ime i prezime: " + kupac['imePrezime'] + '\n'
                + "Adresa: " + kupac['adresa'] + '\n'
                + "Grad: " + kupac['grad'] + '\n'
                + "Broj telefona: " + kupac['brojTelefona'] + '\n'
                + knjige + '\n'
                + "Datum narudzbine: " + str(datetime.now().strftime("%d.%m.%Y. %H:%M:%S")))
        f.flush()
        f.close()
        upisano = True
        print("Sadrzaj uspesno unet u txt fajl!")

def sumaCena(listaCena):
    suma = 0
    for broj in listaCena:
        suma += int(broj)
    return suma

def kreirajCene(jednaCena):
        c = lambda x: x.split(" ")[1]
        # lambda uzima sve što joj se prosledi, splituje po razmaku i uzima drugi(1) indeks
        #c = jednaCena.split(" ")[1]
        return c(jednaCena)

def radServera():
    global upisano
    while True:
        lbServer.insert(0, "SERVER: waiting...")
        conn, addr = s.accept()
        req = conn.recv(1024).decode()

        if req != "":
            lbServer.insert(0, "Primljeni podaci...")
            temp = req.split('+')  # imePrezime,adresa,grad,brTel+[Knjiga,Knjiga]

            kupac = temp[0].split(",")

            kupacRecnik = {'imePrezime': kupac[0], 'adresa': kupac[1], 'grad': kupac[2], 'brojTelefona': kupac[3]}

            naruceneKnjige = temp[1]  # STRING --> ['Harry Potter (JKRowling) CENA: 340 din','Hunger Games (Suzan Collings) CENA: 340 din']

            tempListCena = naruceneKnjige.split("CENA:")

            # "['Lord of the Rings (J R R Tolkien) ",
            # " 750 din', 'Hunger Games (Susan Collins) ",
            # " 500 din']

            del(tempListCena[0])  # obrisati prvi iz liste jer sadrzi samo ime knjige (splitovano po CENA:)

            cene = list(map(kreirajCene, tempListCena))

            ukupnoZaPlacanje = sumaCena(cene)

            if not os.path.exists("narudzbine/" + kupacRecnik['imePrezime'] + ".txt"):
                open("narudzbine/" + kupacRecnik['imePrezime'] + ".txt", "w+")
                print("Kreiran txt fajl!")
                upisUDatoteku(kupacRecnik, naruceneKnjige, False)
            else:
                upisUDatoteku(kupacRecnik, naruceneKnjige, True)

            if upisano:
                lbServer.insert(0, "Primljena narudzbina.")
                odgovor = "USPESNO NARUCENO, CENA: " + str(ukupnoZaPlacanje) + " DIN"
                conn.send(odgovor.encode())
            else:
                odgovor ="NEUSPESNA NARUDZBINA"
                conn.send(odgovor.encode())

s = socket()
host = gethostname()
port = 3000
s.bind((host, port))
s.listen()

root = tkinter.Tk()
root.title("SERVER")
lbServer = tkinter.Listbox(root, selectmode=tkinter.SINGLE, width=55, height=35)
lbServer.pack()
t = threading.Thread(target=radServera)
t.start()
root.mainloop()