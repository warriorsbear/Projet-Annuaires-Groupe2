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
from programme.client_menu import menu_actions
from programme.admin_menu import menu_actions_admin

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





def envoyer_pdu():
    pass

def recevoir_pdu():
    pass




def main() -> None:
    creer_serveur()




if __name__ == "__main__":
    main()