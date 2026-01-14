"""
Classe Utilisateur - Représentation d'un utilisateur et de ses opérations internes.
Aucune logique réseau intégrée : modélisation stricte des données et des opérations.
"""

import hashlib
import os
import uuid
from typing import List, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .Annuaire import Annuaire


class Client:
    """
    Représente un utilisateur et gère ses opérations internes.
    """
    
    def __init__(self, mail: str, hash_mot_de_passe: str):
        """
        Initialise un utilisateur.
        
        Args:
            mail: Adresse email de l'utilisateur (utilisée pour la connexion)
            hash_mot_de_passe: Hash du mot de passe
        """
        # Génération automatique d'un identifiant unique
        self.identifiant = str(uuid.uuid4())
        self.mail = mail
        self.hash_mot_de_passe = hash_mot_de_passe
        # Génération automatique du chemin d'annuaire basé sur l'identifiant unique
        self.chemin_annuaire = f"data/{self.identifiant}.csv"
        self.permissions_accordees: List[str] = []  # Liste des identifiants ayant reçu des permissions
        self.permissions_recues: List[str] = []  # Liste des identifiants ayant accordé des permissions
        self._annuaire: Optional[Annuaire] = None
    
    
    def _charger_annuaire(self) -> 'Annuaire':
        """
        Charge l'annuaire de l'utilisateur depuis le fichier CSV.
        
        Returns:
            Instance de l'Annuaire chargé
        """
        if self._annuaire is None:
            from .Annuaire import Annuaire
            self._annuaire = Annuaire(self, self.chemin_annuaire)
            if os.path.exists(self.chemin_annuaire):
                self._annuaire.charger()
        return self._annuaire
    
    def ajouter_contact(self, contact):
        """
        Ajoute un contact à l'annuaire de l'utilisateur.
        
        Args:
            contact: Contact à ajouter
        """
        annuaire = self._charger_annuaire()
        annuaire.ajouter(contact)
        annuaire.sauvegarder()
    
    def supprimer_contact(self, id_contact: int):
        """
        Supprime un contact de l'annuaire de l'utilisateur.
        
        Args:
            id_contact: Identifiant du contact à supprimer
        """
        annuaire = self._charger_annuaire()
        annuaire.supprimer(id_contact)
        annuaire.sauvegarder()
    
    def modifier_contact(self, id_contact: int, champs: Dict):
        """
        Modifie un contact dans l'annuaire de l'utilisateur.
        
        Args:
            id_contact: Identifiant du contact à modifier
            champs: Dictionnaire contenant les champs à modifier
        """
        annuaire = self._charger_annuaire()
        contacts = annuaire.rechercher({'id_contact': id_contact})
        if contacts:
            contact = contacts[0]
            contact.update(champs)
            annuaire.sauvegarder()
    
    def rechercher_contact(self, criteres: Dict):
        """
        Recherche des contacts dans l'annuaire selon des critères.
        
        Args:
            criteres: Dictionnaire de critères de recherche
            
        Returns:
            Liste des contacts correspondant aux critères
        """
        annuaire = self._charger_annuaire()
        return annuaire.rechercher(criteres)
    
    def lister_contacts(self):
        """
        Liste tous les contacts de l'annuaire.
        
        Returns:
            Liste de tous les contacts
        """
        annuaire = self._charger_annuaire()
        return annuaire.lister()
    
    def accorder_permission(self, utilisateur: str):
        """
        Accorde une permission d'accès à un autre utilisateur.
        
        Args:
            utilisateur: Identifiant de l'utilisateur auquel accorder la permission
        """
        if utilisateur not in self.permissions_accordees:
            self.permissions_accordees.append(utilisateur)
    
    def retirer_permission(self, utilisateur: str):
        """
        Retire une permission d'accès à un autre utilisateur.
        
        Args:
            utilisateur: Identifiant de l'utilisateur auquel retirer la permission
        """
        if utilisateur in self.permissions_accordees:
            self.permissions_accordees.remove(utilisateur)
    
    def exporter_csv(self) -> str:
        """
        Exporte l'annuaire au format CSV.
        
        Returns:
            Chemin du fichier CSV exporté
        """
        annuaire = self.charger_annuaire()
        return annuaire.exporter_csv()
    
    def importer_csv(self, fichier: str):
        """
        Importe un annuaire depuis un fichier CSV.
        
        Args:
            fichier: Chemin vers le fichier CSV à importer
        """
        annuaire = self.charger_annuaire()
        annuaire.importer_csv(fichier)
        annuaire.sauvegarder()

