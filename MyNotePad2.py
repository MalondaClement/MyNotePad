## Semaine 3
## Malonda Clément
## Projet POO

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter.font as tkFont
from PIL import Image, ImageTk
from functools import partial
import os
import platform

filepath = None

#Gestion des OS pour les raccourcis clavier
if platform.system() == "Darwin":
    # si l'os est MacOS
    keyName = "Control"
elif platform.system() == "Windows":
    # si l'os est Windows
    keyName = "Alt"
else :
    #pour linux
    pass

class MyCommand():
    """ Classe MyCommand
        Cette classe permet de creer et de gerer les differentes commandes du programme
    """
    def __init__(self, root, pad, font):
        self.root = root    #fenetre principale
        self.pad = pad      #widget de texte
        self.font = font    #police et formatage du texte

        self.bold = False
        self.italic = False
        self.underline = False
        self.fontSize = 12

    def menuAbout(self):
        #cree une fenetre d'information
        messagebox.showinfo(title="À propos", message="Projet de bloc note \nUE POO \nPar Clément Malonda \nDécembre 2020")

    def menuNew(self, event=None):
        #vide la zone de texte et vide la path du fichier ouvert
        global filepath
        self.pad.delete(1.0, END)
        filepath = None

    def menuOpen(self, event=None):
        #ouvre une fenetre de dialogue puis le fichier selectionne
        global filepath
        filepath = filedialog.askopenfilename(filetypes=[('text files','.txt'),('all files','.*')])
        if filepath != '': # filepath == '' si on clique sur annuler
            file = open(filepath, 'r')
            text = file.read()
            self.pad.delete(1.0, END)
            self.pad.insert(INSERT, text)
            file.close()

    def menuSave(self, event=None):
        #gestion de l'enregistrement du fichier avec ouverture de la boite de dialogue d'enregistrer si le fichier ne l'a jamais ete
        global filepath
        if filepath == None:
            self.menuSaveAs()
        else:
            file = open(filepath, 'w')
            text = self.pad.get(1.0, END)
            file.write(text)
            file.close()

    def menuSaveAs(self, event=None):
        #ouverture de la fenetre de dialogue d'enregistrement
        global filepath
        newFilepath = filedialog.asksaveasfilename(initialdir=os.getcwd(), initialfile="new_file", filetypes=[('text files','.txt'), ('all files','.*')], defaultextension=".txt")
        if newFilepath != '': #gestion du cas d'annulation de l'enresitrement
            file = open(newFilepath, 'w')
            text = self.pad.get(1.0, END)
            file.write(text)
            file.close()
            filepath = newFilepath

    def menuCopy(self, event=None):
        #copie de la selection dans le presse paper
        self.root.clipboard_clear()
        s = self.pad.get("sel.first", "sel.last") #.selection_get()
        self.root.clipboard_append(s)

    def menuCut(self, event=None):
        #similaire a menuCopy mais avec suppression du texte copie
        self.root.clipboard_clear()
        s = self.pad.get("sel.first", "sel.last")
        self.pad.delete("sel.first", "sel.last")
        self.root.clipboard_append(s)

    def menuPast(self, event=None):
        #insertion du contenu du presse paper au niveau du curseur
        s = self.root.clipboard_get()
        self.pad.insert(INSERT, s)

    def menuBold(self, event=None):
        if self.bold:
            self.bold = False
            self.font.configure(weight="normal")
        else:
            self.bold = True
            self.font.configure(weight="bold")
        self.pad.configure(font=self.font)

    def menuItalic(self, event=None):
        if self.italic:
            self.italic = False
            self.font.configure(slant="roman")
        else:
            self.italic = True
            self.font.configure(slant="italic")
        self.pad.configure(font=self.font)

    def menuUnderline(self, event=None):
        if self.underline:
            self.underline = False
        else:
            self.underline = True
        self.font.configure(underline=self.underline)
        self.pad.configure(font=self.font)

    def menuChangeFont(self, newFont):
        self.font.configure(family=newFont)
        self.pad.configure(font=self.font)

    def menuChangeSize(self, newSize):
        if newSize == 0:
            self.fontSize = 12
        else:
            self.fontSize = self.fontSize + newSize
        self.font.configure(size=self.fontSize)
        self.pad.configure(font=self.font)

