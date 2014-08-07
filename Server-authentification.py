__author__ = 'Mickael Amorim'

import socket
import select
import variableglobale
from time import gmtime, strftime
from util import tologbrute


def verify_authenticity(credential_login, credential_mdp):
    authenticity=0
    for cle in variableglobale.dictionnaire :
        if cle == credential_login :
            if variableglobale.dictionnaire[cle] == credential_mdp :
                authenticity=1

    return authenticity

######################################### ///////// MAIN \\\\\\\\\ #############################################

# création d'un socket
ServerSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) # famille et mode

# liaison du scoket à une adresse IP et un port
ServerSocket.bind((variableglobale.HOST_SRV, variableglobale.PORT_SRV))
ServerSocket.listen(10)

print("Le serveur écoute à présent sur le port :", variableglobale.PORT_SRV)
print(">>> Serveur pret, en attente d'un client...")
# liste de clients suceptibles de solliciter le serveur
clients_connectes = []
heure_connect= []
bann_list= []

while 1 :

    # On va vérifier les nouveaux clients qui se connectent
    # Pour cela, on écoute la connexion_principale en lecture
    # On attend maximum 50ms
    connexions_demandees, wlist, xlist = select.select([ServerSocket],
        [], [], 0.06)  # 60 ms de time out

    for connexion in connexions_demandees:  #les clients  de rlist
        connexion_avec_client, infos_connexion = connexion.accept()


        # On ajoute le socket connecté à la liste des clients
        clients_connectes.append(connexion_avec_client)

    # On écoute la liste des clients connectés
    # Les clients renvoyés par select sont ceux devant être lus (recv)
    # On attend là  50ms maximum
    # On encadre l'appel à select.select dans un bloc try
    # En effet, si la liste de clients connectés est vide, une exception
    # Peut être levée

    clients_a_lire = []
    try:
        clients_a_lire, wlist, xlist = select.select(clients_connectes,[], [], 0.05)
    except select.error:
        pass

    #on continue en séquence
    else:
           # On parcourt la liste des clients à lire
        for client in clients_a_lire:

            for j in bann_list :
                if j == infos_connexion[0] :
                    tologbrute("tentative de connexion d'une IP bannie :"+infos_connexion[0],"EMERG")
                    client.close()

            try :
                # Client est de type socket
                # réception de message du client
                ReceivClient_mdp=client.recv(variableglobale.TAILLE_BUFFER_MDP)  # réception de caractères
                ReceivClient_login=client.recv(variableglobale.TAILLE_BUFFER_LOGIN)

                AUTH = verify_authenticity(credential_login = ReceivClient_login.decode(), credential_mdp = ReceivClient_mdp.decode())

                if AUTH == 1 :
                    msgServer="Client authentifie"
                    client.send(msgServer.encode())

                elif AUTH == 0 :
                    client.send(b"Authentification incorrecte")
                    print("bad")
                    date = strftime("%H:%M:%S", gmtime())
                    heure_connect.append(date)

            except :
                client.close()
                clients_connectes.remove(client)


        compt =0
        tmp=""
    for i in heure_connect :
        if i == tmp :
            compt = compt+1
            print(compt)
            if compt == 7 :
                flag=0
                for l in range(1,len(bann_list)) :
                    if bann_list[l]==infos_connexion[0] :
                        flag=1

                if flag == 0 :
                    bann_list.append(infos_connexion[0])
                    print(heure_connect)
                    clients_connectes.remove(client)
                    client.close()
        tmp=i




print("Fermeture des connexions par l'un des clients ")

ServerSocket.close()
