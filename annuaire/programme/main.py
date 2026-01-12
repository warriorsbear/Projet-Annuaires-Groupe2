import sys
import os
from pathlib import Path
import hashlib
data_dir = Path(__file__).parent.parent / "data"
import csv
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Class import Client, Administrateur  # type: ignore

def creer_serveur():
    print("serveur créé, choisir une action :")
    print("1. Se connecter")
    print("2. Quitter")
    choix = input("Choisir une action : ")
    if choix == "1":
        connecter_serveur()
    elif choix == "2":
        print("Quitter")
        exit()
    else:
        print("Choix invalide")
        creer_serveur()
    

def connecter_serveur():
    identifiant = input("Identifiant : ")
    mot_de_passe = input("Mot de passe : ")
    mot_de_passe = hashlib.sha256(mot_de_passe.encode()).hexdigest()
    with open(data_dir / "clients.csv", "r", newline="") as f:
                            lst = []
                            for ligne in f:
                                lst.append([ligne.split(",")[1],ligne.split(",")[2]])
                            lst.remove(lst[0])
                            c = 0
                            for k in range(len(lst)):
                                if identifiant == lst[k][0] and mot_de_passe == lst[k][1]:
                                    print("Connexion réussie")
                                    c = 1
                                    break

                            if c == 0:
                                print("Connexion échouée")
                            f.close()
    print("--------------------------------")
    print("Choisir une action :")
    print("1. visualiser l'annuaire")
    print("2. ajouter un contact")
    print("3. supprimer un contact")
    print("4. modifier un contact")
    print("5. rechercher un contact")
    print("6. lister les contacts")
    print("7. accorder une permission")
    print("8. retirer une permission")
    print("9. exporter l'annuaire")
    print("10. quitter")
    choix = input("Choisir une action : ")
    if choix == "1":
        ##visualiser_annuaire()
        print("Action non implémentée")
    elif choix == "2":
        #ajouter_contact()
        print("Action non implémentée")
    elif choix == "3":
        #supprimer_contact()
        print("Action non implémentée")
    elif choix == "4":
        #modifier_contact()
        print("Action non implémentée")
    elif choix == "5":
        #rechercher_contact()
        print("Action non implémentée")
    elif choix == "6":
        #lister_contacts()
        print("Action non implémentée")
    elif choix == "7":
        #accorder_permission()
        print("Action non implémentée")
    elif choix == "8":
        #retirer_permission()
        print("Action non implémentée")
    elif choix == "9":
        #exporter_annuaire()
        print("Action non implémentée")
    elif choix == "10":
        print("Quitter")
        exit()
    else:
        print("Choix invalide")
        connecter_serveur()


def deconnecter_serveur():
    pass

def envoyer_pdu():
    pass

def recevoir_pdu():
    pass




def main() -> None:
    creer_serveur()













if __name__ == "__main__":
    main()