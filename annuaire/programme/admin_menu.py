"""
Module pour les fonctions et menus liés aux administrateurs.
"""

import os
import sys
import hashlib
import csv
from pathlib import Path

# Configuration du chemin pour les imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Class import Administrateur, Client  # type: ignore

# Import des fonctions client communes (pour les opérations sur l'annuaire)
# Utilisation d'un import relatif au même package
from programme import client_menu

# Constantes
ADMIN_EMAIL = "admin@admin.fr"
data_dir = Path(__file__).parent.parent / "data"


def menu_actions_admin(admin: Administrateur):
    """
    Affiche le menu d'actions pour les administrateurs.
    
    Args:
        admin: Instance de l'Administrateur connecté
    """
    print("--------------------------------")
    print("Menu Administrateur - Choisir une action :")
    print("1. créer un compte utilisateur")
    print("2. supprimer un utilisateur")
    print("3. modifier un compte utilisateur")
    print("4. lister les comptes utilisateurs")
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
        print("Déconnexion réussie.")
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
        "chemin_annuaire": chemin_annuaire,
        "liste_permissions_accordees": "[]",
        "liste_permissions_recues": "[]"
    }
    
    with open(clients_csv_path, "a", encoding="utf-8", newline="") as f:
        fieldnames = ["id_client", "email", "hash_mdp", "chemin_annuaire", 
                     "liste_permissions_accordees", "liste_permissions_recues"]
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
