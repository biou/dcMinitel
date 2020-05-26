#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from minitel.Minitel import Minitel
from minitel.ImageMinitel import ImageMinitel
from PIL import Image
from time import sleep
from minitel.ui.ChampTexte import ChampTexte
from minitel.ui.Conteneur import Conteneur
from minitel.ui.Label import Label
from minitel.ui.Menu import Menu
from minitel.constantes import ENVOI
import xmlrpc.client
import os

server_url = os.environ['SERVER_URL']
client = xmlrpc.client.ServerProxy(server_url)

class LoginForm:
    def __init__(self, login = '', password = ''):
        self.login = login
        self.password = password

    def updateLogin(self, newLogin):
        self.login = newLogin

    def updatePassword(self, newPassword):
        self.password = newPassword

    def __str__(self):
        return self.login+':'+self.password


class PostForm:
    def __init__(self, title = '', extract = '', content1 = '', content2 = '', content3 = '', content4 = '', content5 = ''):
        self.title = title
        self.extract = extract
        self.content1 = content1
        self.content2 = content2
        self.content3 = content3
        self.content4 = content4
        self.content5 = content5

    def updateTitle(self, newTitle):
        self.title = newTitle

    def updateExtract(self, newExtract):
        self.extract = newExtract

    def updateContent1(self, newContent1):
        self.content1 = newContent1

    def updateContent2(self, newContent2):
        self.content2 = newContent2

    def updateContent3(self, newContent3):
        self.content3 = newContent3

    def updateContent4(self, newContent4):
        self.content4 = newContent4

    def updateContent5(self, newContent5):
        self.content5 = newContent5

    def content(self):
        return self.content1+' '+self.content2+' '+self.content3+' '+self.content4+' '+self.content5

    def __str__(self):
        return self.title+'|'+self.extract+'|'+self.content1+'|'+self.content2+'|'+self.content3+'|'+self.content4+'|'+self.content5
    

class DCInput(ChampTexte):
    def __init__(self, minitel, posx, posy, longueur_visible, longueur_totale = None, valeur = '', couleur = None, champ_cache = False, envoi_callback = None, update_callback = None):
        self.envoi_callback = envoi_callback
        self.update_callback = update_callback
        super().__init__(minitel, posx, posy, longueur_visible, longueur_totale, valeur, couleur, champ_cache)

    def gere_touche(self, sequence):
        if (sequence.egale(ENVOI)):
            if (self.envoi_callback != None):
                self.envoi_callback()
            return True
        super().gere_touche(sequence)
        if (self.update_callback != None):
            self.update_callback(self.valeur)

def bouton_envoi():
    minitel.position(30,23)
    minitel.effet(False,True,True)
    minitel.taille(2,2)
    minitel.envoyer('Envoi')
    minitel.taille(1,1)
    minitel.effet(False,False,False)

login_form = LoginForm()
post_form = PostForm()

def ecran_login():
    minitel.efface()

    image = Image.open('Dotclear-logo.png')
    image = image.resize((80,36), Image.ANTIALIAS)
    image_minitel = ImageMinitel(minitel)
    image_minitel.importer(image)
    image_minitel.envoyer(1,1)

    bouton_envoi()

    conteneur = Conteneur(minitel, 1, 13, 40, 4, 'blanc', 'noir')

    labelLogin = Label(minitel, 1, 15, "Nom d'utilisatrice ou d'utilisateur", 'rouge')
    champLogin = DCInput(minitel, 1, 16, 40, 60, envoi_callback = validate_login, update_callback = login_form.updateLogin)

    labelPass = Label(minitel, 1, 18, "Mot de passe", 'rouge')
    champPass = DCInput(minitel, 1, 19, 40, 60, champ_cache=True, envoi_callback = validate_login, update_callback = login_form.updatePassword)


    conteneur.ajoute(labelLogin)
    conteneur.ajoute(champLogin)
    conteneur.ajoute(labelPass)
    conteneur.ajoute(champPass)
    conteneur.affiche()

    conteneur.executer()


def validate_login():
    print('validate login')
    try:
        client.blogger.getUserInfo('', login_form.login, login_form.password)
        print('login successful')
        ecran_write()
    except xmlrpc.client.Fault:
        print('error login')

def validate_write():
    print('validate write')
    try:
        client.metaWeblog.newPost('', login_form.login, login_form.password, {"title": post_form.title, "mt_excerpt": post_form.extract, "description": post_form.content()}, True)
        ecran_success()
    except xmlrpc.client.Fault:
        print('error newPost')

def ecran_write():
    minitel.efface()
    

    minitel.position(1,1)
    minitel.effet(False,False, True)
    minitel.envoyer('Dotclear: nouveau billet')
    minitel.effet(False, False, False)
    
    conteneur = Conteneur(minitel, 1, 3, 40, 4, 'blanc', 'noir')
    labelTitre = Label(minitel, 1, 3, "Titre", 'rouge')
    champTitre = DCInput(minitel, 1, 4, 40, 60, envoi_callback = validate_write, update_callback = post_form.updateTitle)

    labelChapo = Label(minitel, 1, 6, 'Extrait', 'rouge')
    champChapo = DCInput(minitel, 1, 7, 40, 60, envoi_callback = validate_write, update_callback = post_form.updateExtract)

    labelContent = Label(minitel, 1, 9, 'Contenu', 'rouge')
    champContent1 = DCInput(minitel, 1, 10, 40, 40, envoi_callback = validate_write, update_callback = post_form.updateContent1)
    champContent2 = DCInput(minitel, 1, 11, 40, 40, envoi_callback = validate_write, update_callback = post_form.updateContent2)
    champContent3 = DCInput(minitel, 1, 12, 40, 40, envoi_callback = validate_write, update_callback = post_form.updateContent3)
    champContent4 = DCInput(minitel, 1, 13, 40, 40, envoi_callback = validate_write, update_callback = post_form.updateContent4)
    champContent5 = DCInput(minitel, 1, 14, 40, 40, envoi_callback = validate_write, update_callback = post_form.updateContent5)

    conteneur.ajoute(labelTitre)
    conteneur.ajoute(champTitre)
    conteneur.ajoute(labelChapo)
    conteneur.ajoute(champChapo)
    conteneur.ajoute(labelContent)
    conteneur.ajoute(champContent1)
    conteneur.ajoute(champContent2)
    conteneur.ajoute(champContent3)
    conteneur.ajoute(champContent4)
    conteneur.ajoute(champContent5)

    conteneur.affiche()
    
    bouton_envoi()
    conteneur.executer()

def ecran_success():
    minitel.efface()

    minitel.position(4, 10)
    minitel.taille(2,2)
    minitel.effet(False, False, True)
    minitel.envoyer('Billet publié !')
    minitel.taille(1,1)
    minitel.effet(False, False, False)


minitel = Minitel()

minitel.deviner_vitesse()
minitel.identifier()
minitel.definir_vitesse(4800)
minitel.definir_mode('VIDEOTEX')
minitel.configurer_clavier(etendu = True, curseur = False, minuscule = True)
minitel.echo(False)
minitel.curseur(False)

ecran_login()
minitel.close()
