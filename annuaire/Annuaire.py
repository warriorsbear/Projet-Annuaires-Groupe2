"""
Classe Annuaire - Conteneur des contacts associé à un utilisateur.
Aucune logique réseau intégrée : modélisation stricte des données et des opérations.
"""

import os
import csv
from typing import List, Dict, Optional, TYPE_CHECKING
from .Contact import Contact

if TYPE_CHECKING:
    from .Client import Client


class Annuaire:
    """
    Conteneur des contacts associé à un utilisateur.
    """
    
    def __init__(self, proprietaire: 'Client', fichier_csv: str):
        """
        Initialise un annuaire.
        
        Args:
            proprietaire: Utilisateur propriétaire de l'annuaire
            fichier_csv: Chemin vers le fichier CSV de l'annuaire
        """
        self.proprietaire = proprietaire
        self.fichier_csv = fichier_csv
        self.contacts: List[Contact] = []
    
    def charger(self):
        """
        Charge les contacts depuis le fichier CSV.
        """
        self.contacts = []
        if os.path.exists(self.fichier_csv):
            try:
                with open(self.fichier_csv, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        contact = Contact.from_dict(row)
                        # Conversion de l'id_contact en int
                        contact.id_contact = int(contact.id_contact) if contact.id_contact else 0
                        self.contacts.append(contact)
            except Exception as e:
                # En cas d'erreur, on démarre avec une liste vide
                self.contacts = []
    
    def sauvegarder(self):
        """
        Sauvegarde les contacts dans le fichier CSV.
        """
        # Créer le répertoire si nécessaire
        os.makedirs(os.path.dirname(self.fichier_csv) if os.path.dirname(self.fichier_csv) else '.', exist_ok=True)
        
        try:
            with open(self.fichier_csv, 'w', encoding='utf-8', newline='') as f:
                if self.contacts:
                    fieldnames = ['id_contact', 'nom', 'prenom', 'email', 'telephone', 'adresse']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for contact in self.contacts:
                        writer.writerow(contact.to_dict())
                else:
                    # Écrire juste l'en-tête si aucun contact
                    writer = csv.DictWriter(f, fieldnames=['id_contact', 'nom', 'prenom', 'email', 'telephone', 'adresse'])
                    writer.writeheader()
        except Exception as e:
            raise Exception(f"Erreur lors de la sauvegarde de l'annuaire : {e}")
    
    def ajouter(self, contact: Contact):
        """
        Ajoute un contact à l'annuaire.
        
        Args:
            contact: Contact à ajouter
        """
        if not contact.valider():
            raise ValueError("Le contact n'est pas valide")
        
        # Vérifier que l'ID n'existe pas déjà
        if any(c.id_contact == contact.id_contact for c in self.contacts):
            raise ValueError(f"Un contact avec l'ID {contact.id_contact} existe déjà")
        
        self.contacts.append(contact)
    
    def supprimer(self, id_contact: int):
        """
        Supprime un contact de l'annuaire.
        
        Args:
            id_contact: Identifiant du contact à supprimer
        """
        self.contacts = [c for c in self.contacts if c.id_contact != id_contact]
    
    def rechercher(self, criteres: Dict) -> List[Contact]:
        """
        Recherche des contacts selon des critères.
        
        Args:
            criteres: Dictionnaire de critères de recherche
            
        Returns:
            Liste des contacts correspondant aux critères
        """
        resultats = self.contacts.copy()
        
        for critere, valeur in criteres.items():
            if critere == 'id_contact':
                resultats = [c for c in resultats if c.id_contact == valeur]
            elif critere == 'nom':
                resultats = [c for c in resultats if valeur.lower() in c.nom.lower()]
            elif critere == 'prenom':
                resultats = [c for c in resultats if valeur.lower() in c.prenom.lower()]
            elif critere == 'email':
                resultats = [c for c in resultats if valeur.lower() in c.email.lower()]
            elif critere == 'telephone':
                resultats = [c for c in resultats if valeur in c.telephone]
            elif critere == 'adresse':
                resultats = [c for c in resultats if valeur.lower() in c.adresse.lower()]
        
        return resultats
    
    def lister(self) -> List[Contact]:
        """
        Liste tous les contacts de l'annuaire.
        
        Returns:
            Liste de tous les contacts
        """
        return self.contacts.copy()
    
    def importer_csv(self, fichier: str):
        """
        Importe des contacts depuis un fichier CSV.
        
        Args:
            fichier: Chemin vers le fichier CSV à importer
        """
        if not os.path.exists(fichier):
            raise FileNotFoundError(f"Le fichier {fichier} n'existe pas")
        
        nouveaux_contacts = []
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    contact = Contact.from_dict(row)
                    # Conversion de l'id_contact en int
                    contact.id_contact = int(contact.id_contact) if contact.id_contact else 0
                    if contact.valider():
                        nouveaux_contacts.append(contact)
        except Exception as e:
            raise Exception(f"Erreur lors de l'import CSV : {e}")
        
        # Ajouter les nouveaux contacts (en évitant les doublons d'ID)
        ids_existants = {c.id_contact for c in self.contacts}
        for contact in nouveaux_contacts:
            if contact.id_contact not in ids_existants:
                self.contacts.append(contact)
                ids_existants.add(contact.id_contact)
    
    def exporter_csv(self) -> str:
        """
        Exporte l'annuaire au format CSV.
        
        Returns:
            Chemin du fichier CSV exporté (identique à self.fichier_csv)
        """
        self.sauvegarder()
        return self.fichier_csv

