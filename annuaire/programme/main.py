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
    email = input("Email : ")
    mot_de_passe = input("Mot de passe : ")
    
    mot_de_passe_hash = hashlib.sha256(mot_de_passe.encode()).hexdigest()
    client_connecte = None
    
    # Lecture du fichier clients.csv et recherche du client
    with open(data_dir / "clients.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["email"] == email and row["hash_mdp"] == mot_de_passe_hash:
                # Création de l'objet Client avec la classe associée
                client_connecte = Client(row["email"], row["hash_mdp"])
                
                # Restauration des informations du client depuis le CSV
                # L'identifiant peut être dans le CSV ou généré automatiquement
                if row.get("id_client"):
                    # Si on a un UUID dans id_client, on l'utilise
                    try:
                        client_connecte.identifiant = row["id_client"]
                    except:
                        pass  # Garde l'UUID généré automatiquement
                
                # Restauration du chemin d'annuaire (conversion en chemin absolu si nécessaire)
                if row.get("chemin_annuaire"):
                    chemin = row["chemin_annuaire"]
                    # Si le chemin est relatif, le convertir en chemin absolu depuis le répertoire data
                    if not os.path.isabs(chemin):
                        chemin = str(data_dir / Path(chemin).name)
                    client_connecte.chemin_annuaire = chemin
                
                # Restauration des permissions (si présentes dans le CSV)
                # Les permissions peuvent être stockées comme des listes JSON ou séparées par des virgules
                if row.get("liste_permissions_accordees"):
                    perms_accordees = row["liste_permissions_accordees"].strip()
                    if perms_accordees and perms_accordees != "[]":
                        try:
                            import json
                            client_connecte.permissions_accordees = json.loads(perms_accordees)
                        except:
                            # Si ce n'est pas du JSON, essayer de parser comme une liste simple
                            perms_accordees = perms_accordees.strip("[]").replace("'", "").replace('"', "")
                            if perms_accordees:
                                client_connecte.permissions_accordees = [p.strip() for p in perms_accordees.split(",") if p.strip()]
                
                if row.get("liste_permissions_recues"):
                    perms_recues = row["liste_permissions_recues"].strip()
                    if perms_recues and perms_recues != "[]":
                        try:
                            import json
                            client_connecte.permissions_recues = json.loads(perms_recues)
                        except:
                            perms_recues = perms_recues.strip("[]").replace("'", "").replace('"', "")
                            if perms_recues:
                                client_connecte.permissions_recues = [p.strip() for p in perms_recues.split(",") if p.strip()]
                
                print("Connexion réussie")
                break
    
    if client_connecte is None:
        print("Connexion échouée")
        return
    
    # Utilisation du client connecté pour les opérations
    menu_actions(client_connecte)


def menu_actions(client: Client):
    """
    Affiche le menu d'actions et gère les interactions avec le client connecté.
    
    Args:
        client: Instance du Client connecté
    """
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
    print("10. Se déconnecter")
    choix = input("Choisir une action : ")
    if choix == "1":
        visualiser_annuaire(client)
    elif choix == "2":
        ajouter_contact(client)
    elif choix == "3":
        supprimer_contact(client)
    elif choix == "4":
        modifier_contact(client)
    elif choix == "5":
        rechercher_contact(client)
    elif choix == "6":
        lister_contacts(client)
    elif choix == "7":
        accorder_permission(client)
    elif choix == "8":
        retirer_permission(client)
    elif choix == "9":
        exporter_annuaire(client)
    elif choix == "10":
        deconnecter_serveur()
        exit()
    else:
        print("Choix invalide")
        menu_actions(client)


def visualiser_annuaire(client: Client):
    """Visualise l'annuaire du client."""
    contacts = client.lister_contacts()
    if not contacts:
        print("Aucun contact dans l'annuaire.")
    else:
        print(f"\nAnnuaire de {client.mail} ({len(contacts)} contact(s)):")
        for contact in contacts:
            print(f"  - ID: {contact.get('id_contact')}, {contact.get('prenom')} {contact.get('nom')}, Email: {contact.get('email')}")
    print()
    menu_actions(client)


def ajouter_contact(client: Client):
    """Ajoute un contact à l'annuaire."""
    print("Ajout d'un contact :")
    id_contact = int(input("ID du contact : "))
    nom = input("Nom : ")
    prenom = input("Prénom : ")
    email = input("Email : ")
    telephone = input("Téléphone : ")
    adresse = input("Adresse : ")
    
    contact = {
        'id_contact': id_contact,
        'nom': nom,
        'prenom': prenom,
        'email': email,
        'telephone': telephone,
        'adresse': adresse
    }
    try:
        client.ajouter_contact(contact)
        print("Contact ajouté avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'ajout du contact : {e}")
    print()
    menu_actions(client)


def supprimer_contact(client: Client):
    """Supprime un contact de l'annuaire."""
    id_contact = int(input("ID du contact à supprimer : "))
    try:
        client.supprimer_contact(id_contact)
        print("Contact supprimé avec succès.")
    except Exception as e:
        print(f"Erreur lors de la suppression : {e}")
    print()
    menu_actions(client)


def modifier_contact(client: Client):
    """Modifie un contact de l'annuaire."""
    id_contact = int(input("ID du contact à modifier : "))
    print("Entrez les nouveaux champs (laisser vide pour ne pas modifier) :")
    champs = {}
    nom = input("Nom : ")
    if nom:
        champs['nom'] = nom
    prenom = input("Prénom : ")
    if prenom:
        champs['prenom'] = prenom
    email = input("Email : ")
    if email:
        champs['email'] = email
    telephone = input("Téléphone : ")
    if telephone:
        champs['telephone'] = telephone
    adresse = input("Adresse : ")
    if adresse:
        champs['adresse'] = adresse
    
    try:
        client.modifier_contact(id_contact, champs)
        print("Contact modifié avec succès.")
    except Exception as e:
        print(f"Erreur lors de la modification : {e}")
    print()
    menu_actions(client)


def rechercher_contact(client: Client):
    """Recherche des contacts dans l'annuaire."""
    print("Critères de recherche (laisser vide pour ignorer) :")
    criteres = {}
    nom = input("Nom : ")
    if nom:
        criteres['nom'] = nom
    prenom = input("Prénom : ")
    if prenom:
        criteres['prenom'] = prenom
    email = input("Email : ")
    if email:
        criteres['email'] = email
    
    try:
        resultats = client.rechercher_contact(criteres)
        if not resultats:
            print("Aucun contact trouvé.")
        else:
            print(f"\n{len(resultats)} contact(s) trouvé(s) :")
            for contact in resultats:
                print(f"  - ID: {contact.get('id_contact')}, {contact.get('prenom')} {contact.get('nom')}, Email: {contact.get('email')}")
    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")
    print()
    menu_actions(client)


def lister_contacts(client: Client):
    """Liste tous les contacts de l'annuaire."""
    visualiser_annuaire(client)


def accorder_permission(client: Client):
    """Accorde une permission à un autre utilisateur."""
    email_utilisateur = input("Email de l'utilisateur à qui accorder la permission : ")
    try:
        client.accorder_permission(email_utilisateur)
        print(f"Permission accordée à {email_utilisateur}.")
    except Exception as e:
        print(f"Erreur : {e}")
    print()
    menu_actions(client)


def retirer_permission(client: Client):
    """Retire une permission à un autre utilisateur."""
    email_utilisateur = input("Email de l'utilisateur à qui retirer la permission : ")
    try:
        client.retirer_permission(email_utilisateur)
        print(f"Permission retirée à {email_utilisateur}.")
    except Exception as e:
        print(f"Erreur : {e}")
    print()
    menu_actions(client)


def exporter_annuaire(client: Client):
    """Exporte l'annuaire au format CSV."""
    try:
        chemin = client.exporter_csv()
        print(f"Annuaire exporté vers : {chemin}")
    except Exception as e:
        print(f"Erreur lors de l'export : {e}")
    print()
    menu_actions(client)


def deconnecter_serveur():
    """Déconnecte le client."""
    print("Déconnexion réussie.")

def envoyer_pdu():
    pass

def recevoir_pdu():
    pass




def main() -> None:
    creer_serveur()













if __name__ == "__main__":
    main()