__author__ = 'Mickael Amorim'
###############################################
# Partie Client chargé de générer et envoyer  #
# les informations d'authentifications        #
################# Version Beta ################


import socket,sys
import os
import hashlib
import interfaces
import variableglobale
import util
from time import gmtime, strftime

donnee=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
login=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","-",".","_","@"]


def hash_str(chaine) :
    chaine=chaine.encode()
    chaine = hashlib.sha1(chaine).hexdigest()
    return chaine

def affichage_tab(tabcombi):
    aff_final = []
    for string in tabcombi:
        if not "string2" in string :
            aff_final.append(string)

    retourner=("".join(aff_final))
    pass_hash = hash_str(retourner)
    return pass_hash

def brute_force(n,i, tabcombi, donnee, IP, port, choix, chaine):
    result = []

    if i >= n:
        result=affichage_tab(tabcombi)
        # Processus d'envoi du mot de passe généré
        if choix == "2" :
            login = chaine
            z=process_create_client(IP , port, login, result, choix)
        if choix == "3" :
            password = chaine
            z=process_create_client(IP , port, result, password, choix)

        if z == 1 :
            return 1
    else :
        l=0
        while l < len(donnee) :
            tabcombi[i] = donnee[l]
            w=brute_force(n,i+1,tabcombi, donnee, IP, port, choix, chaine)
            if w== 1 :
                return 1
            l+=1

def process_create_client(IP , port, login, password, choix):
    temoin = 0
    # On crée le socket
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
    # connexion du client vers le serveur
        sock.connect((IP,port))
    except socket.error:
        util.tolog("Probleme de connexion avec le serveur","EMERG")
        util.tolog("Reiterer ulterieurement","EMERG")
        sys.exit()

    #print(">>> Connexion établie avec le serveur.")
    # Envoi du message
    #print(">>> Envoi vers le serveur")

    sock.send(password.encode())
    sock.send(login.encode())
    util.tologbrute("Attente d'une reponse du serveur ...","NOTICE")
    util.tolog("Attente d'une reponse du serveur ...","NOTICE")

    try :
        msgServer=sock.recv(1024)
        date = strftime("[%H:%M:%S]", gmtime())
        print(">>> "+ date +" ", msgServer.decode())

        confirmch="b'Client authentifie'"

        if str(msgServer) == confirmch :

            variableglobale.LOG = 1
            if choix == "2" or choix == "3" :
                print(">>> Mot de passe trouvé : "+password)
                return 1
                sock.close()

    except ConnectionResetError :
        util.tologbrute("l IP a ete bannie","WARNING")
        sock.close

    sock.close()


def choice_authentification_simple(HOST,PORT, choix):
        print("login :")
        log=input()
        print("mot de passe :")
        passe = input()
        passe=hash_str(passe)
        z=process_create_client(HOST , PORT, log, passe, 0)

def choice_brute_mdp(HOST, PORT, choix) :
        print("Taille du mot de passe :")
        taille=int(input())                                            # cast en int de l'information récupérée
        print("Login à brute forcer :")
        ident=input()
        tabcombi=[" "]*taille                                           # On définit le tableau de la taille du mot de passe
        brute_force(taille, 0, tabcombi, donnee, HOST, PORT, choix, ident)     # appel de la fonction brute force

def choice_brute_log(HOST, PORT, choix) :
        print("Taille du login :")
        sizelog=int(input())
        tabcombi=[" "]*sizelog
        print("Mot de passe à brute forcer :")
        mdp_brute=input()
        brute_force(sizelog,0,tabcombi,login, HOST, PORT, choix, mdp_brute )


############################################## /////// MAIN \\\\\\\ ##################################################
#os.system("C:\Users\Mickael\PycharmProjects\PROJECT PYTHON\Server-authentification")
interfaces.Welcome()
input()
clear = lambda: os.system('cls')
clear()

while (variableglobale.QUIT ==0) :

    if variableglobale.LOG == 0 :
        interfaces.windows_user()

    if variableglobale.LOG == 1 :
        interfaces.windows_admin()

    choix=input()
    clear = lambda: os.system('cls')
    clear()

    if choix == "1" :                                                                     # Authentification simple
        choice_authentification_simple(variableglobale.HOST, variableglobale.PORT, choix)

    if choix == "2" and variableglobale.LOG == 1 :                                        # Choix Brute par mot de passe
        choice_brute_mdp(variableglobale.HOST, variableglobale.PORT, choix)

    if choix == "3" and variableglobale.LOG == 1 :                                        # Choix Brute par login
        choice_brute_log(variableglobale.HOST, variableglobale.PORT, choix)

    if choix == "4" and variableglobale.LOG == 1 :                                        # Accès au FTP
        print("FTP")

    if choix == "5" and variableglobale.LOG == 1 :
        print("")

    if choix == "6" and variableglobale.LOG == 1 :                                       # Deconnexion
        variableglobale.LOG = 0

    if choix == "q" :
        variableglobale.QUIT = 1
