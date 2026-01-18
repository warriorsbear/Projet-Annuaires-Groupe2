import sys
import os
from pathlib import Path
import hashlib
import uuid
import json
import getpass
data_dir = Path(__file__).parent.parent / "data"
import csv
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Class import Client, Administrateur # type: ignore

ADMIN_EMAIL = "admin@admin.fr"
ADMIN_PASSWORD = "adminadmin"

def verifier_creer_admin():
    """
    Vérifie si l'admin existe dans clients.csv, sinon le crée.
    """
    clients_csv_path = data_dir / "clients.csv"
    
    # Vérifier si le fichier existe
    admin_existe = False
    if clients_csv_path.exists():
        # Lire le fichier pour vérifier si l'admin existe
        try:
            with open(clients_csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("email") == ADMIN_EMAIL:
                        admin_existe = True
                        break
        except Exception:
            # Si erreur de lecture, on considère que l'admin n'existe pas
            admin_existe = False
    
    # Si l'admin n'existe pas, le créer
    if not admin_existe:
        # Génération du hash du mot de passe
        hash_mdp = hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest()
        
        # Génération d'un identifiant unique pour l'admin
        identifiant = str(uuid.uuid4())
        
        # Chemin d'annuaire pour l'admin
        chemin_annuaire = f"data/{identifiant}.csv"
        chemin_annuaire_absolu = data_dir / f"{identifiant}.csv"
        
        # Préparer la ligne à ajouter
        nouvelle_ligne = {
            "id_client": identifiant,
            "email": ADMIN_EMAIL,
            "hash_mdp": hash_mdp,
            "chemin_annuaire": chemin_annuaire,
            "liste_permissions_accordees": "[]",
            "liste_permissions_recues": "[]"
        }
        
        # Écrire dans le fichier CSV
        file_exists = clients_csv_path.exists()
        
        # S'assurer qu'il y a un saut de ligne à la fin du fichier avant d'ajouter
        if file_exists:
            # Lire les dernières lignes pour vérifier le format
            with open(clients_csv_path, "rb") as f:
                try:
                    f.seek(-1, 2)  # Aller à la dernière position
                    dernier_caractere = f.read(1)
                    if dernier_caractere != b"\n":
                        # Ajouter un saut de ligne si nécessaire
                        with open(clients_csv_path, "ab") as f_append:
                            f_append.write(b"\n")
                except (IOError, OSError):
                    # Si le fichier est vide ou erreur, on continue
                    pass
        
        with open(clients_csv_path, "a", encoding="utf-8", newline="") as f:
            fieldnames = ["id_client", "email", "hash_mdp", "chemin_annuaire", 
                         "liste_permissions_accordees", "liste_permissions_recues"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # Écrire l'en-tête si le fichier est nouveau
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(nouvelle_ligne)
        
        # Créer le fichier CSV d'annuaire associé (vide avec juste l'en-tête)
        with open(chemin_annuaire_absolu, "w", encoding="utf-8", newline="") as f:
            fieldnames_annuaire = ["id_contact", "nom", "prenom", "email", "telephone", "adresse"]
            writer = csv.DictWriter(f, fieldnames=fieldnames_annuaire)
            writer.writeheader()
        
        print(f"Administrateur créé : {ADMIN_EMAIL}")

def creer_serveur():
    # Vérifier et créer l'admin si nécessaire
    verifier_creer_admin()
    
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
    mot_de_passe = getpass.getpass("Mot de passe : ")
    
    mot_de_passe_hash = hashlib.sha256(mot_de_passe.encode()).hexdigest()
    utilisateur_connecte = None
    est_admin = email == ADMIN_EMAIL
    
    # Lecture du fichier clients.csv et recherche du client/admin
    with open(data_dir / "clients.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["email"] == email and row["hash_mdp"] == mot_de_passe_hash:
                # Création de l'objet Administrateur ou Client selon l'email
                if est_admin:
                    utilisateur_connecte = Administrateur(row["email"], row["hash_mdp"])
                else:
                    utilisateur_connecte = Client(row["email"], row["hash_mdp"])
                
                # Restauration des informations depuis le CSV
                if row.get("id_client"):
                    try:
                        utilisateur_connecte.identifiant = row["id_client"]
                    except:
                        pass
                
                # Restauration du chemin d'annuaire
                if row.get("chemin_annuaire"):
                    chemin = row["chemin_annuaire"]
                    if not os.path.isabs(chemin):
                        chemin = str(data_dir / Path(chemin).name)
                    utilisateur_connecte.chemin_annuaire = chemin
                
                # Restauration des permissions
                if row.get("liste_permissions_accordees"):
                    perms_accordees = row["liste_permissions_accordees"].strip()
                    if perms_accordees and perms_accordees != "[]":
                        try:
                            utilisateur_connecte.permissions_accordees = json.loads(perms_accordees)
                        except:
                            perms_accordees = perms_accordees.strip("[]").replace("'", "").replace('"', "")
                            if perms_accordees:
                                utilisateur_connecte.permissions_accordees = [p.strip() for p in perms_accordees.split(",") if p.strip()]
                
                if row.get("liste_permissions_recues"):
                    perms_recues = row["liste_permissions_recues"].strip()
                    if perms_recues and perms_recues != "[]":
                        try:
                            utilisateur_connecte.permissions_recues = json.loads(perms_recues)
                        except:
                            perms_recues = perms_recues.strip("[]").replace("'", "").replace('"', "")
                            if perms_recues:
                                utilisateur_connecte.permissions_recues = [p.strip() for p in perms_recues.split(",") if p.strip()]
                
                print("Connexion réussie")
                if est_admin:
                    print("Vous êtes connecté en tant qu'administrateur.")
                break
    
    if utilisateur_connecte is None:
        print("Connexion échouée")
        return
    
    # Utilisation de l'utilisateur connecté pour les opérations
    if est_admin:
        menu_actions_admin(utilisateur_connecte)
    else:
        menu_actions(utilisateur_connecte)


def menu_actions(client: Client):
    """
    Affiche le menu d'actions et gère les interactions avec le client connecté.
    
    Args:
        client: Instance du Client connecté
    """
    print("--------------------------------")
    print("Menu Client - Choisir une action :")
    print("1. visualiser son annuaire")
    print("2. ajouter un contact")
    print("3. supprimer un contact")
    print("4. modifier un contact")
    print("5. rechercher un contact")
    print("6. Se déconnecter")
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
            print(f"  - ID: {contact.get('id_contact')}, {contact.get('prenom')} {contact.get('nom')}, Email: {contact.get('email')}, Adresse: {contact.get('adresse')}, Téléphone: {contact.get('telephone')}")
    print()
    menu_actions(client)


def ajouter_contact(client: Client):
    """Ajoute un contact à l'annuaire."""
    print("Ajout d'un contact :")
    nom = input("Nom : ")
    prenom = input("Prénom : ")
    email = input("Email : ")
    telephone = input("Téléphone : ")
    adresse = input("Adresse : ")
    
    contact = {
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




def menu_actions_admin(admin: Administrateur):
    """
    Affiche le menu d'actions pour les administrateurs.
    
    Args:
        admin: Instance de l'Administrateur connecté
    """
    print("--------------------------------")
    print("Menu Administrateur - Choisir une action :")
    print("1. créer un utilisateur")
    print("2. supprimer un utilisateur")
    print("3. modifier un utilisateur")
    print("4. lister les utilisateurs")
    print("5. Se déconnecter")
    choix = input("Choisir une action : ")
    if choix == "1":
        creer_utilisateur(admin)
    elif choix == "2":
        supprimer_utilisateur(admin)
    elif choix == "3":
        modifier_utilisateur(admin)
    elif choix == "4":
        lister_utilisateurs(admin)
    elif choix == "5":
        deconnecter_serveur()
        exit()
    else:
        print("Choix invalide")
        menu_actions_admin(admin)


def creer_utilisateur(admin: Administrateur):
    """Crée un nouvel utilisateur (réservé aux administrateurs)."""
    print("Création d'un nouvel utilisateur :")
    email = input("Email du nouvel utilisateur : ")
    mot_de_passe = input("Mot de passe : ")
    
    # Vérifier si l'email existe déjà
    clients_csv_path = data_dir / "clients.csv"
    email_existe = False
    
    if clients_csv_path.exists():
        with open(clients_csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("email") == email:
                    email_existe = True
                    break
    
    if email_existe:
        print(f"Erreur : L'email {email} existe déjà.")
        print()
        menu_actions_admin(admin)
        return
    
    # Créer le nouvel utilisateur avec la classe Administrateur
    nouvel_utilisateur_dict = admin.creer_utilisateur(email, mot_de_passe)
    
    # Générer un identifiant unique
    identifiant = nouvel_utilisateur_dict["identifiant"]
    hash_mdp = nouvel_utilisateur_dict["hash_mot_de_passe"]
    chemin_annuaire = f"data/{identifiant}.csv"
    
    # Ajouter l'utilisateur au fichier CSV
    nouvelle_ligne = {
        "id_client": identifiant,
        "email": email,
        "hash_mdp": hash_mdp,
        "chemin_annuaire": chemin_annuaire
    }
    
    with open(clients_csv_path, "a", encoding="utf-8", newline="") as f:
        fieldnames = ["id_client", "email", "hash_mdp", "chemin_annuaire"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(nouvelle_ligne)
    
    print(f"Utilisateur {email} créé avec succès.")
    print()
    menu_actions_admin(admin)


def supprimer_utilisateur(admin: Administrateur):
    """Supprime un utilisateur (réservé aux administrateurs)."""
    email = input("Email de l'utilisateur à supprimer : ")
    
    if email == ADMIN_EMAIL:
        print("Erreur : Impossible de supprimer l'administrateur.")
        print()
        menu_actions_admin(admin)
        return
    
    clients_csv_path = data_dir / "clients.csv"
    
    if not clients_csv_path.exists():
        print("Aucun utilisateur trouvé.")
        print()
        menu_actions_admin(admin)
        return
    
    # Lire tous les utilisateurs
    lignes = []
    utilisateur_trouve = False
    
    with open(clients_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row.get("email") != email:
                lignes.append(row)
            else:
                utilisateur_trouve = True
                # Supprimer aussi le fichier d'annuaire associé
                chemin_annuaire = row.get("chemin_annuaire", "")
                if chemin_annuaire:
                    chemin_absolu = data_dir / Path(chemin_annuaire).name
                    if chemin_absolu.exists():
                        try:
                            os.remove(chemin_absolu)
                        except:
                            pass
    
    if not utilisateur_trouve:
        print(f"Erreur : L'utilisateur {email} n'existe pas.")
        print()
        menu_actions_admin(admin)
        return
    
    # Réécrire le fichier sans l'utilisateur supprimé
    with open(clients_csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(lignes)
    
    print(f"Utilisateur {email} supprimé avec succès.")
    print()
    menu_actions_admin(admin)


def modifier_utilisateur(admin: Administrateur):
    """Modifie un utilisateur (réservé aux administrateurs)."""
    email = input("Email de l'utilisateur à modifier : ")
    
    clients_csv_path = data_dir / "clients.csv"
    
    if not clients_csv_path.exists():
        print("Aucun utilisateur trouvé.")
        print()
        menu_actions_admin(admin)
        return
    
    # Lire tous les utilisateurs et trouver celui à modifier
    lignes = []
    utilisateur_trouve = False
    
    with open(clients_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        
        for row in reader:
            if row.get("email") == email:
                utilisateur_trouve = True
                print("Entrez les nouveaux champs (laisser vide pour ne pas modifier) :")
                
                nouveau_email = input(f"Nouvel email (actuel: {email}) : ")
                nouveau_mdp = input("Nouveau mot de passe (laisser vide pour ne pas modifier) : ")
                
                if nouveau_email:
                    row["email"] = nouveau_email
                
                if nouveau_mdp:
                    row["hash_mdp"] = hashlib.sha256(nouveau_mdp.encode()).hexdigest()
                
                lignes.append(row)
            else:
                lignes.append(row)
    
    if not utilisateur_trouve:
        print(f"Erreur : L'utilisateur {email} n'existe pas.")
        print()
        menu_actions_admin(admin)
        return
    
    # Réécrire le fichier
    with open(clients_csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(lignes)
    
    print(f"Utilisateur modifié avec succès.")
    print()
    menu_actions_admin(admin)


def lister_utilisateurs(admin: Administrateur):
    """Liste tous les utilisateurs (réservé aux administrateurs)."""
    clients_csv_path = data_dir / "clients.csv"
    
    if not clients_csv_path.exists():
        print("Aucun utilisateur trouvé.")
        print()
        menu_actions_admin(admin)
        return
    
    utilisateurs = []
    with open(clients_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            utilisateurs.append({
                "email": row.get("email", ""),
                "identifiant": row.get("id_client", ""),
                "est_admin": row.get("email", "") == ADMIN_EMAIL
            })
    
    
    if not utilisateurs:
        print("Aucun utilisateur trouvé.")
    else:
        print(f"\nListe des utilisateurs ({len(utilisateurs)} utilisateur(s)) :")
        for user in utilisateurs:
            role = "Administrateur" if user["est_admin"] else "Client"
            print(f"  - Email: {user['email']}, ID: {user['identifiant']}, Rôle: {role}")
    
    print()
    menu_actions_admin(admin)


def deconnecter_serveur():
    """Déconnecte le client."""
    print("Déconnexion réussie.")
    exit()

def envoyer_pdu():
    pass

def recevoir_pdu():
    pass




def main() -> None:
    creer_serveur()




if __name__ == "__main__":
    main()