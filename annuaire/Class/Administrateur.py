"""
Classe Administrateur - Extension de la classe Client (Utilisateur).
Aucun attribut spécifique. Le rôle détermine les privilèges.
Aucune logique réseau intégrée : modélisation stricte des données et des opérations.
"""

from typing import List, Dict
from .Client import Client


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
        chemin_annuaire = f"data/annuaires/{identifiant}.csv"
        
        # Création d'un dictionnaire représentant le nouvel utilisateur
        nouvel_utilisateur = {
            'identifiant': identifiant,
            'mail': mail,
            'hash_mot_de_passe': empreinte,
            'chemin_annuaire': chemin_annuaire,
            'permissions_accordees': [],
            'permissions_recues': []
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

