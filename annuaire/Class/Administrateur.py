"""
Classe Administrateur - Extension de la classe Client (Utilisateur).
Aucun attribut spécifique. Le rôle détermine les privilèges.
Aucune logique réseau intégrée : modélisation stricte des données et des opérations.
"""

from typing import List, Dict
from .Client import Client
import csv
import os
from pathlib import Path


class Administrateur(Client):
    """
    Extension de la classe Client.
    Le rôle détermine les privilèges, pas d'attributs supplémentaires.
    """
    
    def __init__(self, mail: str, hash_mot_de_passe: str):
        """
        Initialise un administrateur.
        
        Args:
            mail: Adresse email de l'administrateur (utilisée pour la connexion)
            hash_mot_de_passe: Hash du mot de passe
        """
        super().__init__(mail, hash_mot_de_passe)
    
    def creer_utilisateur(self, mail: str, mot_de_passe: str) -> Dict:
        """
        Crée un nouvel utilisateur.
        
        Args:
            mail: Adresse email du nouvel utilisateur (utilisée pour la connexion)
            mot_de_passe: Mot de passe en clair (sera hashé)
            
        Returns:
            Dictionnaire contenant les informations du nouvel utilisateur créé
        """
        import hashlib
        import uuid
        
        # Génération de l'identifiant unique
        identifiant = str(uuid.uuid4())
        
        # Génération de l'empreinte du mot de passe
        empreinte = hashlib.sha256(mot_de_passe.encode()).hexdigest()
        
        # Création du chemin d'annuaire basé sur l'identifiant unique
        # Déterminer le chemin absolu depuis le répertoire Class
        current_file = Path(__file__)
        data_dir = current_file.parent.parent / "data"
        chemin_annuaire_relatif = f"data/{identifiant}.csv"
        chemin_annuaire_absolu = data_dir / f"{identifiant}.csv"
        
        # Créer le répertoire data s'il n'existe pas
        data_dir.mkdir(parents=True, exist_ok=True)

        # Création du fichier d'annuaire vide
        with open(chemin_annuaire_absolu, "w", encoding="utf-8", newline="") as f:
            fieldnames_annuaire = ["id_contact", "nom", "prenom", "email", "telephone", "adresse"]
            writer = csv.DictWriter(f, fieldnames=fieldnames_annuaire)
            writer.writeheader()
        
        # Création d'un dictionnaire représentant le nouvel utilisateur
        nouvel_utilisateur = {
            'identifiant': identifiant,
            'mail': mail,
            'hash_mot_de_passe': empreinte,
            'chemin_annuaire': chemin_annuaire_relatif
        }
        
        return nouvel_utilisateur
    
    def supprimer_utilisateur(self, username: str) -> bool:
        """
        Supprime un utilisateur.
        
        Args:
            username: Identifiant de l'utilisateur à supprimer
            
        Returns:
            True si la suppression a réussi, False sinon
        """
        # Cette méthode retourne un booléen pour indiquer le succès
        # La logique de suppression réelle serait gérée par le serveur
        return True
    
    def modifier_utilisateur(self, username: str, nouveaux_champs: Dict) -> Dict:
        """
        Modifie les informations d'un utilisateur.
        
        Args:
            username: Identifiant de l'utilisateur à modifier
            nouveaux_champs: Dictionnaire contenant les champs à modifier
            
        Returns:
            Dictionnaire contenant les informations mises à jour de l'utilisateur
        """
        # Cette méthode retourne les champs mis à jour
        # La logique de modification réelle serait gérée par le serveur
        utilisateur_modifie = {
            'identifiant': username,
            **nouveaux_champs
        }
        return utilisateur_modifie
    
    def lister_utilisateurs(self) -> List[Dict]:
        """
        Liste tous les utilisateurs du système.
        
        Returns:
            Liste de dictionnaires contenant les informations des utilisateurs
        """
        # Cette méthode retourne une liste vide par défaut
        # La logique de listing réelle serait gérée par le serveur
        return []