class MyMenu():
    """ Classe MyMenu
        Cette classe permet de créer de gérer le menu de notre application avec les différentes menu et sous-menu.
        Fichier :
        Edition :
        Outils :
        Aide :

    """
    def __init__(self, root, command):
        self.root = root
        self.command = command
        self.menuBar = Menu(self.root)
        self.fontList = ["Arial", "Calibri", "Cambria", "Modern", "Roman", "Time New Roman", "Comic Sans MS"]

    def creatMenu(self):
        menuFichier = Menu(self.menuBar, tearoff=0) # creation du menu Fichier
        menuFichier.add_command(label="Nouveau", accelerator=keyName+"+N", command=self.command.menuNew, underline=1) #le parametre accelerator permet de définir le raccourci clavier
        menuFichier.add_command(label="Ouvrir...", accelerator=keyName+"+O", command=self.command.menuOpen, underline=1)
        menuFichier.add_command(label="Enregistrer", accelerator=keyName+"+S", command=self.command.menuSave)
        menuFichier.add_command(label="Enregistrer sous...", accelerator=keyName+"+Shift+S", command=self.command.menuSaveAs)
        menuFichier.add_separator() #ajout d'un séparateur
        menuFichier.add_command(label="Quitter", command=self.root.quit, underline=1) #modifier la commande de QUitter pour proposer de sauvegarder
        self.menuBar.add_cascade(label="Fichier", menu=menuFichier) # ajout du menu fichier et de ses commandes a la bar de menu

        menuEdition = Menu(self.menuBar, tearoff=0)
        menuEdition.add_command(label="Annuler")
        menuEdition.add_command(label="Rétablir")
        menuEdition.add_separator()
        menuEdition.add_command(label="Couper", accelerator=keyName+"+X", command=self.command.menuCut)
        menuEdition.add_command(label="Copier", accelerator=keyName+"+C", command=self.command.menuCopy)
        menuEdition.add_command(label="Coller", accelerator=keyName+"+V", command=self.command.menuPast)
        self.menuBar.add_cascade(label="Edition", menu=menuEdition)

        menuOutils = Menu(self.menuBar, tearoff=0)
        menuOutils.add_command(label="Gras", accelerator=keyName+"+B", command=self.command.menuBold)
        menuOutils.add_command(label="Italique", accelerator=keyName+"+I", command=self.command.menuItalic)
        menuOutils.add_command(label="Souligné", accelerator=keyName+"+U", command=self.command.menuUnderline)
        menuOutils.add_separator()
        subMenuFont = Menu(self.menuBar, tearoff=0)
        for fontFamily in self.fontList: #list(tkFont.families()):
            subMenuFont.add_command(label=fontFamily, command=partial(self.command.menuChangeFont, fontFamily))
        menuOutils.add_cascade(label="Polices", menu=subMenuFont)
        menuOutils.add_separator()
        menuOutils.add_command(label="Taille du texte...", state="disable")
        menuOutils.add_command(label="Augmenter", command=partial(self.command.menuChangeSize, 1))
        menuOutils.add_command(label="Diminuer", command=partial(self.command.menuChangeSize, -1))
        menuOutils.add_command(label="Taille par défaut", command=partial(self.command.menuChangeSize, 0))
        self.menuBar.add_cascade(label="Outils", menu=menuOutils)

        menuAide = Menu(self.menuBar, tearoff=0)
        menuAide.add_command(label="À propos", command=self.command.menuAbout)
        self.menuBar.add_cascade(label="Aide", menu=menuAide)

        self.root.config(menu=self.menuBar) #ajout du menu dans le fenetre principale

    def addShortcuts(self):
        self.root.bind_all("<"+keyName+"-n>", self.command.menuNew)
        self.root.bind_all("<"+keyName+"-o>", self.command.menuOpen)
        self.root.bind_all("<"+keyName+"-s>", self.command.menuSave)
        self.root.bind_all("<"+keyName+"-Shift-s>", self.command.menuSaveAs)

        self.root.bind_all("<"+keyName+"-c>", self.command.menuCopy)
        self.root.bind_all("<"+keyName+"-x>", self.command.menuCut)
        self.root.bind_all("<"+keyName+"-v>", self.command.menuPast)

        self.root.bind_all("<"+keyName+"-b>", self.command.menuBold)
        self.root.bind_all("<"+keyName+"-i>", self.command.menuItalic)
        self.root.bind_all("<"+keyName+"-u>", self.command.menuUnderline)

class MyNotePad(Frame):
    """ Classe principale
        La classe MyNotePad et la classe principale de notre programme, elle représente l'application elle même.
        Pour cela elle doit être une classe fille de la classe Frame de tkinter
    """
    def __init__(self):
        self.root = Tk()
        self.pad = Text(self.root, height=200, width=100, wrap='word')
        self.font = tkFont.Font(size=12)
        self.pad.configure(font=self.font)
        self.command = MyCommand(self.root, self.pad, self.font)
        self.menu = MyMenu(self.root, self.command)

        self.configRoot()

        self.root.mainloop()

    def configRoot(self):
        self.root.geometry("700x500+60+60")
        self.root.minsize(450, 300)
        self.root.title("MyNotePad")
        ico = Image.open("img/icone.png")
        ico = ImageTk.PhotoImage(ico)
        self.root.wm_iconphoto(False, ico)

        self.pad.pack()
        self.menu.creatMenu()
        self.menu.addShortcuts()

def main():
    app = MyNotePad()

if __name__ == "__main__":
    main()
